from cadquery import Workplane, Vector
from math import floor, ceil
from . import Miscellaneous
Size = Miscellaneous.Size
Switch = Miscellaneous.Switch
Periodicity = Miscellaneous.Periodicity
BoundingBox = Miscellaneous.BoundingBox
from . import UnitaryCell
UnitaryCell = UnitaryCell.UnitaryCell
from copy import deepcopy


class Lattice:
    """
    Repräsentation des Gitters, welches aus Elementarzellen aufgebaut ist
    """
    def __init__(self,
                 space: BoundingBox | None = None,
                 preferred_cell_size: Size = Size(),
                 strict: Switch = Switch() ):
        """
        Initialisierung des Gitters

        :parameter space: Raum, in welchem das Gitter erzeugt werden soll
        :parameter strict: steuert, ob die gegebenen Abmessungen des Begrenzungsraumes genau eingehalten werden sollen
        """

        self.geometry = None
        self.space: BoundingBox | None = space
        self.adjusted_space: BoundingBox | None = space
        self.cell_size: Size = preferred_cell_size
        self.periodicity = Periodicity()
        self.initialized: bool = True

        if preferred_cell_size == Size():
            self.initialized = False

        self.has_grid = False

        if not self.initialized:
            return

        for direction in range( len( preferred_cell_size ) ):
            if strict[ direction ]:
                self.periodicity[ direction ] = ceil( self.space.length( direction ) / preferred_cell_size[ direction ] )

                d_bb = preferred_cell_size[ direction ] * self.periodicity[ direction ] - self.space.length( direction )
                self.space.extend( direction, d_bb )
                self.adjusted_space.extend( direction, d_bb - preferred_cell_size[ direction ] )
            else:
                self.periodicity[ direction ] = ceil( self.space.length( direction ) / preferred_cell_size[ direction ] )
                self.cell_size[ direction ] = self.space.length( direction ) / self.periodicity[ direction ]
                self.adjusted_space.extend( direction, - self.cell_size[ direction ] )

    def create( self, cell: UnitaryCell, combine: bool = False ) -> None:
        """
        Erstellt die Geometrie des Gitters unter Verwendung der Elementarzelle

        :parameter cell: Elementarzelle, mit der das Gitter erstellt werden soll
        :parameter combine: steuert, die Verschmelzung der Elementarzellen
        """
        if not self.initialized:
            raise ValueError( "Gitter wurde noch nicht initialisiert." )

        cmin: Vector = Vector( self.adjusted_space.min() )

        points: list[ tuple[ float, float, float ] ] = [
            ( cmin.x + nx * cell.size.dx, cmin.y + ny * cell.size.dy, cmin.z + nz * cell.size.dz )
            for nx in range( self.periodicity.nx )
            for ny in range( self.periodicity.ny )
            for nz in range( self.periodicity.nz )
        ]

        self.geometry = Workplane().pushPoints( points ).eachpoint(
            lambda loc: cell.geometry.val().located( loc ), combine = combine )

        self.has_grid = True

    def reset( self ):
        """
        Löscht die Geometrie des Gitters
        """
        self.geometry = Workplane()
        self.has_grid = False

    def empty( self ) -> bool:
        """
        Prüft ob eine Geometrie für das Gitter vorhanden ist

        :return: True, wenn keine Geometrie vorhanden ist
        """
        return not self.has_grid
from . import Miscellaneous
Size = Miscellaneous.Size
from . import CellConfiguration
CellConfiguration = CellConfiguration.CellConfiguration
from cadquery import Workplane, Plane, Location, Vector
from cadquery.selectors import BoxSelector


class UnitaryCell:
    """
    Geometrische Repräsentation der Elementarzelle
    """
    def __init__( self, size: Size = Size() ):
        """
        Initialisierung der Elementarzelle über Angabe der räumlichen Dimensionen

        :parameter size: Abmaße der Elementarzelle
        """
        def _vertices( measures: Size ) -> dict[ int, Vector ]:
            return {
                1: Vector( ( - measures.dx / 2., - measures.dy / 2., - measures.dz / 2.) ),
                2: Vector( ( - measures.dx / 2., measures.dy / 2., - measures.dz / 2.) ),
                3: Vector( ( measures.dx / 2., measures.dy / 2., - measures.dz / 2.) ),
                4: Vector( ( measures.dx / 2., - measures.dy / 2., - measures.dz / 2.) ),
                5: Vector( ( - measures.dx / 2., - measures.dy / 2., measures.dz / 2.) ),
                6: Vector( ( measures.dx / 2., - measures.dy / 2., measures.dz / 2.) ),
                7: Vector( ( measures.dx / 2., measures.dy / 2., measures.dz / 2.) ),
                8: Vector( ( - measures.dx / 2., measures.dy / 2., measures.dz / 2.) )
            }
        self.size = size
        self.vertices = _vertices( size )
        self.initialized = False
        self.geometry: Workplane = Workplane()

        if not size == Size():
            self.initialized = True

        self.has_cell = False

    def create( self, config: CellConfiguration, box_intersect = True ) -> None:
        """
        Erstellung der Elementarzelle aus gegebener Konfiguration

        :parameter config: Konfiguration der Elementarzelle
        :parameter box_intersect: Steuert das Zurechtschneiden der Elementarzelle auf die gegebenen Abmaße
        """

        if not self.initialized:
            raise ValueError( "Die Elementarzelle wurde noch nicht initialisiert." )

        for entity in config:
            dimension = entity.dimension()

            if dimension == -1:
                selection: BoxSelector = BoxSelector(
                    self.vertices[ 1 ], self.vertices[ 7 ] )
                self.geometry = self.geometry.edges( selection ).fillet( entity.get( "radius" ) )

            if dimension == 0:
                radius: float = entity.get( "diameter" ) / 2.
                self.geometry = self.geometry.union(
                    Workplane().sphere( radius ).val().located( loc = Location( entity.geometry[ 0 ] ) ) )

            if dimension == 1:
                radius: float = entity.get( "diameter" ) / 2.
                first, last = tuple( entity.geometry )
                plane = Plane( origin = ( first + last ) / 2., normal = ( first - last ).normalized() )
                self.geometry = self.geometry.union(
                    Workplane( plane ).cylinder( height = ( first - last ).Length, radius = radius ) )

            if dimension == 2:
                first, second, third = tuple( entity.geometry )
                normal = ( second - first ).cross( third - second ).normalized()
                plane = Plane( origin = first, normal = normal,
                               xDir = ( second - first ).normalized() )
                plane_points = [ ( ( p - first ).dot( plane.xDir ), ( p - first ).dot( plane.yDir ) )
                                 for p in entity.geometry ]
                thickness: float = entity.get( "thickness" )
                self.geometry = self.geometry.union(
                    Workplane( plane ).polyline( plane_points ).close().extrude(
                        thickness / 2., both=True ) )

        if box_intersect:
            self.geometry = self.geometry.intersect(
                Workplane().box( self.size.dx, self.size.dy, self.size.dz ) )

        self.has_cell = True

    def reset( self ) -> None:
        """
        Entfernt die Geometrie der Elementarzelle
        """
        self.geometry = Workplane()
        self.has_cell = False
        self.vertices = {}
        self.initialized = False

    def empty( self ) -> bool:
        """
        Prüft, ob das Objekt eine Geometrie besitzt
        :return: True, wenn die Elementarzelle nicht definiert ist.
        """
        return not self.has_cell and self.initialized

    def density( self ) ->  float | None:
        """
        Berechnet die relative Dichte der Elementarzelle aus dem Verhältnis des Geometrievolumens und des
        eingeschlossenen Zellvolumens

        :return: True, wenn die Elementarzelle nicht definiert ist.
        """
        if self.empty():
            return None
        volume_cell : float = self.size.dx * self.size.dy * self.size.dz
        volume_struts : float = self.geometry.solids().val().Volume()
        return volume_struts / volume_cell



from cadquery import Workplane, importers, exporters
from . import Geometry
from . import Miscellaneous
from . import UnitaryCell
from . import Lattice
from . import CellConfiguration

Geometry = Geometry.Geometry
Size = Miscellaneous.Size
Periodicity = Miscellaneous.Periodicity
Switch = Miscellaneous.Switch
BoundingBox = Miscellaneous.BoundingBox
UnitaryCell = UnitaryCell.UnitaryCell
Lattice = Lattice.Lattice
Entity = CellConfiguration.Entity
CellConfiguration = CellConfiguration.CellConfiguration


class LatticeGeometryLib:
    def __init__( self ):
        self.config = CellConfiguration()
        self.geometry = Geometry()
        self.lattice: Lattice = Lattice()
        self.cell: UnitaryCell = UnitaryCell()

    def import_initial_model( self, filepath: str ) -> None:
        self.geometry = Geometry( importers.importStep( filepath ) )

    def export_initial_model( self, filepath: str ) -> None:
        exporters.export( self.get_initial_model(), filepath )

    def set_initial_model( self, solid: Workplane ) -> None:
        self.geometry = Geometry( solid )

    def get_initial_model( self ) -> Workplane:
        if not self.geometry.has_solid_geometry:
            raise ValueError( "Es ist kein Eingangsmodell verfügbar." )
        return self.geometry.solid_geometry

    def delete_initial_model( self ) -> None:
        self.geometry.reset()
        self.config.reset()
        self.cell.reset()
        self.lattice.reset()

    def create_shell( self, inner_thickness: float, outer_thickness: float = 0. ) -> None:
        if not self.geometry.has_solid_geometry:
            raise ValueError( "Es ist kein Eingangsmodell verfügbar." )
        self.geometry.shell( inner_thickness, outer_thickness )

    def import_shell( self, filepath: str ) -> None:
        self.geometry.shell( importers.importStep( filepath ) )

    def export_shell( self, filepath: str ) -> None:
        exporters.export( self.get_shell(), filepath )

    def set_shell( self, shell: Workplane ) -> None:
        self.geometry.shell( shell )

    def get_shell( self ) -> Workplane:
        if not self.geometry.has_shell_geometry:
            raise ValueError( "Es ist kein Schalenobjekt vorhanden." )
        return self.geometry.shell_geometry

    def delete_shell(self):
        self.geometry.shell = None
        self.geometry.has_shell = False
        self.delete_intersected_lattice()

    def init_unitary_cell( self,
                           length: tuple[ float, float, float ],
                           strict: tuple[ bool, bool, bool ] = ( False, False, False ) ) -> None:
        if not self.geometry.has_solid_geometry:
            raise ValueError( "Es ist kein Eingangsmodell verfügbar." )

        self.lattice = Lattice( self.geometry.bounding_box(), Size( *length ), Switch( *strict ) )
        self.cell = UnitaryCell( self.lattice.cell_size )
        self.config = CellConfiguration( self.cell.vertices )

    def get_entity( self, index: int | None = None ) -> Entity | list:
        if self.config.empty():
            raise ValueError( "Bis jetzt sind noch keine Informationen zur Topologie gegeben." )
        return self.config[ index ]

    def add_entity( self, entity: str | list ) -> None:
        if not self.cell.initialized:
            raise ValueError( "Es ist noch keine Einheitszelle initialisiert." )
        self.config.append( entity )

    def add_entities( self, entities: str | list ) -> None:
        if not self.cell.initialized:
            raise ValueError( "Es ist noch keine Einheitszelle initialisiert." )
        self.config.insert( entities )

    def delete_features( self ) -> None:
        self.config.reset()
        self.cell.reset()
        self.lattice.reset()
        self.delete_intersected_lattice()

    def create_unitary_cell( self ) -> None:
        if self.config.empty():
            raise ValueError( "Bis jetzt sind noch keine Informationen zur Topologie gegeben." )
        if not self.cell.initialized:
            raise ValueError( "Es ist noch keine Einheitszelle initialisiert." )
        self.cell.create( self.config )

    def export_unitary_cell( self, filepath: str ) -> None:
        exporters.export( self.get_unitary_cell(), filepath )

    def get_unitary_cell( self ) -> Workplane:
        if self.cell.empty():
            raise ValueError( "Es ist keine Einheitszelle vorhanden." )
        return self.cell.geometry

    def delete_unitary_cell( self ):
        self.cell.reset()
        self.lattice.reset()
        self.delete_intersected_lattice()

    def create_lattice( self ) -> None:
        if self.cell.empty():
            raise ValueError( "Es ist keine Einheitszelle vorhanden." )
        self.lattice.create( self.cell )

    def export_lattice( self, filepath: str ) -> None:
        exporters.export( self.get_lattice(), filepath )

    def get_lattice( self ) -> Workplane:
        if self.lattice.empty():
            raise ValueError( "Es ist kein Gitter vorhanden." )
        return self.lattice.geometry

    def delete_lattice( self ):
        self.lattice.reset()
        self.delete_intersected_lattice()

    def intersect_lattice( self ) -> None:
        if self.lattice.empty():
            raise ValueError( "Es ist kein Gitter vorhanden." )
        if not self.geometry.has_solid_geometry:
            raise ValueError( "Es ist kein Eingangsmodell verfügbar." )
        self.geometry.fill( self.lattice )

    def export_intersected_lattice(self, filepath: str) -> None:
        exporters.export( self.get_intersected_lattice(), filepath )

    def get_intersected_lattice( self ) -> Workplane:
        if not self.geometry.has_lattice_geometry:
            raise ValueError( "Es ist kein zurechtgeschnittenes Gitter verfügbar." )
        return self.geometry.lattice_geometry

    def delete_intersected_lattice( self ):
        self.geometry.core = None
        self.geometry.has_core = False
        self.delete_unified()

    def unify( self ) -> None:
        if not self.geometry.has_lattice_geometry:
            raise ValueError( "Es ist kein zurechtgeschnittenes Gitter verfügbar." )
        if not self.geometry.has_shell_geometry:
            raise ValueError( "Es ist kein Schalenobjekt vorhanden." )
        self.geometry.merge()

    def export_unified( self, filepath: str ) -> None:
        exporters.export( self.get_unified(), filepath )

    def get_unified(self) -> Workplane:
        if not self.geometry.has_union_geometry:
            raise ValueError("Es ist kein Modell mit Gitter vorhanden.")
        return self.geometry.union_geometry

    def delete_unified(self):
        self.geometry.union_geometry = None
        self.geometry.has_union_geometry = False

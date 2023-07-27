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


class LatticeGenerator:
    """
    Klasse zur Erzeugung einer Schalengeometrie mit Gitterjern aus
    einer Eingangsgeometrie
    """
    def __init__( self ):
        """
        Initialisiert einen LatticeGenerator
        """
        self.config = CellConfiguration()
        self.geometry = Geometry()
        self.lattice: Lattice = Lattice()
        self.cell: UnitaryCell = UnitaryCell()

    def import_initial_model( self, filepath: str ) -> None:
        """
        Importfunktion für die initiale Geometrie

        :param filepath: Pfad zur STEP-Datei
        """
        self.geometry = Geometry( importers.importStep( filepath ) )

    def export_initial_model( self, filepath: str ) -> None:
        """
        Exportfunktion für die initiale Geometrie

        :param filepath: Dateipfad der Datei
        """
        exporters.export( self.get_initial_model(), filepath )

    def set_initial_model( self, solid: Workplane ) -> None:
        """
        Setzen des initialen Modells

        :param solid: initiale Geometrie als CADQuery Workplane
        """
        self.geometry = Geometry( solid )

    def get_initial_model( self ) -> Workplane:
        """
        Rückgabefunktion für die initiale Geometrie

        :return: Modell als CADQuery Workplane
        """
        if not self.geometry.has_solid_geometry:
            raise ValueError( "Es ist kein Eingangsmodell verfügbar." )
        return self.geometry.solid_geometry

    def delete_initial_model( self ) -> None:
        """
        Löscht das initiale Modell
        """
        self.geometry.reset()
        self.config.reset()
        self.cell.reset()
        self.lattice.reset()

    def create_shell( self, inner_thickness: float, outer_thickness: float = 0. ) -> None:
        """
        Erstellt Schalengeometrie aus der initialen Geometrie

        :param inner_thickness: Aufdickung nach Innen gegenüber Oberfläche
        :param outer_thickness: Aufdickung nach außen gegenüber Oberfläche
        """
        if not self.geometry.has_solid_geometry:
            raise ValueError( "Es ist kein Eingangsmodell verfügbar." )
        self.geometry.shell( inner_thickness, outer_thickness )

    def import_shell( self, filepath: str ) -> None:
        """
        Importfunktion zum setzen der Schalengeometrie

        :param filepath: Dateipfad zur STEP-Datei
        """
        self.geometry.shell( importers.importStep( filepath ) )

    def export_shell( self, filepath: str ) -> None:
        """
        Exportfunktion für die Schalengeometrie

        :param filepath: Dateipfad für die CAD-Datei
        """
        exporters.export( self.get_shell(), filepath )

    def set_shell( self, shell: Workplane ) -> None:
        """
        Setzen der Schalengeometrie

        :param shell: Schalengeometrie als CADQuery Workplane
        """
        self.geometry.shell( shell_geometry = shell )

    def get_shell( self ) -> Workplane:
        """
        Rückgabefunktion für Schalengeometrie

        :return: Schalengeometrie als CADQuery Workplane
        """
        if not self.geometry.has_shell_geometry:
            raise ValueError( "Es ist kein Schalenobjekt vorhanden." )
        return self.geometry.shell_geometry

    def delete_shell(self):
        """
        Löscht die Schalengeometrie
        """
        self.geometry.shell = None
        self.geometry.has_shell = False
        self.delete_intersected_lattice()

    def init_unitary_cell( self,
                           length: tuple[ float, float, float ],
                           strict: tuple[ bool, bool, bool ]
                           = ( False, False, False ) ) -> None:
        """
        Initialisiert die Elementarzellgeometrie und das Gitter

        :param length: Bevorzugte Abmessungen der Elementarzelle
        :param strict: Einstellung, ob die gegebenen Abmessungen genau
                       eingehalten werden sollen
        """
        if not self.geometry.has_solid_geometry:
            raise ValueError( "Es ist kein Eingangsmodell verfügbar." )

        self.lattice = Lattice( self.geometry.bounding_box(), Size( *length ), Switch( *strict ) )
        self.cell = UnitaryCell( self.lattice.cell_size )
        self.config = CellConfiguration( self.cell.vertices )

    def get_entity( self, index: int | None = None ) -> Entity | list:
        """
        Rückgabefunktion für eine Entität

        :param index: Index der Entität
        :return: Entität
        """
        if self.config.empty():
            raise ValueError(
                "Bis jetzt sind noch keine Informationen zur Topologie gegeben." )
        return self.config[ index ]

    def add_entity( self, entity: str | list ) -> None:
        """
        Fügt eine Entität hinzu

        :param entity: Liste mit Informationen zur Entität
        """
        if not self.cell.initialized:
            raise ValueError(
                "Es ist noch keine Einheitszelle initialisiert." )
        self.config.append( entity )

    def add_entities( self, entities: str | list ) -> None:
        """
        Fügt eine Liste mit Entitäten hinzu

        :param entities: Liste mit Informationen zu Entitäten
        """
        if not self.cell.initialized:
            raise ValueError(
                "Es ist noch keine Einheitszelle initialisiert." )
        self.config.insert( entities )

    def delete_entities( self ) -> None:
        """
        Löscht alle Entitäten
        """
        self.config.reset()
        self.cell.reset()
        self.lattice.reset()
        self.delete_intersected_lattice()

    def create_unitary_cell( self ) -> None:
        """
        Erstellt die Geometrie der Elementarzelle aus der Konfiguration
        """
        if self.config.empty():
            raise ValueError( "Bis jetzt sind noch keine Informationen zur Topologie gegeben." )
        if not self.cell.initialized:
            raise ValueError( "Es ist noch keine Einheitszelle initialisiert." )
        self.cell.create( self.config )

    def export_unitary_cell( self, filepath: str ) -> None:
        """
        Exportiert die Elementarzellgeometrie

        :param filepath: Pfad zur CAD-Datei
        """
        exporters.export( self.get_unitary_cell(), filepath )

    def get_unitary_cell( self ) -> Workplane:
        """
        Rückgabefunktion für die Elementarzelle

        :return: Elementarzellgeometrie als CADQuery Workplane
        """
        if self.cell.empty():
            raise ValueError( "Es ist keine Einheitszelle vorhanden." )
        return self.cell.geometry

    def delete_unitary_cell( self ):
        """
        Löscht die Elementarzellgeometrie
        """
        self.cell.reset()
        self.lattice.reset()
        self.delete_intersected_lattice()

    def create_lattice( self ) -> None:
        """
        Erstellt das Gitter aus der Elementarzelle.
        """
        if self.cell.empty():
            raise ValueError( "Es ist keine Einheitszelle vorhanden." )
        self.lattice.create( self.cell )

    def export_lattice( self, filepath: str ) -> None:
        """
        Exportfunktion für das Gitter

        :param filepath: Pfad zur Datei
        """
        exporters.export( self.get_lattice(), filepath )

    def get_lattice( self ) -> Workplane:
        """
        Rückgabefunktion für das Gitter

        :return: Geometrie des Gitters als CADQuery-Workplane
        """
        if self.lattice.empty():
            raise ValueError( "Es ist kein Gitter vorhanden." )
        return self.lattice.geometry

    def delete_lattice( self ):
        """
        Läscht das Gitter
        """
        self.lattice.reset()
        self.delete_intersected_lattice()

    def intersect_lattice( self ) -> None:
        """
        Überschneidet das Gitter mit der Eingangsgeometrie
        """
        if self.lattice.empty():
            raise ValueError( "Es ist kein Gitter vorhanden." )
        if not self.geometry.has_solid_geometry:
            raise ValueError( "Es ist kein Eingangsmodell verfügbar." )
        self.geometry.fill( self.lattice )

    def export_intersected_lattice(self, filepath: str) -> None:
        exporters.export( self.get_intersected_lattice(), filepath )

    def get_intersected_lattice( self ) -> Workplane:
        """
        Rückgabefunktion für das zurechtgeschnittene Gitter
        """
        if not self.geometry.has_lattice_geometry:
            raise ValueError( "Es ist kein zurechtgeschnittenes Gitter verfügbar." )
        return self.geometry.lattice_geometry

    def delete_intersected_lattice( self ):
        """
        Lösch das zurechtgeschnittene Gitter
        """
        self.geometry.core = None
        self.geometry.has_core = False
        self.delete_unified()

    def unify( self ) -> None:
        """
        Verschmelzen des zurechtgeschnittenen Gitters und der
        Schalengeometrie
        """
        if not self.geometry.has_lattice_geometry:
            raise ValueError(
                "Es ist kein zurechtgeschnittenes Gitter verfügbar." )
        if not self.geometry.has_shell_geometry:
            raise ValueError(
                "Es ist kein Schalenobjekt vorhanden." )
        self.geometry.merge()

    def export_unified( self, filepath: str ) -> None:
        """
        Exportfunktion für die Schalengeometrie mit Gitterkern

        :param filepath: Pfad zur Datei
        """
        exporters.export( self.get_unified(), filepath )

    def get_unified(self) -> Workplane:
        """
        Rückgabefunktion für die Schalengeometrie mit Gitterkern

        :return: Geometrie als CADQuery-Workplane
        """
        if not self.geometry.has_union_geometry:
            raise ValueError(
                "Es ist kein Modell mit Gitter vorhanden.")
        return self.geometry.union_geometry

    def delete_unified(self):
        """
        Löscht die Schalengeometrie mit Gitterkern
        """
        self.geometry.union_geometry = None
        self.geometry.has_union_geometry = False
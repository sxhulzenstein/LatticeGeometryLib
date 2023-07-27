from cadquery import Workplane
import math
from . import Lattice
Lattice = Lattice.Lattice
from . import Miscellaneous
BoundingBox = Miscellaneous.BoundingBox


class Geometry:
    """
    Beinhaltet die Eingangsgeometrie und fügt in diese ein Gitter ein
    """
    def __init__( self, solid: Workplane | None = None):
        """
        Initialisierung der Geometrie mit einer Eingangsgeometrie

        :param solid: Eingangsgeometrie
        """
        self.solid_geometry: Workplane | None = solid
        self.has_solid_geometry: bool = True

        self.shell_geometry: Workplane | None = None
        self.has_shell_geometry: bool = False

        self.lattice_geometry: Workplane | None = None
        self.has_lattice_geometry : bool = False

        self.union_geometry: Workplane | None = None
        self.has_union_geometry: bool = False

        if solid is None:
            self.has_solid_geometry = False

    def bounding_box( self ) -> BoundingBox:
        if not self.has_solid_geometry:
            raise ValueError( "Es ist keine Eingangsgeometrie vorhanden." )
        bb = BoundingBox( self.solid_geometry )
        return bb

    def shell( self, inner_thickness: float = 0.,
               outer_thickness: float = 0.,
               shell_geometry: Workplane | None = None ) -> None:
        """
        Erstellt die Schalengeometrie für eine gegebene Eingangsgeometrie

        :param inner_thickness: Aufdickung der Oberfläche ins innere der Geometrie
        :param outer_thickness: Nach außen gerichtete Aufdickung der Oberfläche der Geometrie
        :param shell_geometry: importierte Schalengeometrie, falls extern erzeugt
        """

        if not shell_geometry is None:
            self.shell_geometry = shell_geometry
            self.has_shell_geometry = True
            return

        try:
            if inner_thickness  == 0. and not outer_thickness == 0.:
                self.shell_geometry = self.solid_geometry.shell( math.fabs( outer_thickness ) )

            elif not inner_thickness == 0. and outer_thickness == 0.:
                self.shell_geometry = self.solid_geometry.shell( - math.fabs( inner_thickness ) )

            elif not ( inner_thickness == 0. and outer_thickness == 0. ):
                self.shell_geometry = self.solid_geometry.shell(
                    - math.fabs( inner_thickness ) ).union( self.solid_geometry.shell( math.fabs( inner_thickness ) ) )

            else:
                raise UserWarning("Bitte beachten Sie, dass mindestens ein Dickenwert ungleich 0 sein muss.")

            self.has_shell_geometry = True

        except ValueError as exception:
            message = f"Fehlermeldung in der OpenCascade-Bibliothek: {exception}."
            message += "Eine mögliche Ursache hierfür ist, dass durch die Aufdickung degenerierte Flächen entstehen."
            message += " wählen Sie eine andere Wandstärke oder verwenden Sie in Ihrem Modell weniger Verrundungen."
            raise Exception( message )

        except UserWarning as user_warning:
            raise( user_warning )

        self.has_shell_geometry = True

    def fill( self, lattice: Lattice ) -> None:
        """
        Erstellt eine Überschneidung aus Gitter und Eingangsgeometrie

        :param lattice: regelmäßiges Gitter
        """
        if not self.has_solid_geometry:
            raise ValueError( "Es ist keine Eingangsgeometrie vorhanden." )

        self.lattice_geometry = self.solid_geometry.intersect(
            lattice.geometry, clean = False )
        self.has_lattice_geometry = True

    def merge( self ) -> None:
        """
        Vereinigt den Kern mit der Schale
        """
        if not self.has_shell_geometry:
            raise ValueError( "Es ist keine Schalengeometrie vorhanden." )

        if not self.has_lattice_geometry:
            raise ValueError( "Es ist kein Gitter als Kern vorhanden." )

        self.union_geometry = self.shell_geometry.union( self.lattice_geometry, clean = False )
        self.has_union_geometry = True

    def reset( self ) -> None:
        """
        Löscht das interne Gitter, die Schale und die Eingangsgeometrie
        """
        self.solid_geometry = None
        self.has_solid_geometry = False
        self.shell_geometry = None
        self.has_shell_geometry = False
        self.lattice_geometry = None
        self.has_lattice_geometry = False
        self.union_geometry = None
        self.has_union_geometry = False

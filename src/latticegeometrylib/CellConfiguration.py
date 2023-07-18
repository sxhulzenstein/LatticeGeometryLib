from cadquery import Vector
from typing import Any, Iterator
from ast import literal_eval
from copy import deepcopy

class Entity:
    """
    Enthält Informationen zum zu erstellenden Feature in der Elementarzelle
    """
    def __init__(self, info: list | str ) -> None:
        """
        Initialisiert die Entität, ohne Berücksichtigung der Abmaße der Elementarzelle

        :param info: Liste oder String, welches die zu erstellende Entität beschreibt
        """
        self.input: list | None = None

        if type( info ) is str:
            self.input = literal_eval( info )
        else:
            self.input = deepcopy( info )

        self.attributes: dict = deepcopy( info[ -1 ] )
        self.geometry: list[ Vector ] = []

    def create( self, vertices: dict[ int, Vector ], variables: dict = {} ) -> Any:
        """
        Berechnung der Koordinaten aller Knoten des Features aus Topologie

        :param vertices: Koordinaten der Eckknoten der Elementarzelle
        :param variables: Variablen zur Berücksichtigung parametrisierter Abmessungen
        """

        def _scales( config: tuple ) -> tuple:
            """
            Gibt die Relationen zwischen zwei Knoten aus. Sind nur die zwei Indizes der Eckknoten bekannt,
            werden als Relationen (0.5, 0.5) ausgegeben, was den Mittelpunkt der Eckknoten entspricht. Befindet sich auf
            Position 2 im Tupel eine Relation r, werden die Relationen (r, 1-r) ausgegeben. Befinden sich sowohl auf
            Position 2 und 3 Relationen, werden diese wieder ausgegeben.

            :param config: Tupel mit Relationen zwischen Eckknoten
            :return: Tupel mit Relationen
            """
            num: int = len( config )

            if num == 3: return config[ 2 ], 1. - config[ 2 ]
            if num == 4: return config[ 2 ], config[ 3 ]

            return 0.5, 0.5

        def _point( config: tuple | int ) -> Vector:
            """
            Berechnung der Koordinaten eines Punktes aus Topologieinformationen und Relationen zwischen zweier Punkte

            :param config: Index eines Eckknoten oder Tupel mit zwei Punkten und Relationen
            :return: ein Punkt als CADQuery Vector
            """
            if type( config ) is int:
                return vertices[ config ]

            u, v = _scales( config )

            return u * _point( config[ 0 ] ) + v * _point( config[ 1 ] )

        self.geometry = [ _point( index )
                          for index in self.input
                          if type( index ) is int or type( index ) is tuple  ]

        for a in self.attributes:
            if self.attributes[ a ] in variables:
                var = self.attributes[ a ]
                self.attributes[ a ] = variables[ var ]

        return self

    def __str__( self ) -> str:
        """
        Ausgabe der Topologieinformation, welche auch bei der Initialisierung übergeben wurde.
        """
        return str( self.input )

    def __getitem__( self, attribute: str ) -> Any:
        """
        Get-Funktion für Attribute

        :param attribute: Bezeichnung des Attributs
        :return: Wert des angeforderten Attributes
        """
        if attribute in self.attributes.keys():
            return self.attributes[ attribute ]
        else:
            raise AttributeError( f"Es ist kein Attribut mit der Bezeichnung { attribute } vorhanden." )

    def __setitem__( self, attribute, value ) -> None:
        """
        Set-Funktion für Attribute

        :param attribute: Bezeichnung des Attributs
        :param value: Neuer Wert des Attributs
        """
        self.attributes[ attribute ] = value

    def __bool__( self ) -> bool:
        """
        Überprüft, ob Feature mit Geometrieinformationen ausgeprägt ist

        :return: True, wenn Feature nicht leer ist
        """
        return not self.empty()

    def empty( self ) -> bool:
        """
        Überprüft, ob Feature leer ist, d.h., keine Geometrieinformationen enthält

        :return: True, wenn Feature leer ist
        """
        if len( self.geometry ) == 0:
            return True
        return False

    def dimension( self ) -> int:
        """
        Gibt die Dimension der Entität aus.\n
        Dimension -1: Verrundung\n
        Dimension 0: Knoten\n
        Dimension 1: Strebe\n
        Dimension 2: Fläche

        :return: Dimension der Entität
        """
        if not self.empty():
            return len( self.geometry ) - 1
        return -1

    def has(self, attribute: str) -> bool:
        """
        Überprüft, ob es das gegebene Attribut gibt

        :return: True, wenn das gegebene Attribut vorhanden ist
        """
        return attribute in self.attributes

    def set(self, attribute: str, value: Any) -> None:
        """
        Set-Funktion für Attribute

        :param attribute: Bezeichnung des Attributs
        :param value: Neuer Wert des Attributs
        """
        self.attributes[ attribute ] = value

    def get(self, attribute: str) -> Any:
        """
        Get-Funktion für Attribute

        :param attribute: Bezeichnung des Attributs
        :return: Wert des angeforderten Attributes
        """
        if not self.has( attribute ):
            return None
        return self.attributes[ attribute ]


class CellConfiguration:
    """
    Konfiguriert die Zusammensetzung der Elementarzelle
    """
    def __init__( self, vertices: dict | None = None ):
        """
        Initialisiert eine Elementarzellkonfiguration

        :param vertices: Eckknoten der Elementarzelle
        """
        self.entities: list[ Entity ] = []
        self.vertices: dict | None = vertices
        self.variables: dict = {}
        self.initialized = True

        if self.vertices is None:
            self.initialized = False

    def append( self, entity: str | Entity | list ) -> None:
        """
        Fügt eine einzelne Entität hinzu

        :param entity: Information zur Entität
        :raise ValueError, wenn keine Eckknoten vorhanden sind
        """
        if not self.initialized:
            raise ValueError( "CellConfiguration wurde noch nicht initialisiert" )

        def _template( info: dict ):
            """
            Liest eine Vorlage ein und fügt den Inhalt der Konfiguration hinzu

            :param info: beinhaltet den Dateipfad zur Vorlagendatei
            """
            filepath = info[ 'filepath' ]

            with open( filepath, mode='r' ) as template:
                content = literal_eval(
                    template.read().replace( "\n", "" ).replace( "\t", "" ).strip() )

                if not type( content[ 0 ] ) is list:
                    content = [content]

                for i in range( len( content ) ):
                    new_feature_list: list = content[ i ].copy()
                    self.append( new_feature_list )

        def _var( info: dict ):
            """
            Fügt der Variablenliste ein Element hinzu

            :param info: name und Wert der Variable
            """
            name = info[ 'name' ]
            value = info[ 'value' ]
            self.variables[ name ] = value

        if type( entity ) is list:
            if str( entity[ 0 ] ) == 'template':
                _template( entity[ -1 ] )

            elif str( entity[ 0 ] ) == 'var':
                _var( entity[ -1 ] )

            elif str( entity[ 0 ] ) == 'fillet':
                self.entities.append(  Entity( entity ).create( self.vertices, self.variables ) )

            elif type( entity[ 0 ] ) is tuple or type( entity[ 0 ] ) is int:
                self.entities.append(  Entity( entity ).create( self.vertices, self.variables ) )

        if type( entity ) is str:
            self.append( literal_eval( entity ) )

        if type(entity) is entity:
            self.entities.append( entity )

    def insert( self, entities: str | list | tuple[ list, ... ] ) -> None:
        """
        Fügt eine Liste an Entitäten der Konfiguration hinzu

        :param entities: Liste an Informationen zu Entitäten
        """
        if ( type( entities ) is list ) or ( type( entities ) is tuple  ):
            if type( entities[ 0 ] ) is Entity:
                self.entities += entities

            elif type( entities[ 0 ] ) is list:
                for info in entities: self.append( info )

            else:
                self.append( entities )

        if type( entities ) is str:
            self.insert( literal_eval( entities ) )

    def reset( self ) -> None:
        """
        Entfernt alle bisher hinzugefügten Entitäten
        """
        self.entities.clear()

    def empty( self ) -> bool:
        """
        Prüft, ob die Konfigurationsliste leer ist.

        :return: True, wenn die Liste leer ist
        """
        if len( self.entities ) == 0:
            return True
        return False

    def __len__( self ):
        """
        Gibt die Menge an Entitäten aus

        :return: Länge der Konfigurationsliste
        """
        return len( self.entities )

    def __iter__( self ) -> Iterator[ Entity ]:
        """
        Iterator für die Konfigurationsliste

        :return: Iterator
        """
        self.iter = iter( self.entities )
        return self.iter

    def __next__( self ) -> Entity:
        """
        Inkrementiert den Iterator

        :return: nächste Entität
        """
        return next( self.iter )

    def __getitem__( self, position: int | None = None ) -> Entity | list:
        """
        Getter für eine bestimmte Entität

        :param position: Position in der Konfigurationsliste
        :return: geforderte Entität
        :raise IndexError: falls die Position nicht bekannt ist.
        """

        if position is None:
            return self.entities
        elif position < len( self.entities ):
            return self.entities[ position ]
        else:
            raise IndexError( "Position nicht definiert." )

    def __setitem__(self, position: int, entity: Entity ) -> None:
        """
        Setter für eine bestimmte Position

        :param position: Position in der Konfigurationsliste
        :param entity: zu setzende Entität
        :raise IndexError: falls die Position nicht bekannt ist.
        """

        if position < len( self.entities ):
            self.entities[ position ] = entity
        else:
            raise IndexError( "Position nicht definiert." )

    def __str__( self ) -> str:
        """
        Gibt die Konfigurationsliste als string zurück, wobei Variablen an den Anfang gesetzt werden.

        :return: Entitäten-Infos als string
        """
        string_repr: str = ""

        if len( self.variables ) > 0:
            for var in self.variables:
                info = [ 'var', {'name': var, 'value': self.variables[ var ] } ]
                if len( string_repr ) == 0:
                    string_repr += str(info)
                else:
                    string_repr += ",\n" + str(info)

        if self.__len__() > 0:
            for feature in self.entities:
                if len( string_repr ) == 0:
                    string_repr += str( feature )
                else:
                    string_repr += ",\n" + str( feature )

        return string_repr

from latticegeometrylib.Generator import LatticeGenerator
from cadquery import Workplane, exporters
import datetime
import xlwt

nProcesses: int = 5  # Anzahl an Prozessen zur Mittelung der Rechenzeit

length: float = 2.  # Kantenlänge der kubischen Elementarzelle

strut_diameter: float = 0.4  # Strebendurchmesser

shell_thickness: float = 1.0  # Wandstärke der Schalengeometrie

box_size: float = 20.  # Kantenlänge der Box, welche mit Gitter gefüllt wird

# Liste für Zellkonfiguration des Typs BCC
bcc = [ [ 1, 7, { 'diameter': strut_diameter } ], [ 4, 8, { 'diameter': strut_diameter } ],
        [ 3, 5, { 'diameter': strut_diameter } ], [ 2, 6, { 'diameter': strut_diameter } ] ]

# Liste für Zellkonfiguration des Typs FCC
fcc = [ [4, 7, {'diameter': strut_diameter }], [3, 6, {'diameter': strut_diameter }],
        [3, 8, {'diameter': strut_diameter }], [1, 8, {'diameter': strut_diameter }],
        [1, 6, {'diameter': strut_diameter }], [8, 6, {'diameter': strut_diameter }],
        [5, 7, {'diameter': strut_diameter }], [5, 4, {'diameter': strut_diameter }],
        [5, 2, {'diameter': strut_diameter }], [7, 2, {'diameter': strut_diameter }],
        [4, 2, {'diameter': strut_diameter }], [1, 3, {'diameter': strut_diameter }] ]

# Liste für Zellkonfiguration des Typs Octet
octet = [ [4, 7, {'diameter': strut_diameter }], [3, 6, {'diameter': strut_diameter }],
          [3, 8, {'diameter': strut_diameter }], [1, 8, {'diameter': strut_diameter }],
          [1, 6, {'diameter': strut_diameter }], [8, 6, {'diameter': strut_diameter }],
          [5, 7, {'diameter': strut_diameter }], [5, 4, {'diameter': strut_diameter }],
          [5, 2, {'diameter': strut_diameter }], [7, 2, {'diameter': strut_diameter }],
          [4, 2, {'diameter': strut_diameter }], [1, 3, {'diameter': strut_diameter }],
          [(4,5), (5,7), {'diameter': strut_diameter }], [(4,5), (1,8), {'diameter': strut_diameter }],
          [(4,5), (1,3), {'diameter': strut_diameter }], [(4,5), (6,3), {'diameter': strut_diameter }],
          [(3,8), (6,3), {'diameter': strut_diameter }], [(3,8), (1,3), {'diameter': strut_diameter }],
          [(3,8), (1,8), {'diameter': strut_diameter }], [(3,8), (5,7), {'diameter': strut_diameter }],
          [(1,8), (5,7), {'diameter': strut_diameter }], [(1,8), (1,3), {'diameter': strut_diameter }],
          [(3,6), (5,7), {'diameter': strut_diameter }], [(3,6), (1,3), {'diameter': strut_diameter }] ]

templates = [ bcc, fcc, octet ]

timesGrid: list = ["Zeit zur Erstellung des Gitters in s"]  # Liste für gemessene Zeiten

timesIntersect: list = ["Zeit zur Überschneidung des Gitters in s"]  # Liste für gemessene Zeiten

timesUnify: list = ["Zeit zur Verschmelzung in s"]  # Liste für gemessene Zeiten

nObjects: list = ["Anzahl der Streben pro Zelle", len( bcc ), len( fcc ), len( octet ) ]  # Liste Anzahl der Streben

for template in templates:
    timeLattice: float = 0.
    timeIntersect: float = 0.
    timeUnify: float = 0.

    for i in range( nProcesses ):
        generator = LatticeGenerator()
        generator.set_initial_model( Workplane().box( box_size, box_size, box_size ) )
        generator.create_shell( shell_thickness )
        generator.init_unitary_cell( ( length, length, length ), ( True, True, True ) )
        generator.add_entities( template )
        generator.create_unitary_cell()

        start = datetime.datetime.now()
        generator.create_lattice()
        stop = datetime.datetime.now()
        timeLattice += ( stop - start ).total_seconds() / nProcesses

        start = datetime.datetime.now()
        generator.intersect_lattice()
        stop = datetime.datetime.now()
        timeIntersect += ( stop - start ).total_seconds() / nProcesses

        start = datetime.datetime.now()
        generator.unify()
        stop = datetime.datetime.now()
        timeUnify += ( stop - start ).total_seconds() / nProcesses

        del generator

    timesGrid.append( timeLattice )
    timesIntersect.append( timeIntersect )
    timesUnify.append( timeUnify )

# Export der Zeiten in Excel-Sheet
m = xlwt.Workbook( encoding = "utf-8" )
s = m.add_sheet( "Rechenzeit_Zellkomplexität" )

for i in range( len( nObjects ) ):
    s.write( i, 0, nObjects[ i ] )
    s.write( i, 1, timesGrid[ i ] )
    s.write( i, 2, timesIntersect[ i ] )
    s.write( i, 3, timesUnify[ i ] )

m.save( "cellcomplexity_calctime.xls" )

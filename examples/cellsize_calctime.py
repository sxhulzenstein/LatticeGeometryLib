from latticegeometrylib.Generator import LatticeGenerator
import datetime
import xlwt
from cadquery import Workplane

nProcesses = 5  # Anzahl an Prozessen zur Mittelung der Rechenzeit

box_size: float = 20.  # Kantenlänge der Box, welche mit Gitter gefüllt wird

# Kantenlängen der kubischen Elementarzelle
lengths: list[ float ] = [ 20., 10., 5., 2. ]

# Anzahl der Zellen
nCells: list[ str ] = [ str( int( box_size / length ) ) for length in lengths ]

rel: float = 1. / 5.  # Verhältnis des Strebendurchmessers zur Kantenlänge der Zelle

shell_thickness: float = 1.0  # Wandstärke der Schalengeometrie

# Vorlage für Zellkonfiguration
def bcc( d: float ):
    return [
        [1, 7, {'diameter': d}],
        [4, 8, {'diameter': d}],
        [3, 5, {'diameter': d}],
        [2, 6, {'diameter': d}]
    ]

timesGrid: list = [ "Zeit zur Erstellung des Gitters in s" ]  # Liste für gemessene Zeiten

timesIntersect: list = [ "Zeit zur Überschneidung des Gitters in s" ]  # Liste für gemessene Zeiten

timesUnify: list = [ "Zeit zur Verschmelzung in s" ]  # Liste für gemessene Zeiten

nObjects: list[ str ] = [ "Anzahl der Zellen" ] + nCells  # Anzahl der Elementarzellen

for length in lengths:
    timeLattice: float = 0.
    timeIntersect: float = 0.
    timeUnify: float = 0.

    for i in range( nProcesses ):
        generator = LatticeGenerator()
        generator.set_initial_model( Workplane().box( box_size, box_size, box_size ) )
        generator.create_shell( shell_thickness )
        generator.init_unitary_cell( ( length, length, length ), ( True, True, True ) )
        strut_diameter = rel * length
        generator.add_entities( bcc( strut_diameter ) )
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

    timesGrid.append( timeLattice / nProcesses )
    timesIntersect.append( timeIntersect / nProcesses )
    timesUnify.append( timeUnify / nProcesses )

# Export der Zeiten in Excel-Sheet
m = xlwt.Workbook( encoding="utf-8" )
s = m.add_sheet( "Rechenzeit_Zellgröße" )

for i in range( len( nObjects ) ):
    s.write( i, 0, nObjects[ i ] )
    s.write( i, 1, timesGrid[ i ] )
    s.write( i, 2, timesIntersect[ i ] )
    s.write( i, 3, timesUnify[ i ] )

m.save( "cellsize_calctime.xls" )

from cadquery import Workplane
import datetime
import xlwt

r = 1.0
nObjects = [10, 100, 1000, 10000]
times = [ "Rechenzeit in s" ]
nProcesses = 5
combine = False

def centers( nObjects ) -> list[ tuple[ float, float ] ]:
    return [ ( i * r, 0.) for i in range( nObjects ) ]


def createCylinders( c ) -> Workplane:
    cylinder = Workplane( "XY" ).cylinder( radius = r, height = r )
    return Workplane( "XY" ).pushPoints( c ).eachpoint(
        lambda p: cylinder.val().located( p ), combine = combine )


def benchmark():
    for n in nObjects:
        c = centers( n )
        timeInSeconds = 0

        for i in range( nProcesses ):
            begin = datetime.datetime.now()
            createCylinders( c )
            end = datetime.datetime.now()
            timeInSeconds += ( end - begin ).total_seconds() / nProcesses

        times.append( str( timeInSeconds ) )

    nObjects.insert( 0, "Anzahl der Objekte" )

    m = xlwt.Workbook( encoding="utf-8" )
    s = m.add_sheet( "benchmark" )
    for i in range( len( nObjects ) ):
        s.write( i, 0, nObjects[ i ] )
        s.write( i, 1, times[ i ] )

    m.save( "primitive_cadquery_calctime.xls" )

benchmark()


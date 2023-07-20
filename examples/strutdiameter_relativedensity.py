from cadquery import Workplane
from latticegeometrylib.Generator import LatticeGenerator
import math
import xlwt

# Kantenlänge der Elementarzelle
l: float = 10.

# Abschätzung re. Dichte für BCC Typ
def density_bcc( d: float ) -> float:
    return ( math.pi / 4. ) * ( ( d ** 2. ) / ( l ** 2. ) ) * ( 4. * math.sqrt( 3. ) )

# Abschätzung re. Dichte für FCC Typ
def density_fcc( d: float ) -> float:
    return ( math.pi / 4. ) * ( ( d ** 2. ) / ( l ** 2. ) ) * ( 6. * math.sqrt( 2. ) )

# Vorlage für BCC Typ
def bcc( d ):
    return [
        [ 1, 7, { 'diameter': d } ],
        [ 4, 8, { 'diameter': d } ],
        [ 3, 5, { 'diameter': d } ],
        [ 2, 6, { 'diameter': d } ]
        ]

# Vorlage für FCC Typ
def fcc(d):
    return [
        [4, 7, {'diameter': d }],
        [3, 6, {'diameter': d }],
        [3, 8, {'diameter': d }],
        [1, 8, {'diameter': d }],
        [1, 6, {'diameter': d }],
        [8, 6, {'diameter': d }],
        [5, 7, {'diameter': d }],
        [5, 4, {'diameter': d }],
        [5, 2, {'diameter': d }],
        [7, 2, {'diameter': d }],
        [4, 2, {'diameter': d }],
        [1, 3, {'diameter': d }]
    ]


diameter_length_ratio = [ "d / l" ]  # Verhältnisse d / l

# rel. Dichte BCC abgeschätzt
density_bcc_analytical: list = [ "Näherung BCC analytisch" ]

# rel. Dichte BCC, gewonnen über CAD-Objekt
density_bcc_cad: list = [ "Näherung BCC CAD" ]

# rel. Dichte FCC abgeschätzt
density_fcc_analytical: list = [ "Näherung FCC analytisch" ]

# rel. Dichte FCC, gewonnen über CAD-Objekt
density_fcc_cad: list = [ "Näherung FCC CAD" ]

for i in range( 100 ):
    d = ( i + 1 ) / 100 * l
    diameter_length_ratio.append( d / l )
    genBCC = LatticeGenerator()
    genBCC.set_initial_model( Workplane().box( l, l, l ) )
    genBCC.init_unitary_cell( ( l, l, l ), ( True, True, True ) )
    genBCC.add_entities( bcc( d ) )
    genBCC.create_unitary_cell()
    density_bcc_analytical.append( min( 1., density_bcc( d ) ) )
    density_bcc_cad.append( genBCC.cell.density() )

    genFCC = LatticeGenerator()
    genFCC.set_initial_model( Workplane().box( l, l, l ) )
    genFCC.init_unitary_cell( ( l ,l ,l ), ( True, True, True ) )
    genFCC.add_entities( fcc( d ) )
    genFCC.create_unitary_cell()
    density_fcc_analytical.append( min( 1., density_fcc( d ) ) )
    density_fcc_cad.append( genFCC.cell.density() )

m = xlwt.Workbook( encoding = "utf-8" )
s = m.add_sheet( "Relative_Dichte" )

# Export der Daten in Excel-Sheet
for i in range( len( diameter_length_ratio ) ):
    s.write( i + 1, 0, diameter_length_ratio[ i ] )
    s.write( i + 1, 1, density_bcc_analytical[ i ] )
    s.write( i + 1, 2, density_bcc_cad[ i ] )
    s.write( i + 1, 3, density_fcc_analytical[ i ] )
    s.write( i + 1, 4, density_fcc_cad[ i ] )

m.save( "strutdiameter_relativedensity.xls" )
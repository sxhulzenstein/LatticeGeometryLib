from latticegeometrylib.Generator import LatticeGenerator
from cadquery import Workplane, exporters

nEx, nEy, nEz = (4,4, 5)
lE = 5.
dS = 1.
cell_type = 'FCC'
pin_height = 7.

bcc = [ [ 1, 7, { 'diameter': dS } ], [ 4, 8, { 'diameter': dS } ],
        [ 3, 5, { 'diameter': dS } ], [ 2, 6, { 'diameter': dS } ] ]

# Liste für Zellkonfiguration des Typs FCC
fcc = [ [4, 7, {'diameter': dS }], [3, 6, {'diameter': dS }],
        [3, 8, {'diameter': dS }], [1, 8, {'diameter': dS }],
        [1, 6, {'diameter': dS }], [8, 6, {'diameter': dS }],
        [5, 7, {'diameter': dS }], [5, 4, {'diameter': dS }],
        [5, 2, {'diameter': dS }], [7, 2, {'diameter': dS }],
        [4, 2, {'diameter': dS }], [1, 3, {'diameter': dS }] ]


generator = LatticeGenerator()

generator.set_initial_model(
    Workplane( "XY" ).box( nEx * lE, nEy * lE, nEz * lE ) )

generator.init_unitary_cell( ( lE, lE, lE ), ( True, True, True ) )

generator.add_entities( fcc )

generator.create_unitary_cell()

generator.create_lattice()

lattice = generator.get_lattice()

pin = Workplane( "XY" ).circle( 2.0 ).workplane(
        offset= 2. ).circle( 3.0 ).workplane(
        offset=1. ).circle( 1.0 ).workplane(
    offset=pin_height-5.).circle( 1.0 ).workplane(
    offset=2. ).circle(0.5).loft( True )

p = [ ( x * lE - ( nEx * lE ) / 2., y * lE - ( nEy * lE ) / 2. , - pin_height - ( nEz * lE ) / 2.)
      for x in range( nEx + 1 ) for y in range( nEy + 1 ) ]

lattice = lattice.union(Workplane().pushPoints(p).eachpoint( lambda loc: pin.val().located( loc ) ), clean=False)

exporters.export( lattice, f"relative_density_specimen_FDM_{cell_type}.STL" )

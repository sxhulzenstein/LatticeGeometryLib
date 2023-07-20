from cadquery import Workplane, Location, exporters
from latticegeometrylib.Generator import LatticeGenerator

cube_length = 30.
plate_height = 25.
strut_diameter = 1.
cell_type = 'BCC'
cell_size = 5.0
nCells = int( cube_length / cell_size )

cube = Workplane().box( cube_length, cube_length, cube_length )
generator = LatticeGenerator()
generator.set_initial_model( cube )
generator.init_unitary_cell( ( cell_size, cell_size, cell_size ), (True, True, True) )

#body centered cell type
generator.add_entities( [ [ 1, 7, { 'diameter': strut_diameter } ],
                          [ 4, 8, { 'diameter': strut_diameter } ],
                          [ 3, 5, { 'diameter': strut_diameter } ],
                          [ 2, 6, { 'diameter': strut_diameter } ] ] )

generator.create_unitary_cell()

generator.create_lattice()

lattice = generator.get_lattice()

p = [ ( 0., 0., -( cube_length + plate_height  ) / 2 ) ]

pos = [ ( ( cell_size - cube_length ) / 2 + x * cell_size, ( cell_size - cube_length ) / 2 + y * cell_size )
        for x in range( nCells ) for y in range( nCells ) ]

additional_box = Workplane( 'XY' ).box( cube_length, cube_length, plate_height )

additional_box = additional_box.union( additional_box.mirror().val().located(
    Location( ( 0., 0., cube_length + plate_height) ) ) )

lattice = lattice.union( Workplane().pushPoints( p ).eachpoint(
    lambda loc: additional_box.val().located( loc ), combine = False ), clean = False )

exporters.export( lattice, f"compressiontest_specimen_fdm_{cell_type}.STL" )

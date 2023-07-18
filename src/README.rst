==================
LatticeGeometryLib
==================

Description
===========

LatticeGeometryLib is a python library for creating spacial lattice structures which
consist of an interconnected network of nodes struts and plates. These individual entities
are combined into a unitary cell which periodic repetition creates the lattice. Furthermore
this lattice can be inserted into any shell-like CAD geometry. This library is based on the CADQuery library.

.. image:: https://github.com/sxhulzenstein/LatticeGeometryLib/raw/main/src/images/latticegeometrylib.png
    :height: 500

Requirements
============

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Package
     - Version
   * - cadquery
     - 2.2.0

Installation
============

Embedding the library into your python code is just as easy as for any other library
Just call the following command from your python terminal::

    pip install latticegeometrylib

Usage
=====

Example ::

    from latticegeometrylib.Generator import LatticeGenerator

    # create a new generator for the lattice
    generator = LatticeGenerator()

    # import a geometry as STEP-file
    # cylinder has a height and radius of 10.
    generator.import_initial_model( "cylinder.STEP" )

    # create a shell object from geometry
    # thickness of wall is set to 1.0
    generator.create_shell( 1.0 )

    # define the sizes of the unit cell in every spacial direction
    size = ( 2., 2., 2. )

    # state, if the measurements shall be set exactly as given
    strict = ( True, True, True )

    # initialize unitary cell
    generator.init_unitary_cell( size, strict )

    # define the strut diameter
    d = 0.25

    # add entities to the cell, which are defined by node ids of the unit cell (cell type is called BCC here)
    generator.add_entity( [ 1, 7, { 'diameter': d } ] )
    generator.add_entity( [ 2, 6, { 'diameter': d } ] )
    generator.add_entity( [ 3, 5, { 'diameter': d } ] )
    generator.add_entity( [ 4, 8, { 'diameter': d } ] )

    # create unitary cell object from given entities
    generator.create_unitary_cell()

    # create lattice from given unit cell
    generator.create_lattice()

    # create intersection of lattice and shell
    generator.intersect_lattice()

    # merge shell and intersected lattice
    generator.unify()

    # export the shell with lattice core
    generator.export_unified( "cylinder_with_lattice.STEP" )

Additional Remarks
==================
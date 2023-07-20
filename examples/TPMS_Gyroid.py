from cadquery import Workplane, Plane, Location
import math

L = math.pi
nx = 2
ny = 2
nz = 2

def function( x: float ) -> tuple[ float, float ]:
    return x, math.atan(-math.sin(x-L/2))

systems = [
    ((L/2, L, 0.), (0.,0.,-1.), (1.,0.,0.)),
    ((L/2, 0, L), (0.,0.,1.), (1.,0.,0.)),
    ((L, 0, L/2), (0.,-1.,0.), (0.,0.,1.)),
    ((0, L, L/2), (0.,1.,0.), (0.,0.,1.)),
    ((L, L/2, 0), (1.,0.,0.), (0.,1.,0.)),
    ((0, L/2, L), (-1.,0.,0.), (0.,1.,0.))
    ]

wires = []

for  o, n, x in systems:
    plane = Plane(origin = o, normal = n, xDir = x )
    wires.append( Workplane( plane ).parametricCurve(function, start= -L/2, stop=L/2).val())

cell = Workplane('XY').interpPlate(wires, thickness=0.1)

o = (0.,0.,0.)
xAxis = (1.0,0.0,0.0)
yAxis = (0.0,1.0,0.0)
zAxis = (0.0,0.0,1.0)

unit = cell

cell = cell.union(
    unit.rotate(o,xAxis,0).rotate(o,yAxis,0).rotate(o,zAxis,180).val().located(
        Location((0,L,0))))

cell = cell.union(
    unit.rotate(o,xAxis,180).rotate(o,yAxis,0).rotate(o,zAxis,180).val().located(
        Location((0,-L,L))))

cell = cell.union(
    unit.rotate(o,xAxis,90).rotate(o,yAxis,90).rotate(o,zAxis,0).val().located(
        Location((0,0,L))))

cell = cell.union(
    unit.rotate(o,xAxis,0).rotate(o,yAxis,0).rotate(o,zAxis,0).val().located(
        Location((-L,-L,-L))))

cell = cell.union(
    unit.rotate(o,xAxis,180).rotate(o,yAxis,90).rotate(o,zAxis,90).val().located(
        Location((-L,L,0))))

cell = cell.union(
    unit.rotate(o,xAxis,270).rotate(o,yAxis,270).rotate(o,zAxis,180).val().located(
        Location((L,0,-L))))

cell = cell.union(
    unit.rotate(o,xAxis,270).rotate(o,yAxis,90).rotate(o,zAxis,0).val().located(
        Location((L,0,0))))

p = [( x * 2*L, y*2*L, z*2*L)
     for x in range(nx) for y in range(ny) for z in range(nz)]

grid = Workplane().pushPoints(p).eachpoint(
    lambda loc: cell.val().located(loc), combine=False)

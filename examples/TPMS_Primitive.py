from cadquery import Plane, Workplane, Location
import math

L = math.pi
nx = 2
ny = 2
nz = 2

def fun( x: float ) -> tuple[float, float]:
    return x, math.acos(-math.cos(x)-1)

systems = [
    ((0., 0., 0.), (1.,0.,0.), (0.,1.,0.)),
    ((0., 0., 0.), (0.,-1.,0.), (1.,0.,0.)),
    ((0., 0., 0.), (0.,0.,1.), (1.,0.,0.)),
    ((L, L, L), (1,0.,0.), (0,-1.,0.)),
    ((L, L, L), (0,1.,0.), (0,0.,-1.)),
    ((L, L, L), (0,0.,1.), (-1,0.,0.))
    ]

wires = []

for  o, n, x in systems:
    plane = Plane(origin = o, normal = n, xDir = x )
    wires.append(
        Workplane( plane ).parametricCurve(fun, start= L/2, stop=L).val())

cell = Workplane('XY').interpPlate(wires, thickness=0.1)

o = (0.,0.,0.)
xAxis = (1.0,0.0,0.0)
yAxis = (0.0,1.0,0.0)
zAxis = (0.0,0.0,1.0)

unit = cell

cell = cell.union(unit.rotate(o,xAxis,90).rotate(o,yAxis,0).rotate(o,zAxis,0))

cell = cell.union(unit.rotate(o,xAxis,180).rotate(o,yAxis,0).rotate(o,zAxis,0))

cell = cell.union(unit.rotate(o,xAxis,270).rotate(o,yAxis,0).rotate(o,zAxis,0))

cell = cell.union(cell.mirror('YZ'))

p = [( x * 2*L, y*2*L, z*2*L)
     for x in range(nx) for y in range(ny) for z in range(nz)]

grid = Workplane().pushPoints(p).eachpoint(
    lambda loc: cell.val().located(loc), combine=False)
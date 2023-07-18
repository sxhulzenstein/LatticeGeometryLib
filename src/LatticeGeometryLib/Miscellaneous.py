
from stl.mesh import Mesh
from cqmore import Workplane
import cadquery as cq
from typing import (Tuple, List, Any, AnyStr, Union)


def boundingBox(model: cq.Workplane) -> List[ List[ float ]]:

    bbInfo = model.val().BoundingBox()

    return [ [bbInfo.xmin, bbInfo.ymin, bbInfo.zmin],
             [bbInfo.xmax, bbInfo.ymax, bbInfo.zmax],
             [bbInfo.xlen, bbInfo.ylen, bbInfo.zlen] ]


class Size:
    def __init__( self, dx: float = 0, dy: float = 0, dz: float = 0 ):
        self.dx: float = dx
        self.dy: float = dy
        self.dz: float = dz

    def toTuple(self) -> Tuple[float, float, float]:
        return self.dx, self.dy, self.dz

    def toList(self) -> List[float]:
        return [self.dx, self.dy, self.dz]

    def __str__(self) -> AnyStr:
        return str(self.toList())

    def __getitem__(self, component: int ) -> float:
        if component == 0:
            return self.dx
        elif component == 1:
            return self.dy
        elif component == 2:
            return self.dz
        else:
            raise IndexError

    def __setitem__( self, component, value ) -> None:
        if component == 0:
            self.dx = value
        elif component == 1:
            self.dy = value
        elif component == 2:
            self.dz = value
        else:
            raise IndexError

    def __len__(self) -> int:
        return 3

    def __eq__(self, other) -> bool:
        return self.dx == other.dx and self.dy == other.dy and self.dz == other.dz


class BoundingBox:
    def __init__( self, model: cq.Workplane ) -> None:
        self.box: cq.BoundBox = model.val().BoundingBox()
        self.xmin = self.box.xmin
        self.ymin = self.box.ymin
        self.zmin = self.box.zmin

        self.xmax = self.box.xmax
        self.ymax = self.box.ymax
        self.zmax = self.box.zmax

        self.xlen = self.box.xlen
        self.ylen = self.box.ylen
        self.zlen = self.box.zlen

    def extend(self, direction: Union[ str, int ], value: float ) -> None:
        if direction == 'x' or direction == 0:
            self.xmin, self.xmax, self.xlen = ( self.xmin - value / 2., self.xmax + value / 2., self.xlen + value )
        elif direction == 'y' or direction == 1:
            self.ymin, self.ymax, self.ylen = ( self.ymin - value / 2., self.ymax + value / 2., self.ylen + value )
        elif direction == 'z' or direction == 2:
            self.zmin, self.zmax, self.zlen = (self.zmin - value / 2., self.zmax + value / 2., self.zlen + value)
        else:
            raise IndexError

    def min(self, direction: Union[ str, int, None ] = None ) -> Union[ float, Tuple[ float, ... ] ]:
        if direction == 'x' or direction == 0:
            return self.xmin
        elif direction == 'y' or direction == 1:
            return self.ymin
        elif direction == 'z' or direction == 2:
            return self.zmin
        elif direction is None:
            return self.xmin, self.ymin, self.zmin
        else:
            raise IndexError

    def max(self, direction: Union[ str, int, None] = None ) -> Union[ float, Tuple[ float, ... ] ]:
        if direction == 'x' or direction == 0:
            return self.xmax
        elif direction == 'y' or direction == 1:
            return self.ymax
        elif direction == 'z' or direction == 2:
            return self.zmax
        elif direction is None:
            return self.xmax, self.ymax, self.zmax
        else:
            raise IndexError

    def length(self, direction: Union[ str, int, None ] = None ) -> Union[ float, Tuple[ float, ... ] ]:
        if direction == 'x' or direction == 0:
            return self.xlen
        elif direction == 'y' or direction == 1:
            return self.ylen
        elif direction == 'z' or direction == 2:
            return self.zlen
        elif direction is None:
            return self.xlen, self.ylen, self.zlen
        else:
            raise IndexError


class Switch:
    def __init__( self, x: bool = True, y: bool = True, z: bool = True ):
        self.x = x
        self.y = y
        self.z = z

    def toTuple( self ) -> tuple[ float, float, float ]:
        return self.x, self.y, self.z

    def toList( self ) -> list[ float ]:
        return [ self.x, self.y, self.z ]

    def __str__( self ) -> str:
        return str( self.toList() )

    def __getitem__( self, component: int ) -> float:
        if component == 0:
            return self.x
        elif component == 1:
            return self.y
        elif component == 2:
            return self.z
        else:
            raise IndexError( "Index außerhalb des Intervalls." )

    def __setitem__( self, component: int, value: bool ) -> None:
        if component == 0:
            self.x = value
        elif component == 1:
            self.y = value
        elif component == 2:
            self.z = value
        else:
            raise IndexError( "Index außerhalb des Intervalls." )

    def __len__( self ) -> int:
        return 3


class Periodicity:
    def __init__( self, nx: int = 0, ny: int = 0, nz: int = 0 ):
        self.nx = nx
        self.ny = ny
        self.nz = nz

    def toTuple(self) -> Tuple[float, float, float]:
        return self.nx, self.ny, self.nz

    def toList(self) -> List[float]:
        return [self.nx, self.ny, self.nz]

    def __str__(self) -> AnyStr:
        return str(self.toList())

    def __getitem__(self, component: int) -> float:
        if component == 0:
            return self.nx
        elif component == 1:
                return self.ny
        elif component == 2:
            return self.nz
        else:
            raise IndexError

    def __setitem__(self, component, value) -> None:
        if component == 0:
            self.nx = value
        elif component == 1:
            self.ny = value
        elif component == 2:
            self.nz = value
        else:
            raise IndexError

    def __len__(self) -> int:
        return 3
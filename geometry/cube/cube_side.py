from functools import partial
from operator import imul

from kivy.graphics.vertex_instructions import Quad

from geometry.helpers import make_flat
from geometry.cube.enums import SIDE


class CubeSide:
    DRAWING_RATIO = 10

    def __init__(self, side,  corners):
        self.corners = corners
        self.side = side
        self.drawn = None

        self.multiply_by_ratio = partial(imul, self.DRAWING_RATIO)

    def get_edge_length(self):
        assert self.side in [SIDE.FRONT, SIDE.BACK], 'Only front and back sides are 100% valid for this'
        return self.corners[1].y - self.corners[0].y

    def get_coords(self, multiplied_by_ratio=True, flatten=True):
        coords = [
            corner.coords() if not multiplied_by_ratio
            else map(self.multiply_by_ratio, corner.coords())
            for corner
            in self.corners
        ]

        # if True - return list with 8 elements
        # otherwise returns list with 4 tuples each having 2 int elemt
        if flatten:
            coords = make_flat(coords)

        return coords

    def draw(self, texture=None):
        assert self.drawn is None, 'Trying to draw already drawn figure'

        self.drawn = Quad(
            points=self.get_coords(),
            texture=texture,
        )

        return self.drawn

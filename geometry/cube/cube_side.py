from typing import List, Tuple
from functools import partial
from operator import imul

from kivy.graphics.vertex_instructions import Quad
from kivy.animation import Animation

from geometry.helpers import make_flat
from geometry.cube.enums import SIDE
from geometry.constants import CUBE_SIZE


class CubeSide:
    DRAWING_RATIO = 10

    def __init__(self, side: SIDE,  corners):
        self.corners = corners
        self.side = side
        self.drawn = None

    def draw(self, texture=None):
        assert self.drawn is None, 'Trying to draw already drawn figure'

        self.drawn = Quad(points=self.get_coords(), texture=texture)

        return self.drawn

    def is_pos_inside(self, pos):
        if pos.x > self.corners[0].x * CUBE_SIZE and pos.y > self.corners[0].y * CUBE_SIZE:
            if pos.x < self.corners[2].x * CUBE_SIZE and pos.y < self.corners[2].y * CUBE_SIZE:
                return True

        return False

    def transform(self):
        # transform touched side
        initial_coord_values = self.get_coords()

        modified_coord_values = [
            coord - 15
            if idx in [0, 1, 2, 7]
            else coord + 15
            for idx, coord in enumerate(initial_coord_values)
        ]

        anim = Animation(points=modified_coord_values, duration=0.4, transition='out_back')

        anim += Animation(points=initial_coord_values, duration=0.4, transition='in_back')
        anim.start(self.drawn)

    def get_coords(self) -> List[int]:
        """
            make list of coords tuples ---------> [(x1, y1), (x2, y2), ...]
            make it flat -----------------------> [x1, y1, x2, y2, ...]
            multiply each element by ratio -----> [x1 * RATIO, y1 * RATIO, x2 * RATIO, y2 * RATIO, ...]
            return
        """

        return list(map(partial(imul, self.DRAWING_RATIO),  make_flat([corner.coords() for corner in self.corners])))

from dataclasses import dataclass
from enum import IntEnum
from functools import partial
from operator import imul
from typing import Tuple, Iterable

from kivy.graphics.vertex_instructions import Quad

from calculations.pos import Pos


class SIDE(IntEnum):
    FRONT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
    BACK = 5


@dataclass
class CubeSide:
    side: SIDE
    corners: Iterable[Pos]

    def get_edge_length(self):
        assert self.side in [SIDE.FRONT, SIDE.BACK], 'Only front and back sides are 100% valid for this'
        return self.corners[1].y - self.corners[0].y

    def get_coords(self):
        coords = []
        for corner in self.corners:
            coords.extend(corner.coords())

        return coords

    def draw(self, ratio=10, texture=None):
        mul_func = partial(imul, ratio)

        return Quad(points=map(mul_func, self.get_coords()), texture=texture)


class Cube:
    SIDES_DRAWING_ORDER = [SIDE.RIGHT, SIDE.FRONT, SIDE.TOP]

    def __init__(self, front_bottom_left: Pos, size: int):  #, front_bottom_left: Pos, front_top_left: Pos, front_top_right: Pos, front_bottom_right: Pos):
        self.size = size

        self.sides = {}
        self.sides[SIDE.FRONT] = self._calc_front_side(front_bottom_left)  # Calculation order is important
        self.sides[SIDE.BACK] = self._calc_back_side()
        self.sides[SIDE.TOP] = self._calc_top_side()
        self.sides[SIDE.RIGHT] = self._calc_right_side()

    @staticmethod
    def _front_side_coords_calculate(bottom_left_corner: Pos, size: int):
        pos_dicts = {
            'front_bottom_left': bottom_left_corner,
            'front_top_left': bottom_left_corner.get_transformed_pos(0, size),
            'front_top_right': bottom_left_corner.get_transformed_pos(size, size),
            'front_bottom_right': bottom_left_corner.get_transformed_pos(size, 0),
        }
        return pos_dicts

    def _calc_front_side(self, bottom_left_corner) -> CubeSide:
        pos_dict = self._front_side_coords_calculate(bottom_left_corner, self.size)

        return CubeSide(
            side=SIDE.FRONT,
            corners=tuple(pos_dict.values()),
        )

    def _calc_back_side(self) -> CubeSide:
        back_side = CubeSide(
            side=SIDE.BACK,
            corners=tuple(
                corner.get_transformed_pos(
                    transform_x=self.size/2,
                    transform_y=self.size/2,
                )
                for corner in self.sides[SIDE.FRONT].corners
            ),
        )

        return back_side

    def _calc_top_side(self) -> CubeSide:
        # Invalid drawing if wrong order!
        front_top_edge = self.sides[SIDE.FRONT].corners[1], self.sides[SIDE.FRONT].corners[2]
        back_top_edge = self.sides[SIDE.BACK].corners[2], self.sides[SIDE.BACK].corners[1]

        top_side = CubeSide(
            side=SIDE.TOP,
            corners=front_top_edge + back_top_edge,
        )

        return top_side

    def _calc_right_side(self) -> CubeSide:
        # Invalid drawing if wrong order!
        front_right_edge = self.sides[SIDE.FRONT].corners[2], self.sides[SIDE.FRONT].corners[3]
        back_right_edge = self.sides[SIDE.BACK].corners[3], self.sides[SIDE.BACK].corners[2]

        right_side = CubeSide(
            side=SIDE.RIGHT,
            corners=front_right_edge + back_right_edge,
        )

        return right_side

from typing import Dict, List, Tuple

from geometry.cube.cube_side import CubeSide
from geometry.point import Point
from geometry.cube.enums import SPATIAL_DIRECTION
from geometry.helpers import calc_square_corners


class Cube:
    SIDES_CALCULATION_ORDER = [
        SPATIAL_DIRECTION.FRONT,  # front and back sides should be calculated first; next order may be any
        SPATIAL_DIRECTION.BACK,
        SPATIAL_DIRECTION.TOP,
        SPATIAL_DIRECTION.RIGHT,
    ]

    SIDES_DRAWING_ORDER = [
        SPATIAL_DIRECTION.TOP,
        SPATIAL_DIRECTION.RIGHT,
        SPATIAL_DIRECTION.FRONT,
    ]

    def __init__(self, front_side_initial_point: Point, size: int):
        self.size = size

        # only FRONT and BACK sides initial points stored because all other sides
        # can be calculated just by choosing corresponding corners of FRONT and BACK sides;
        back_side_initial_point = front_side_initial_point.apply_delta(delta_x=self.size / 2, delta_y=self.size / 2)

        self.sides_initial_points = {
            SPATIAL_DIRECTION.FRONT: front_side_initial_point,
            SPATIAL_DIRECTION.BACK: back_side_initial_point,
        }

        self.sides = {}
        for side_name in self.SIDES_CALCULATION_ORDER:
            self.sides[side_name] = self._calc_side(side_name)

    def __contains__(self, point):
        return any([point in side for side in self.sides.values()])

    @property
    def drawn_sides(self):
        return list(filter(lambda side: side.drawn_quad is not None, self.sides.values()))

    def transform(self):
        for side in self.drawn_sides:
            side.transform()

    def _calc_side(self, side_name: SPATIAL_DIRECTION) -> CubeSide:
        if side_name in [SPATIAL_DIRECTION.FRONT, SPATIAL_DIRECTION.BACK]:
            initial_point = self.sides_initial_points[side_name]
            corners = calc_square_corners(initial_point, self.size)

            return CubeSide(side_name=side_name, corners=corners)

        # just selecting corresponding edges from front and back sides and taking their corners
        # (ex: choose RIGHT edges of FRONT and BACK sides to draw RIGHT side...)
        corners = self.sides[SPATIAL_DIRECTION.FRONT].edges[side_name]
        corners += self.sides[SPATIAL_DIRECTION.BACK].edges[side_name][::-1]  # specific order is necessary for drawing

        return CubeSide(side_name=side_name, corners=corners)

from typing import Dict, List, Tuple

from geometry.cube.cube_side import CubeSide
from geometry.point import Point
from geometry.cube.enums import SPATIAL_DIRECTION
from geometry.helpers import calc_square_corners


class Cube:
    # Drawing order differs from calculation order
    SIDES_DRAWING_ORDER = [SPATIAL_DIRECTION.TOP, SPATIAL_DIRECTION.RIGHT, SPATIAL_DIRECTION.FRONT, ]

    def __init__(self, front_side_initial_point: Point, size: int):
        self.size = size

        # only FRONT and BACK sides initial points stored because all other sides are:
        # 1. not squares;
        # 2. can be calculated just by choosing corresponding corners of FRONT and BACK sides;
        half_size = self.size / 2
        self.sides_initial_points = {
            SPATIAL_DIRECTION.FRONT: front_side_initial_point,
            SPATIAL_DIRECTION.BACK: front_side_initial_point.get_transformed_point(half_size, half_size),
        }

        # Calculation order is important
        self.sides = dict()
        self.sides[SPATIAL_DIRECTION.FRONT] = self._calc_side(SPATIAL_DIRECTION.FRONT)
        self.sides[SPATIAL_DIRECTION.BACK] = self._calc_side(SPATIAL_DIRECTION.BACK)
        self.sides[SPATIAL_DIRECTION.TOP] = self._calc_side(SPATIAL_DIRECTION.TOP)
        self.sides[SPATIAL_DIRECTION.RIGHT] = self._calc_side(SPATIAL_DIRECTION.RIGHT)

    def __contains__(self, point):
        return any([point in side for side in self.sides.values()])

    @property
    def drawn_sides(self):
        return list(filter(lambda side: side.drawn_quad is not None, self.sides.values()))

    def transform(self):
        for side in self.drawn_sides:
            side.transform()

    def _calc_side(self, side_name) -> CubeSide:
        if side_name in [SPATIAL_DIRECTION.FRONT, SPATIAL_DIRECTION.BACK]:
            # front/back sides are equal except initial point
            initial_point = self.sides_initial_points[side_name]
            corners = calc_square_corners(initial_point, self.size)

            return CubeSide(side_name=side_name, corners=corners)

        # after front and back sides calculated remaining sides do not need calculations
        # just selecting corresponding edges from front and back sides and taking their corners
        # (ex: choose RIGHT edges of FRONT and BACK sides to draw RIGHT side...)
        corners = self.sides[SPATIAL_DIRECTION.FRONT].edges[side_name]
        corners += self.sides[SPATIAL_DIRECTION.BACK].edges[side_name][::-1]  # specific order is necessary for drawing

        return CubeSide(side_name=side_name, corners=corners)

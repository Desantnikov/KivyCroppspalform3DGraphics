from typing import Dict

from geometry.cube.cube_side import CubeSide
from geometry.point import Point
from geometry.cube.enums import SIDES, CORNERS


class Cube:
    # Drawing order differs from calculation order
    SIDES_DRAWING_ORDER = [SIDES.TOP, SIDES.RIGHT, SIDES.FRONT, ]

    def __init__(self, front_side_bottom_left_corner_pos: Point, size: int):
        self.size = size
        self.sides = dict()
        self.front_side_bottom_left_corner_pos = front_side_bottom_left_corner_pos

        # Calculation order is important
        self.sides[SIDES.FRONT] = self._calc_front_side()
        self.sides[SIDES.BACK] = self._calc_back_side()
        self.sides[SIDES.TOP] = self._calc_top_side()
        self.sides[SIDES.RIGHT] = self._calc_right_side()

    def __contains__(self, point):
        return any([point in side for side in self.sides])

    @property
    def drawn_sides(self):
        return list(filter(lambda side: side.drawn_quad, self.sides.values()))

    def _calc_front_side(self) -> CubeSide:
        front_side_corners_pos_dict = self._calc_square_corners_pos_dict(self.front_side_bottom_left_corner_pos, self.size)

        front_side_corners_pos = tuple(front_side_corners_pos_dict.values())

        return CubeSide(
            side_name=SIDES.FRONT,
            corners=front_side_corners_pos,
        )

    def _calc_back_side(self) -> CubeSide:
        back_side = CubeSide(
            side_name=SIDES.BACK,
            corners=tuple(
                corner.get_transformed_point(
                    add_to_x=self.size / 2,
                    add_to_y=self.size / 2,
                )
                for corner in self.sides[SIDES.FRONT].corners
            ),
        )

        return back_side

    def _calc_top_side(self) -> CubeSide:
        front_top_edge = self.sides[SIDES.FRONT].corners[1], self.sides[SIDES.FRONT].corners[2]
        back_top_edge = self.sides[SIDES.BACK].corners[2], self.sides[SIDES.BACK].corners[1]

        top_side = CubeSide(
            side_name=SIDES.TOP,
            corners=front_top_edge + back_top_edge,
        )

        return top_side

    def _calc_right_side(self) -> CubeSide:
        front_right_edge = self.sides[SIDES.FRONT].corners[2], self.sides[SIDES.FRONT].corners[3]
        back_right_edge = self.sides[SIDES.BACK].corners[3], self.sides[SIDES.BACK].corners[2]

        right_side = CubeSide(
            side_name=SIDES.RIGHT,
            corners=front_right_edge + back_right_edge,
        )

        return right_side

    @staticmethod
    def _calc_square_corners_pos_dict(bottom_left_corner: Point, size: int) -> Dict[CORNERS, Point]:
        square_corners_pos_dict = {
            CORNERS.LEFT_BOTTOM: bottom_left_corner,
            CORNERS.LEFT_TOP: bottom_left_corner.get_transformed_point(0, size),
            CORNERS.RIGHT_TOP: bottom_left_corner.get_transformed_point(size, size),
            CORNERS.RIGHT_BOTTOM: bottom_left_corner.get_transformed_point(size, 0),
        }

        return square_corners_pos_dict

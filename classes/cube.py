from typing import Dict

from classes.cube_side import CubeSide
from classes.pos import Pos
from enums import SIDE, CORNER


class Cube:
    # Drawing order differs from calculation order
    SIDES_DRAWING_ORDER = [SIDE.TOP, SIDE.RIGHT, SIDE.FRONT, ]

    def __init__(self, front_side_bottom_left_corner_pos: Pos, size: int):
        self.size = size
        self.sides = dict()
        self.front_side_bottom_left_corner_pos = front_side_bottom_left_corner_pos

        # Calculation order is important
        self.sides[SIDE.FRONT] = self._calc_front_side()
        self.sides[SIDE.BACK] = self._calc_back_side()
        self.sides[SIDE.TOP] = self._calc_top_side()
        self.sides[SIDE.RIGHT] = self._calc_right_side()

    def _calc_front_side(self) -> CubeSide:
        front_side_corners_pos_dict = self._calc_square_corners_pos_dict(self.front_side_bottom_left_corner_pos, self.size)

        front_side_corners_pos = tuple(front_side_corners_pos_dict.values())

        return CubeSide(
            side=SIDE.FRONT,
            corners=front_side_corners_pos,
        )

    def _calc_back_side(self) -> CubeSide:
        back_side = CubeSide(
            side=SIDE.BACK,
            corners=tuple(
                corner.get_transformed_pos(
                    add_to_x=self.size / 2,
                    add_to_y=self.size / 2,
                )
                for corner in self.sides[SIDE.FRONT].corners
            ),
        )

        return back_side

    def _calc_top_side(self) -> CubeSide:
        front_top_edge = self.sides[SIDE.FRONT].corners[1], self.sides[SIDE.FRONT].corners[2]
        back_top_edge = self.sides[SIDE.BACK].corners[2], self.sides[SIDE.BACK].corners[1]

        top_side = CubeSide(
            side=SIDE.TOP,
            corners=front_top_edge + back_top_edge,
        )

        return top_side

    def _calc_right_side(self) -> CubeSide:
        front_right_edge = self.sides[SIDE.FRONT].corners[2], self.sides[SIDE.FRONT].corners[3]
        back_right_edge = self.sides[SIDE.BACK].corners[3], self.sides[SIDE.BACK].corners[2]

        right_side = CubeSide(
            side=SIDE.RIGHT,
            corners=front_right_edge + back_right_edge,
        )

        return right_side

    @staticmethod
    def _calc_square_corners_pos_dict(bottom_left_corner: Pos, size: int) -> Dict[CORNER, Pos]:
        square_corners_pos_dict = {
            CORNER.LEFT_BOTTOM: bottom_left_corner,
            CORNER.LEFT_TOP: bottom_left_corner.get_transformed_pos(0, size),
            CORNER.RIGHT_TOP: bottom_left_corner.get_transformed_pos(size, size),
            CORNER.RIGHT_BOTTOM: bottom_left_corner.get_transformed_pos(size, 0),
        }

        return square_corners_pos_dict

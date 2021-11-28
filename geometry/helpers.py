import itertools
from typing import List

from gui.constants import CUBE_SIDES_COLOR_VALUES, BRIGHTNESS_MULTIPLIER
from geometry.constants import SPACES_Y, SPACES_X
from geometry.cube.enums import SPATIAL_DIRECTION


# Misc
def flatten(input_list):
    return list(itertools.chain.from_iterable(input_list))


# Geometry
def calc_square_corners(bottom_left_corner, size):
    square_corners = [
        bottom_left_corner,  # bottom left
        bottom_left_corner.apply_delta(0, size),  # top left
        bottom_left_corner.apply_delta(size, size),  # top right
        bottom_left_corner.apply_delta(size, 0),  # bottom right
    ]

    return square_corners


# Drawing
def get_side_shadow_multiplier(side, plot_idx, row_idx, cube_idx):
    side_shadow_multiplier_map = {
        SPATIAL_DIRECTION.TOP: (plot_idx + plot_idx + plot_idx + cube_idx + row_idx + SPACES_Y + SPACES_X) / 70,
        SPATIAL_DIRECTION.FRONT: (plot_idx + row_idx + cube_idx + row_idx + row_idx + SPACES_Y + SPACES_X) / 70,
        SPATIAL_DIRECTION.RIGHT: (cube_idx + plot_idx + cube_idx + row_idx + cube_idx + SPACES_Y + SPACES_X) / 70,
    }

    return side_shadow_multiplier_map[side]


def adjust_color_brightness(side, shadow_multiplier: float) -> List[float]:
    """
        used to adjust brightness according to shadow miltiplier, which is calculated
        basing on current cube's position and current side
    """

    side_initial_color = CUBE_SIDES_COLOR_VALUES[side]

    overall_multiplier = shadow_multiplier * BRIGHTNESS_MULTIPLIER
    recalculated_color = [color_part * overall_multiplier for color_part in side_initial_color]

    return recalculated_color

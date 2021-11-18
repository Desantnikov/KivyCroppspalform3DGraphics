from typing import List

from kivy.animation import Animation
from kivy.graphics.context_instructions import Color
from kivy.uix.widget import Widget

from geometry.cube.cube import Cube
from geometry.pos import Pos
from geometry.cube.enums import SIDE


CUBE_SIDES_COLOR_VALUES = [
    (0.6, 0.6, 0.6),  # front
    (0.80, 0.80, 0.80),  # top
    (0.95, 0.95, 0.95),  # right
]

ROW_LENGTH = 4  # should be dividable by 2
HEIGHT = 1
DEPTH = 4

# multipliers
SPACES_X = 9  # two-axis coords

CUBE_SIZE = 10

BRIGHTNESS_MULTIPLIER = 0.15  #

# direct values
X_OFFSET = 3
Y_OFFSET = 2

SPACES_Y = 15

INITIAL_BRIGHTNESS = .7


def create_cubes_array():
    cubes_array = []
    for plot_number in range(HEIGHT):  # Y_OFFSET, ROW_LENGTH + Y_OFFSET):
        cubes_plot = []
        for row_number in range(DEPTH):  # Y_OFFSET, ROW_LENGTH + Y_OFFSET):

            cubes_row = []
            for real_cube_nuber, cube_number in enumerate(range(ROW_LENGTH * 2, 0, -2)):
                pos = Pos(
                    x=(cube_number * SPACES_X + row_number * SPACES_X + X_OFFSET),
                    y=(row_number * SPACES_X + (5 + plot_number * SPACES_Y)) + Y_OFFSET,
                )
                cubes_row.append(Cube(front_side_bottom_left_corner_pos=pos, size=CUBE_SIZE))

            cubes_plot.append(cubes_row)

        cubes_array.append(cubes_plot)
    return cubes_array


class CubesWidget(Widget):
    def __init__(self, **kwargs):
        super(CubesWidget, self).__init__(**kwargs)

        self.cubes_array = create_cubes_array()
        self.sides = []

        with self.canvas:
            self._draw_cubes()

    def on_touch_up(self, touch):
        print(touch)
        for z in reversed(self.cubes_array):
            for x in reversed(z):
                for cube in reversed(x):
                    for side in cube.sides.values():
                        if not side.drawn:
                            continue

                        touch_x = touch.pos[0]
                        touch_y = touch.pos[1]

                        if touch_x > side.corners[0].x * 10 and touch_y > side.corners[0].y * 10:
                            if touch_x < side.corners[2].x * 10 and touch_y < side.corners[2].y * 10:

                                initial_coord_values = side.get_coords()

                                modified_coord_values = [
                                    coord - 15
                                    if idx in [0, 1, 2, 7]
                                    else coord + 15
                                    for idx, coord in enumerate(initial_coord_values)
                                ]

                                anim = Animation(points=modified_coord_values, duration=0.4, transition='out_back')

                                anim += Animation(points=initial_coord_values, duration=0.4, transition='in_back')
                                anim.start(side.drawn)

    def _draw_cubes(self):
        for plot_idx, plot in enumerate(self.cubes_array, start=2):  # height (z)

            for row_idx, row in enumerate(reversed(plot), start=2):  # rows from back to front

                for cube_idx, cube in enumerate(reversed(row), start=2):  # cubes from left to right  #

                    for side_idx, side in enumerate(cube.SIDES_DRAWING_ORDER):  # cube sides

                        shadow_multiplier = self._get_side_shadow_multiplier(side, plot_idx, row_idx, cube_idx)
                        color_with_shadow = self._adjust_color_brightness(side, shadow_multiplier)

                        Color(rgb=color_with_shadow)

                        cube.sides[side].draw()

    @staticmethod
    def _get_side_shadow_multiplier(side, plot_idx, row_idx, cube_idx):
        side_shadow_multiplier_map = {
            SIDE.TOP: (plot_idx + plot_idx + plot_idx + cube_idx + row_idx + SPACES_Y + SPACES_X) / 7,
            SIDE.FRONT: (plot_idx + row_idx + cube_idx + row_idx + row_idx + SPACES_Y + SPACES_X) / 7,
            SIDE.RIGHT: (cube_idx + plot_idx + cube_idx + row_idx + cube_idx + SPACES_Y + SPACES_X) / 7,
        }

        return side_shadow_multiplier_map[side]

    @staticmethod
    def _adjust_color_brightness(side, shadow_multiplier: float) -> List[float]:
        """
            used to adjust brightness according to shadow miltiplier, which is calculated
            basing on current cube's position and current side
        """

        side_initial_color = CUBE_SIDES_COLOR_VALUES[side]

        overall_multiplier = shadow_multiplier * BRIGHTNESS_MULTIPLIER
        recalculated_color = [color_part * overall_multiplier for color_part in side_initial_color]

        return recalculated_color

from typing import List

from kivy.graphics.context_instructions import Color
from kivy.uix.widget import Widget

from geometry.constants import SPACES_Y, SPACES_X
from geometry.cube_from_cubes import CubeFromCubes
from geometry.cube.enums import SIDES
from geometry.point import Point
from gui.constants import CUBE_SIDES_COLOR_VALUES, BRIGHTNESS_MULTIPLIER


class CubesWidget(Widget):
    def __init__(self, **kwargs):
        super(CubesWidget, self).__init__(**kwargs)

        self.cube_from_cubes = CubeFromCubes()
        self.sides = []

        with self.canvas:
            self._draw_cubes()

    def on_touch_up(self, touch):
        touch_point = Point(*touch.pos)

        for plot in reversed(self.cube_from_cubes.array):
            for row in plot:
                for cube in reversed(row):
                    if touch_point in cube:
                        cube.transform()
                        return

                    # for cube_side in reversed(cube.drawn_sides):
                    #
                    #     if touch_point in cube_side:
                    #         cube_side.transform()
                    #         return

    def _draw_cubes(self):
        for plot_idx, plot in enumerate(self.cube_from_cubes.array, start=2):  # height (z)
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
            SIDES.TOP: (plot_idx + plot_idx + plot_idx + cube_idx + row_idx + SPACES_Y + SPACES_X) / 70,
            SIDES.FRONT: (plot_idx + row_idx + cube_idx + row_idx + row_idx + SPACES_Y + SPACES_X) / 70,
            SIDES.RIGHT: (cube_idx + plot_idx + cube_idx + row_idx + cube_idx + SPACES_Y + SPACES_X) / 70,
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

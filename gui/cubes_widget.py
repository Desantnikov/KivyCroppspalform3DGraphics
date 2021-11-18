from typing import List

from kivy.animation import Animation
from kivy.graphics.context_instructions import Color
from kivy.uix.widget import Widget

from geometry.constants import SPACES_Y, SPACES_X
from geometry.cube_from_cubes import CubeFromCubes
from geometry.cube.enums import SIDE
from gui.constants import CUBE_SIDES_COLOR_VALUES, BRIGHTNESS_MULTIPLIER


class CubesWidget(Widget):
    def __init__(self, **kwargs):
        super(CubesWidget, self).__init__(**kwargs)

        self.cube_from_cubes = CubeFromCubes()
        self.sides = []

        with self.canvas:
            self._draw_cubes()

    def on_touch_up(self, touch):
        print(touch)
        for z in reversed(self.cube_from_cubes.array):
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

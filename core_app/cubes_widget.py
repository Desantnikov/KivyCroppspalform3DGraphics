import itertools
import time

from kivy.uix.widget import Widget

from geometry.cube_from_cubes import CubeFromCubes
from geometry.cube import Cube, CubeSide
from geometry.point import Point
from geometry.helpers import flatten
from graphic_controller import GraphicController
from kivy.graphics import RenderContext, Color, Rectangle, BindTexture
from kivy.uix.behaviors import CompoundSelectionBehavior, FocusBehavior, ButtonBehavior
from geometry.helpers import print_time_elapsed


class CubesWidget(Widget):
    def __init__(self, **kwargs):
        super(CubesWidget, self).__init__(**kwargs)

        self.cube_from_cubes = CubeFromCubes()

        with self.canvas:
            self.cube_from_cubes.draw()

    @print_time_elapsed
    def on_touch_up(self, touch):
        touch_point = Point(*touch.pos)

        all_cubes_flat_list = flatten(flatten(self.cube_from_cubes.array[::-1]))

        for collided_cube in filter(lambda cube: touch_point in cube, all_cubes_flat_list):
            with self.canvas:
                collided_cube.touched(touch_button=touch.button)

            return

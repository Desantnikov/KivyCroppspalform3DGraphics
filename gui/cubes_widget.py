from kivy.uix.widget import Widget

from geometry.cube_from_cubes import CubeFromCubes
from geometry.point import Point


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

    def _draw_cubes(self):
        for plot in self.cube_from_cubes.array:  # height (z)
            for row in reversed(plot):  # rows from back to front
                for cube in reversed(row):  # cubes from left to right  #
                    cube.draw()

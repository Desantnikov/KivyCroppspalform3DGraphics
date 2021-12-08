from geometry.helpers import print_time_elapsed
from geometry.point import Point
from geometry.cube import Cube
from geometry.enums import SPATIAL_DIRECTION

from constants import (
    CUBES_ARRAY_WIDTH,
    CUBES_ARRAY_HEIGHT,
    CUBES_ARRAY_DEPTH,
)


# Class used to create, incapsulate and operate with a 3-D array of cubes
class CubeFromCubes:
    __slots__ = 'array',

    def __init__(self):
        self.array = self._create_cubes_array()

    @print_time_elapsed
    def _create_cubes_array(self):
        cubes_array = []
        cubes_plot = []
        cubes_row = []

        for plot in range(CUBES_ARRAY_HEIGHT):
            for row in range(CUBES_ARRAY_DEPTH):
                for cube in range(CUBES_ARRAY_WIDTH):
                    cube = Cube(position_within_parent_cube=Point(row, cube, plot))
                    cubes_row.append(cube)

                cubes_row = cubes_plot.append(cubes_row) or []  # append current cubes row and clear
            cubes_plot = cubes_array.append(cubes_plot) or []  # append current cubes plot and clear

        return cubes_array

    @print_time_elapsed
    def draw(self):
        from kivy.graphics import Color
        for plot in self.array:  # height (z)
            for row in plot[::-1]:  # rows from back to front
                for cube in row[::-1]:  # cubes from left to right  #
                    cube.draw_sides()

                    Color(rgba=(0, 0, 0, 100))

                    for side in cube.drawn_sides:
                        dashed, dash_offset = None, None
                        # Color(rgba=(0, 0, 0, 2))
                        no_draw = False
                        if side.side_name in [SPATIAL_DIRECTION.LEFT, SPATIAL_DIRECTION.BACK]:
                            Color(rgba=(0, 0, 0, 100))
                            dashed = []
                            dash_offset = 10
                            no_draw = True

                        if not no_draw:
                            side.draw_edges(dashed=dashed, dash_offset=dash_offset)
                        no_draw = False

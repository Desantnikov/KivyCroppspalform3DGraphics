from geometry.point import Point
from geometry.cube import Cube
from geometry import helpers

from constants import (
    CUBES_ARRAY_WIDTH,
    CUBES_ARRAY_HEIGHT,
    CUBES_ARRAY_DEPTH,
    CUBE_SIZE,
)


class CubeFromCubes:
    """
        Class used to create, incapsulate and operate with a 3-D array of cubes
    """

    def __init__(self):
        self.array = self.create_cubes_array()

    @classmethod
    def create_cubes_array(cls):
        cubes_array = []
        cubes_plot = []
        cubes_row = []

        for height in range(CUBES_ARRAY_HEIGHT):
            for depth in range(CUBES_ARRAY_DEPTH):
                for width in range(CUBES_ARRAY_WIDTH):
                    cube = cls._create_cube(height=height, depth=depth, width=width)
                    cubes_row.append(cube)

                cubes_row = cubes_plot.append(cubes_row) or []  # append current cubes row and clear
            cubes_plot = cubes_array.append(cubes_plot) or []  # append current cubes plot and clear

        return cubes_array

    @classmethod
    def _create_cube(cls, height, depth, width, size=CUBE_SIZE):
        bottom_left_corner = helpers.calc_cube_initial_point(height=height, depth=depth, width=width)

        created_cube = Cube(
            front_side_initial_point=bottom_left_corner,
            size=size,
            position_within_parent_cube=Point(depth, width, height),
        )

        return created_cube



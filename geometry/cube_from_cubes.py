from geometry.point import Point
from geometry.cube.cube import Cube

from geometry.constants import (
    CUBES_ARRAY_WIDTH,
    CUBES_ARRAY_HEIGHT,
    CUBES_ARRAY_DEPTH,
    SPACES_X,
    SPACES_Y,
    CUBE_SIZE,
    X_OFFSET,
    Y_OFFSET,
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
        bottom_left_corner = cls._create_cube_bottom_left_corner(height=height, depth=depth, width=width)

        created_cube = Cube(
            front_side_initial_point=bottom_left_corner,
            size=size,
            position_within_parent_cube=Point(depth, width, height),
        )

        return created_cube

    @classmethod
    def _create_cube_bottom_left_corner(cls, height: int, depth: int, width: int) -> Point:
        # these x and y transformations were chosen randomly
        # but cubes positions looks more or less ok after them
        x = ((8 - width * 2) * SPACES_X + depth * SPACES_X + X_OFFSET)
        y = depth * SPACES_X + (5 + height * SPACES_Y) + Y_OFFSET

        return Point(x, y)

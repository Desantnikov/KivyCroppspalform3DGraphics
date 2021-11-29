import itertools

from geometry.point import Point

from constants import (
    SPACES_X,
    SPACES_Y,
    X_OFFSET,
    Y_OFFSET,
)


# Misc
def flatten(nested_iterable):
    return tuple(itertools.chain.from_iterable(nested_iterable))


# Geometry
def calc_cube_initial_point(height: int, depth: int, width: int) -> Point:
    # returns initial point for front side of a cube with chosen position within parent cube

    # these x and y transformations were chosen randomly
    # but cubes positions looks more or less ok after them
    x = ((8 - width * 2) * SPACES_X + depth * SPACES_X + X_OFFSET)
    y = depth * SPACES_X + (5 + height * SPACES_Y) + Y_OFFSET

    return Point(x, y)


def calc_square_corners(initial_point, size):
    square_corners = [
        initial_point,  # bottom left
        initial_point.apply_delta(0, size),  # top left
        initial_point.apply_delta(size, size),  # top right
        initial_point.apply_delta(size, 0),  # bottom right
    ]

    return square_corners




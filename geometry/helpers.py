import itertools


def flatten(input_list):
    return list(itertools.chain.from_iterable(input_list))


def calc_square_corners(bottom_left_corner, size):
    square_corners = [
        bottom_left_corner,  # bottom left
        bottom_left_corner.get_transformed_point(0, size),  # top left
        bottom_left_corner.get_transformed_point(size, size),  # top right
        bottom_left_corner.get_transformed_point(size, 0),  # bottom right
    ]

    return square_corners
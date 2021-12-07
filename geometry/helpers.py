import time
import itertools


# Misc
def flatten(nested_iterable):
    return tuple(itertools.chain.from_iterable(nested_iterable))


def calc_square_corners(initial_point, size):
    square_corners = [
        initial_point,  # bottom left
        initial_point.apply_delta(0, size),  # top left
        initial_point.apply_delta(size, size),  # top right
        initial_point.apply_delta(size, 0),  # bottom right
    ]

    return square_corners


def print_time_elapsed(func):
    def wrapped(*args, **kwargs):
        start_time = time.time()

        return_value = func(*args, **kwargs)

        time_elapsed = time.time() - start_time
        print(f'Function "{func.__qualname__}" took: {time_elapsed}s')

        return return_value

    return wrapped
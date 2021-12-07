import time
import itertools


# Misc
def flatten(nested_iterable):
    return tuple(itertools.chain.from_iterable(nested_iterable))


def pair(flat_iterable):
    # -> [1, 2, 3, 4, 5, 6]
    # <- [[1, 2], [3, 4], [5, 6]]
    result_list = []

    for i in range(0, len(flat_iterable), 2):
        result_list.append(flat_iterable[i:i+2])

    return result_list


def print_time_elapsed(func):
    def wrapped(*args, **kwargs):
        start_time = time.time()

        return_value = func(*args, **kwargs)

        time_elapsed = time.time() - start_time
        print(f'Function "{func.__qualname__}" took: {time_elapsed}s')

        return return_value

    return wrapped
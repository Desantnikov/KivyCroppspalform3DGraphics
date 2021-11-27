import itertools


def flatten(input_list):
    return list(itertools.chain.from_iterable(input_list))

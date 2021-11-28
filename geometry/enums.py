from enum import IntEnum


class SPATIAL_DIRECTION(IntEnum):
    FRONT = 0  # order is important; int value used to choose color from tuple by index
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
    BACK = 5


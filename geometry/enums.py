from enum import IntEnum


class SPATIAL_DIRECTION(IntEnum):
    FRONT = 0  # order is important; int value used to choose color from tuple by index
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
    BACK = 5


class TRANSFORMATION(IntEnum):
    MOVE_UP = 0
    MOVE_DOWN = 1
    MOVE_RIGHT = 2
    MOVE_LEFT = 3
    EXPAND_AND_ROTATE = 4

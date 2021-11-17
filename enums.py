from enum import IntEnum


class SIDE(IntEnum):
    FRONT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
    BACK = 5


class CORNER(IntEnum):
    LEFT_BOTTOM = 0
    LEFT_TOP = 1
    RIGHT_TOP = 2
    RIGHT_BOTTOM = 3

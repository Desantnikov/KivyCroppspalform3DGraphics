""" Window """
WINDOW_SIZE = (1640, 970)
WINDOW_SIZE = [dim * 0.95 for dim in WINDOW_SIZE]

""" Main """
CUBES_ARRAY_WIDTH = 6  # should be dividable by 2
CUBES_ARRAY_HEIGHT = 6
CUBES_ARRAY_DEPTH = 6


""" Geometry """
CUBE_SIZE = 80

# set to no spaces - new cube starts where previous ends
SPACES_X = CUBE_SIZE * 0.66  # 0.6
SPACES_Y = CUBE_SIZE * 1.1   # 1.1

X_OFFSET = ((CUBE_SIZE + SPACES_X) * CUBES_ARRAY_WIDTH) / 3
Y_OFFSET = CUBE_SIZE / 2


""" Drawing """
CUBE_SIDE_INITIAL_COLORS_VALUES = {
    'FRONT': (0.4,) * 3,
    'TOP': (0.435,) * 3,
    'RIGHT': (0.47,) * 3,
    'LEFT': (0.37,) * 3,
    'BACK': (0.35,) * 3,
}

TRANSFORMATION_DISTANCE = 30

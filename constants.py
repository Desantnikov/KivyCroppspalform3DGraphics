""" Window """
WINDOW_SIZE = (1640, 970)
WINDOW_SIZE = [dim * 0.95 for dim in WINDOW_SIZE]

""" Main """
CUBES_ARRAY_WIDTH = 12  # should be dividable by 2
CUBES_ARRAY_HEIGHT = 1
CUBES_ARRAY_DEPTH = 12


""" Geometry """
CUBE_SIZE = 50

# set to no spaces - new cube starts where previous ends
SPACES_X = CUBE_SIZE * 0.6  # 0.6
SPACES_Y = CUBE_SIZE * 1.1   # 1.1

X_OFFSET = ((CUBE_SIZE + SPACES_X) * CUBES_ARRAY_WIDTH) / 1.5
Y_OFFSET = CUBE_SIZE / 1


""" Drawing """
CUBE_SIDE_INITIAL_COLORS_VALUES = {
    'FRONT': (0.4,) * 3,
    'TOP': (0.435,) * 3,
    'RIGHT': (0.47,) * 3,
    'LEFT': (0.37,) * 3,
    'BACK': (0.35,) * 3,
}

FLAT_SQUARE = True
TRANSFORMATION_DISTANCE = 25

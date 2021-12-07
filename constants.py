
""" Main """
CUBES_ARRAY_WIDTH = 4  # should be dividable by 2
CUBES_ARRAY_HEIGHT = 4
CUBES_ARRAY_DEPTH = 4


""" Geometry """
CUBE_SIZE = 50

# set to no spaces - new cube starts where previous ends
SPACES_X = CUBE_SIZE * 0.66  # 0.6
SPACES_Y = CUBE_SIZE * 1.1   # 1.1

X_OFFSET = ((CUBE_SIZE + SPACES_X) * CUBES_ARRAY_WIDTH)
Y_OFFSET = CUBE_SIZE / 2


""" Drawing """
CUBE_SIDE_INITIAL_COLORS_VALUES = {
    'FRONT': (0.4,) * 3,
    'TOP': (0.435,) * 3,
    'RIGHT': (0.47,) * 3,
}

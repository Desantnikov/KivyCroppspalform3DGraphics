
""" Main """
CUBES_ARRAY_WIDTH = 10  # should be dividable by 2
CUBES_ARRAY_HEIGHT = 10
CUBES_ARRAY_DEPTH = 10


""" Geometry """
CUBE_SIZE = 50

# set to no spaces - new cube starts where previous ends
SPACES_X = CUBE_SIZE * 0.66  # 0.6
SPACES_Y = CUBE_SIZE * 1.1   # 1.1

X_OFFSET = ((CUBE_SIZE + SPACES_X) * CUBES_ARRAY_WIDTH) / 2
Y_OFFSET = CUBE_SIZE / 2


""" Drawing """

CUBE_SIDE_INITIAL_COLORS_VALUES = {
    'FRONT': (0.3,) * 3,  # front
    'TOP': (0.35,) * 3,#(0.80, 0.80, 0.80),  # top
    'RIGHT': (0.32,) * 3,#(0.9, 0.9, 0.9),  # right
}

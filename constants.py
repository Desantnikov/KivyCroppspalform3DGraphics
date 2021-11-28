""" Main """
CUBES_ARRAY_WIDTH = 4  # should be dividable by 2
CUBES_ARRAY_HEIGHT = 4
CUBES_ARRAY_DEPTH = 4


""" Geometry """
CUBE_SIZE = 75

X_OFFSET = 300
Y_OFFSET = 100

# set to no spaces - new cube starts where previous ends
SPACES_X = CUBE_SIZE * 0.5
SPACES_Y = CUBE_SIZE

SPACES_X += 10
SPACES_Y += 20


""" Drawing """
CUBE_SIDES_COLOR_VALUES = (
    (0.6, 0.6, 0.6),  # front
    (0.80, 0.80, 0.80),  # top
    (0.95, 0.95, 0.95),  # right
)
BRIGHTNESS_MULTIPLIER = 0.15

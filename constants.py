""" Main """
CUBES_ARRAY_WIDTH = 18  # should be dividable by 2
CUBES_ARRAY_HEIGHT = 18
CUBES_ARRAY_DEPTH = 18


""" Geometry """
CUBE_SIZE = 30

X_OFFSET = 600
Y_OFFSET = 50

# set to no spaces - new cube starts where previous ends
SPACES_X = CUBE_SIZE * 0.6
SPACES_Y = CUBE_SIZE * 1.1

# SPACES_X += 50
# SPACES_Y += 20


""" Drawing """
CUBE_SIDES_COLOR_VALUES = (
    (0.6, 0.6, 0.6),  # front
    (0.80, 0.80, 0.80),  # top
    (0.95, 0.95, 0.95),  # right
)
BRIGHTNESS_MULTIPLIER = 0.3

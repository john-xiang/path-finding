"""
    This file contains some predefined parameter values
"""
# Chance for random obstacles
CHANCE = 0.25

# Define display parameters
WIDTH = 800
HEIGHT = 800
NODE_SIZE = 20
LIMIT = WIDTH // NODE_SIZE    # total number of cells

# Button parameters
NUM_BTS = 4               # buttons per row
BUFFER = 5                # buffer spaces between buttons
BT_HEIGHT = 45
BT_WIDTH = (WIDTH - (BUFFER*NUM_BTS)) // NUM_BTS

# Font
FONT_PATH = '/home/johnx/Projects/path-finding/font/OpenSans-Semibold.ttf'

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CREAM = (222, 222, 222)
GREEN = (0, 255, 0)
DRK_GREEN = (0, 128, 0)
DARKER_GREEN = (0, 50, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LT_BLUE = (37, 194, 221)
DRK_BLUE = (0, 0, 128)
ORANGE = (255, 128, 0)
PURPLE = (179,128,223)
YELLOW = (255, 255, 0)
LT_YELLOW = (155, 155, 0)
GREY = (143, 143, 143)
LT_GREY = (175, 200, 175)
BROWN = (186, 127, 50)

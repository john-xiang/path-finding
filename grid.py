"""
    ...
"""

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 111, 255)
ORANGE = (255, 128, 0)
PURPLE = (128, 0, 255)
YELLOW = (255, 255, 0)
GREY = (143, 143, 143)
BROWN = (186, 127, 50)
DARK_GREEN = (0, 128, 0)
DARKER_GREEN = (0, 50, 0)
DARK_BLUE = (0, 0, 128)

class Node:
    """
        ...
    """
    def __init__(self, category='empty', colour=WHITE, pos=None):
        self.category = category    # categories = [start, end, empty, wall]
        self.colour = colour
        self.path = False
        self.visited = False
        self.pos = pos

class Grid:
    """
        ...
    """
    def __init__(self, display, nodesize, boardsize):
        self.display = display
        self.nodesize = nodesize
        self.boardsize = boardsize
        self.graph = (Node() for node in range(int(boardsize/nodesize)))

    def render_grid(self):
        """
            ...
        """
        # finds out how many nodes we need to render
        cells = int(self.boardsize/self.nodesize)

        # draw the grid
        for i in range(cells):
            start_vert = (self.nodesize*i, 0)
            end_vert = (self.nodesize*i, self.boardsize)
            start_hor = (0, self.nodesize*i)
            end_hor = (self.boardsize, self.nodesize*i)
            pygame.draw.aaline(self.display, BLACK, start_vert, end_vert)
            pygame.draw.aaline(self.display, BLACK, start_hor, end_hor)

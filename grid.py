"""
    ...
"""

from collections import defaultdict
import pygame
import colour as col

class Node:
    """
        ...
    """
    def __init__(self, status='empty'):
        self.status = status    # categories = [start, end, empty, wall]
        self.path = False
        self.visited = False
        self.neighbours = []

    def find_neighbours(self, node):
        """
            Finds the neighbours for a node
            TODO: look up, down, left and right for nodes
            if they are not 'walls' then append to neighbours list
        """
        exit()

    def show_path(self):
        return self.path

class Grid:
    """
        ...
    """
    def __init__(self, display, nodesize, boardsize):
        self.display = display
        self.nodesize = nodesize
        self.boardsize = boardsize
        self.graph = defaultdict(Node)

    def render_grid(self):
        """
            ...
        """
        count = 0
        # finds out how many nodes we need to render
        cells = int(self.boardsize/self.nodesize)

        # draw the grid
        for i in range(cells+1):
            # start and end position of vertical lines
            start_vert = (self.nodesize*i, 0)
            end_vert = (self.nodesize*i, self.boardsize)
            # start and end position of horizontal lines
            start_hor = (0, self.nodesize*i)
            end_hor = (self.boardsize, self.nodesize*i)
            # render lines
            pygame.draw.aaline(self.display, col.BLACK, start_vert, end_vert)
            pygame.draw.aaline(self.display, col.BLACK, start_hor, end_hor)
            for j in range(cells):  # initiate node object for each grid
                self.graph[count] = Node()
                count += 1

"""
    ...
"""

from collections import defaultdict
import time
import pygame
import colour as col


class Node:
    """
        ...
    """
    def __init__(self, xpos, ypos, status='empty'):
        self.status = status    # categories = [start, end, empty, wall]
        self.xpos = xpos
        self.ypos = ypos
        self.distance = 999999
        self.previous = (-1, -1)
        self.neighbours = []


class Grid:
    """
        ...
    """
    def __init__(self, display, nodesize, boardsize):
        self.display = display
        self.nodesize = nodesize
        self.boardsize = boardsize
        self.graph = defaultdict()


    def render_grid(self):
        """
            ...
        """
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
                if i < cells:
                    self.graph[i, j] = Node(i, j)


    def find_neighbours(self, node):
        """
            Finds the neighbours for a node which is not a wall.
            This function checks the top, bottom, left and right for neighbours.
                1) if the node in question is a wall, then no checks will be done
                2) If the neighbouring cell is a wall, then it will not be counted as a neighbour
        """
        neighbours = []
        xpos = node[0]
        ypos = node[1]
        limit = int(self.boardsize/self.nodesize)

        if self.graph[node].status == 'wall':  # do not check nodes which are walls
            self.graph[node].neighbours = []
            return

        if xpos > 0:
            if self.graph[xpos-1, ypos] != 'wall':      # left
                neighbours.append((xpos-1, ypos))
        if xpos < limit-1:
            if self.graph[xpos+1, ypos] != 'wall':      # right
                neighbours.append((xpos+1, ypos))
        if ypos > 0:
            if self.graph[xpos, ypos-1] != 'wall':      # top
                neighbours.append((xpos, ypos-1))
        if ypos < limit-1:
            if self.graph[xpos, ypos+1] != 'wall':      # bottom
                neighbours.append((xpos, ypos+1))

        self.graph[node].neighbours = neighbours


    def find_min(self, visited_set):
        """
            Helper function that finds the index of the graph with minimum distance
                NOTE: if the node is in the visited set then it won't be considered
        """
        # find the next node with smallest distance
        min_dist = None
        min_index = None
        for index, node in self.graph.items():
            if node.distance > 0 and (min_dist is None or node.distance < min_dist):
                if index in visited_set:    # if node is visited, then don't consider
                    continue
                min_dist = node.distance
                min_index = index

        return min_index


    def dijkstra(self, source, target):
        """
            Dijkstra's algorithm finds the shortest path between a source and target node.
            The algorithm works as follows:
                1) All nodes are initially unvisited
                2) set the source node as the current node
                3) Initialize the tentative distance of the source node as 0
                    all other nodes have distance of infinity
                4) While target node is unvisited
                    a) compute the distance between current node and each neighbour node
                    b) if computed distance is smaller than replace as current distance
                    c) remove the current node from the unvisited list and continue
                5) Display result

            The inputs to dijkstra is source node, target node and graph.
                The graph is represented as a grid and the neighbours are the
                north, south, east and west cells. Helper function find_neighbours
                is used to help compute neighbours for each cell.

            The output is the computed path and the length of said path.
                If there are no paths found, then -1 is returned.
        """
        unvisited = list(self.graph)
        visited = []
        self.graph[source].distance = 0 # set the distance of source to 0
        path = []           # stores the computed path from source to node
        size = self.nodesize
        current = source

        while unvisited and target in unvisited:
            if self.graph[current].status == 'wall':
                # skip the current node if it's a wall since we can't traverse it
                unvisited.remove(current)  # remove the current node from unvisited set
                visited.append(current)
                current = self.find_min(visited)
                continue
            tentative_dist = self.graph[current].distance + 1
            # compute the distance travelled for each neighbour node
            self.find_neighbours(current)
            for neighbour in self.graph[current].neighbours:
                # render in the neighbours for the current computation
                xpos = (neighbour[0] * size) + 1
                ypos = (neighbour[1] * size) + 1
                if self.graph[neighbour].status == 'empty':
                    pygame.draw.rect(self.display, col.LT_BLUE, [xpos, ypos, size-1, size-1])

                # update distance if it's smaller than current recorded distance
                if tentative_dist < self.graph[neighbour].distance:
                    self.graph[neighbour].distance = tentative_dist
                    # update where the node travelled from
                    self.graph[neighbour].previous = current

                pygame.display.update() # update display

            time.sleep(0.015)            # set a small delay between nodes
            unvisited.remove(current)   # remove the current node from unvisited set
            visited.append(current)

            # find the next node with smallest distance and update current node
            current = self.find_min(visited)

        if self.graph[target].previous == (-1, -1): # no path found
            return -1

        # backtrack to find the full path
        node = target
        path_dist = self.graph[target].distance
        path.append(node)
        while len(path) <= path_dist:
            node = self.graph[node].previous
            path.append(node)

        return (path, path_dist)

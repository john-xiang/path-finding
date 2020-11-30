"""
Grid.py contains the class information for the grid and node

Node Class:
    each cell of a grid is defined by a node object which contains
    several parameters.

    init:
        status: classifies the cell as a start, end, wall or empty node
        xpos: the x position of the node on the grid
        ypos: the y position of the node on the grid
        neighbours: the neighbours of the node
        distance: computed distance from the source to this node
        previous: what was the previous node that travelled to this node
        fscore: computed fscore (fscorce = distance + heuristic(node, target))
            NOTE: heuristic is a standalone function and computes the manhattan
            distance (abs(x1 - y1) + abs(x2 - y2))

Grid Class:
    Grid class defines and renders the whole grid. Stores each cell as a
    node object and together forms the graph.

    init:
        display: the current display
        nodesize: the pixel size of each node
        boardsize: size of the board
"""

from collections import defaultdict
import math
import time
import pygame
import parameters as param
import minheap as minh

def heuristic(source, target):
    """
    This function will compute the heuristic function for A*
    The chosen heuristic will be the Manhattan distance which is
        abs(x1 - y1) + abs(x2 - y2) if x = (x1, x2) and y = (y1, y2)
    """
    return abs(source[0]-target[0]) + abs(source[1]-target[1])

class Node:
    """
    init:
        status: classifies the cell as a start, end, wall or empty node
        xpos: the x position of the node on the grid
        ypos: the y position of the node on the grid
        neighbours: the neighbours of the node
        previous: what was the previous node that travelled to this node
        distance: computed distance from the source to this node
        fscore: computed fscore (fscorce = distance + heuristic(node, target))
            NOTE: heuristic is a standalone function and computes the manhattan
            distance (abs(x1 - y1) + abs(x2 - y2))
    """
    def __init__(self, xpos, ypos, status='empty'):
        self.status = status    # categories = [start, end, empty, wall]
        self.xpos = xpos
        self.ypos = ypos
        self.neighbours = []
        self.previous = (-1, -1)
        self.distance = math.inf
        self.fscore = math.inf
        self.infringe = False

class Grid:
    """
        ...
    """
    def __init__(self, display):
        self.display = display
        self.graph = defaultdict()

    def build_graph(self):
        """
        Builds the graph by initiating an empty node for each
        cell of the grid
        """
        for i in range(param.LIMIT):
            for j in range(param.LIMIT):
                self.graph[i, j] = Node(i, j)

    def render_neighbours(self, node):
        """
        Renders the neighbours which are being checked
        """
        # render in the neighbours for the current computation
        xpos = node[0] * param.NODE_SIZE
        ypos = node[1] * param.NODE_SIZE
        if self.graph[node].status == 'empty':
            pygame.draw.rect(self.display, param.LT_BLUE, \
                [xpos, ypos, param.NODE_SIZE, param.NODE_SIZE])

    def find_neighbours(self, node, visited_set):
        """
            Finds the neighbours for a node which is not a wall.
            This function checks the top, bottom, left and right for neighbours.
                1) if the node in question is a wall, then no checks will be done
                2) If the neighbouring cell is a wall, then it will not be counted as a neighbour
        """
        if self.graph[node].status == 'wall':  # do not check nodes which are walls
            self.graph[node].neighbours = []
            return

        neighbours = []
        xpos = node[0]
        ypos = node[1]

        if xpos > 0:
            if self.graph[xpos-1, ypos] != 'wall' and \
                (xpos-1, ypos) not in visited_set:      # left
                neighbours.append((xpos-1, ypos))
        if xpos < param.LIMIT-1:
            if self.graph[xpos+1, ypos] != 'wall' and \
                (xpos+1, ypos) not in visited_set:      # right
                neighbours.append((xpos+1, ypos))
        if ypos > 0:
            if self.graph[xpos, ypos-1] != 'wall'and \
                (xpos, ypos-1) not in visited_set:      # top
                neighbours.append((xpos, ypos-1))
        if ypos < param.LIMIT-1:
            if self.graph[xpos, ypos+1] != 'wall' and \
                (xpos, ypos+1) not in visited_set:      # bottom
                neighbours.append((xpos, ypos+1))

        self.graph[node].neighbours = neighbours

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

        Inputs: the graph, the source node and the target node.
        Outputs: the computed path and its length. If there are no paths then return -1

        Helper function find_neighbours:
            This function is used to help compute neighbours for a given node.
        """
        visited = []    # stores the visited nodes
        path = []       # stores the computed path from source to node
        path_found = False
        self.graph[source].distance = 0 # set the distance of source to 0
        unvisited = minh.MinHeap()      # build the min heap priority queue
        unvisited.build_heap([(self.graph[node].distance, node) for node in self.graph])

        while unvisited and not path_found:
            extracted_min = unvisited.extract_min()   # set current and extract from unvisited
            current = extracted_min[1]
            visited.append(current)

            if self.graph[current].distance == math.inf:
                # the distance is infinity only if there are no more paths found
                return -1
            if current == target:   # at the target node! don't need to search further
                path_found = True
                continue
            if self.graph[current].status == 'wall':
                # skip the current node if it's a wall since we can't traverse it
                continue

            # compute the distance travelled for each neighbour node
            tentative_dist = self.graph[current].distance + 1   # tentative distance
            self.find_neighbours(current, visited)
            for neighbour in self.graph[current].neighbours:
                # render the cells which are being considered for current computation
                self.render_neighbours(neighbour)
                # update distance if it's smaller than current recorded distance
                if tentative_dist < self.graph[neighbour].distance:
                    self.graph[neighbour].distance = tentative_dist
                    # update where the node travelled from
                    self.graph[neighbour].previous = current
                    # update priority queue
                    for index, node in enumerate(unvisited.items()):
                        if node == 0:   # skip the 0 element in the heap
                            continue
                        if neighbour == node[1]:
                            unvisited.decrease_key(index, (tentative_dist, neighbour))

            pygame.display.update() # update display

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

    def a_star(self, source, target):
        """
        The A* algorithm is an extention of Dijkstra where a heuristic is applied to
            guide the search towards the target node. The heuristic of choice here
            will be the Manhattan distance between the node in question to the target
            node. This was chosen because it provicdes a better approximation when we
            are only considering movement along the cardinal directions.
        The algorithm works as follows:
            1) Initiate two sets, one is for nodes that have been visited and the
                other is for nodes who are currently being considered for expansion
            2) Push the current node (source node is first) to the open set
            3) Repeat until the open set is empty:
                1) set the current node to be the one with lowest score
                2) If the current node is the target node then finish!
                3) remove the current node from the open set
                4) Check each neighbour of the current node:
                    1) Compute the tentative score
                    2) if the tentative score is less than the current score
                        then set the current score to be the tentative score
                    3) Add the neighbour to the openset if it's not already in
            4) if the open set is empty then we have not found a path!

        Inputs: the graph, the source node and the target node
        Outputs: The computed path and the length
        """
        fringe = minh.MinHeap()
        visited = []
        path = []
        self.graph[source].distance = 0 # set the distance of source to 0
        self.graph[source].fscore = self.graph[source].distance + heuristic(source, target)
        fringe.insert((0, 0, source))   # the heap descending on fscore, heuristic

        while fringe:
            extracted_min = fringe.extract_min()
            current = extracted_min[2]

            if current == target:           # reached the target!
                # backtrack to find the full path
                node = target
                path_dist = self.graph[target].distance
                path.append(node)
                while len(path) <= path_dist:
                    node = self.graph[node].previous
                    path.append(node)
                return (path, path_dist)

            visited.append(current)         # add node to visited
            self.find_neighbours(current, visited)   # find neighbours

            for neighbour in self.graph[current].neighbours:
                # render the cells which are being considered for current computation
                self.render_neighbours(neighbour)

                # set the tentative distance
                tentative_dist = self.graph[current].distance + 1

                if tentative_dist < self.graph[neighbour].distance:
                    # path through current node is better than previous path
                    self.graph[neighbour].distance = tentative_dist
                    self.graph[neighbour].previous = current
                    hvalue = heuristic(neighbour, target)
                    self.graph[neighbour].fscore = tentative_dist + hvalue

                    # add neighbour to the fringe set if it's not yet in there
                    if not self.graph[neighbour].infringe:
                        self.graph[neighbour].infringe = True
                        fringe.insert((self.graph[neighbour].fscore, hvalue, neighbour))

            time.sleep(0.03)
            pygame.display.update() # update display

        # if loop finishes then fringe_set is empty and no paths are found
        return -1

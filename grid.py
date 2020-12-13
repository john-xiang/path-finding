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
            fscore: computed fscore (fscore = distance + heuristic(node, target))
                NOTE: heuristic is a standalone function and computes the manhattan
                distance (abs(x1 - y1) + abs(x2 - y2))

    Grid Class:
        Grid class defines and renders the whole grid. Stores each cell as a
        node object and together forms the graph.

        init:
            display: the current display
            graph: the cells of the grid where each cell is a node object
"""

from collections import defaultdict
from collections import deque
import math
import time
import random
import pygame
import parameters as param
import minheap as minh

def heuristic(source, target):
    """
        This function will compute the heuristic function for A*
        The chosen heuristic will be the Manhattan distance

        abs(x1 - y1) + abs(x2 - y2) if x = (x1, x2) and y = (y1, y2)
    """
    return abs(source[0]-target[0]) + abs(source[1]-target[1])

class Node:
    """
        Init:
            status: classifies the cell as a start, end, wall or empty node
            xpos: the x position of the node on the grid
            ypos: the y position of the node on the grid
            previous: what was the previous node that travelled to this node
            distance: computed distance from the source to this node
            fscore: computed fscore (fscore = distance + heuristic(node, target))
            visited: boolean variable that determines if the node is in the fringe set

        Methods:
            Move(new xpos, new ypos): moves the position of a node to the new position
            reset_parameters(): resets the parameter of a node to the default values
    """
    def __init__(self, xpos, ypos, status='empty'):
        self.status = status    # categories = [start, end, empty, wall]
        self.xpos = xpos
        self.ypos = ypos
        self.previous = (-1, -1)
        self.distance = math.inf
        self.fscore = math.inf
        self.visited = False

    def move(self, newx, newy):
        """
            This function moves the current node to a different position
        """
        self.xpos = newx
        self.ypos = newy

    def reset_parameters(self):
        """
            Resets the initial parameters for all nodes in the graph
        """
        self.previous = (-1, -1)
        self.distance = math.inf
        self.fscore = math.inf
        self.visited = False

class Grid:
    """
        Init
            display: The current display for rendering purposes
            graph: the graph represented as a list of Node objects

        Methods
            build_graph(): builds the graph to the size of the grid
            generate_obstacles(): randomly generate wall obstacles determined by
                the chance variable in parameter.py
            render_node(node): renders the node onto the display
            find_neighbours(node): returns the neighbours of the input node
            find_path(target): returns the path found as a list of nodes
            dijkstra(source, target): returns the shortest path from source to target
                with dijkstra's pathfinding algorithm
            astar(source, target): returns the shortest path from source to target
                with astar pathfininding algorithm
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

    def generate_obstacles(self):
        """
            Randomly generate wall obstacles on the graph. Each node in the graph
            has a chance to become a wall and is based on the CHANCE variable in parameter.py
        """
        for node in self.graph:
            empty_node = (self.graph[node].status != 'start' and self.graph[node].status != 'end')
            if random.random() <= param.CHANCE and empty_node:  # node has CHANCE % to be a wall
                self.graph[node].status = 'wall'
                xpos = node[0] * param.NODE_SIZE
                ypos = node[1] * param.NODE_SIZE
                pygame.draw.rect(self.display, param.BLACK, \
                    [xpos, ypos, param.NODE_SIZE, param.NODE_SIZE])

    def render_node(self, node):
        """
            Renders the input node onto the grid
        """
        # render in the neighbours for the current computation
        xpos = node[0] * param.NODE_SIZE
        ypos = node[1] * param.NODE_SIZE
        if self.graph[node].status == 'empty':
            pygame.draw.rect(self.display, param.LT_BLUE, \
                [xpos, ypos, param.NODE_SIZE, param.NODE_SIZE])

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

        if self.graph[node].status == 'wall':  # do not check nodes which are walls
            return neighbours

        # main check for the neighbours (left, right, top , bottom)
        if xpos > 0 and self.graph[xpos-1, ypos] != 'wall':
            neighbours.append((xpos-1, ypos))
        if xpos < param.LIMIT-1 and self.graph[xpos+1, ypos] != 'wall':
            neighbours.append((xpos+1, ypos))
        if ypos > 0 and self.graph[xpos, ypos-1] != 'wall': 
            neighbours.append((xpos, ypos-1))
        if ypos < param.LIMIT-1 and self.graph[xpos, ypos+1] != 'wall':
            neighbours.append((xpos, ypos+1))

        return neighbours

    def find_path(self, target):
        """
            Finds the path by backtracking. Start at the target node and keeping
            recording the previous node until the source node is reached.

            target -> prev node -> prev node -> ... -> source
        """
        path = []
        node = target
        path_dist = self.graph[target].distance
        path.append(node)
        while len(path) <= path_dist:
            node = self.graph[node].previous
            path.append(node)
        print('The path distance is', path_dist)
        return path

    def dijkstra(self, source, target):
        """
            Dijkstra's algorithm finds the shortest path between a source and target node.
                1) All nodes are initially unvisited
                2) set the source node as the current node
                3) Initialize the tentative distance of the source node as 0
                    all other nodes have distance of infinity
                4) While target node is unvisited
                    a) compute the distance between current node and each neighbour node
                    b) if computed distance is smaller than replace as current distance
                    c) remove the current node from the unvisited list and continue
                5) Display result

            Inputs: the source node and the target node.
            Outputs: the computed path and its length. If there are no paths then return -1

            Helper function
                find_neighbours(node): used to help compute neighbours for a given node.
        """
        start_time = time.time()
        visited = []    # stores the visited nodes
        self.graph[source].distance = 0 # set the distance of source to 0
        unvisited = minh.MinHeap()      # build the min heap priority queue
        unvisited.build_heap([(self.graph[node].distance, node) for node in self.graph])

        while unvisited:
            extracted_min = unvisited.extract_min()   # set current and extract from unvisited
            current = extracted_min[1]
            visited.append(current)

            if self.graph[current].distance == math.inf:
                # the distance is inf only when there's no other nodes to consider
                end_time = time.time() - start_time
                print('Time elapsed:', end_time)
                return -1

            if current == target:   # at the target node! don't need to search further
                end_time = time.time() - start_time
                print('Time elapsed:', end_time)
                return self.find_path(target)

            if self.graph[current].status == 'wall':
                # skip the current node if it's a wall since we can't traverse it
                continue

            # compute the distance travelled for each neighbour node
            tentative_dist = self.graph[current].distance + 1   # tentative distance
            current_neighbours = self.find_neighbours(current)
            for neighbour in current_neighbours:
                if neighbour not in visited and tentative_dist < self.graph[neighbour].distance:
                    self.render_node(neighbour)   # render the cells
                    # update distance if it's smaller than current recorded distance
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
        # no path found
        end_time = time.time() - start_time
        print('Time elapsed:', end_time)
        return -1

    def astar(self, source, target):
        """
            The A* algorithm is an extention of Dijkstra where a heuristic is applied to
            guide the search towards the target node. The heuristic of choice here
            will be the Manhattan distance between the node in question to the target
            node. This was chosen because it provicdes a better approximation when we
            are only considering movement along the cardinal directions.

            The algorithm works as follows:
                1) Initiate two sets, one is for nodes that have been visited and the
                    other is for nodes who are currently being considered for expansion
                2) Push the current node (source node is first) to the fringe set
                3) Repeat until the fringe set is empty:
                    1) find the node with smallest fscore in fringe set and set as current node
                    2) If the current node is the target node then finish!
                    3) otherwise remove the current node from the fringe set and add to visited set
                    4) Check each neighbour of the current node:
                        1) Compute the tentative distance
                        2) if the tentative distance is less than the neighbour's distance
                            then update the distance to be the tentative distance
                        3) Add the neighbour to the fringe set if it's not already in
                4) if the fringe set is empty then we have not found a path!

            Inputs: the source node and the target node
            Outputs: The computed path and the length

            Helper Function:
                find_neighbours(node): finds the neighbours for the current node
                heuristic(node, target): computes the heuristic value
        """
        start_time = time.time()
        fringe = minh.MinHeap()
        self.graph[source].distance = 0     # set the distance of source to 0
        # compute the fscore (fscore = distance + heuristic)
        self.graph[source].fscore = self.graph[source].distance + heuristic(source, target)
        self.graph[source].visited = True   # mark as visited
        fringe.insert((self.graph[source].fscore, \
            self.graph[source].distance, source))   # insert source node (fscore, dist, node)

        while fringe:
            # Set the current node as the node with minimum fscore value
            extracted_min = fringe.extract_min()
            current = extracted_min[2]

            if current == target:           # reached the target! return path
                end_time = time.time() - start_time
                print('Time elapsed:', end_time)
                return self.find_path(target)

            current_neighbours = self.find_neighbours(current)   # find neighbours
            tentative_dist = self.graph[current].distance + 1   # set the tentative distance

            for neighbour in current_neighbours:
                if not self.graph[neighbour].visited and \
                    tentative_dist < self.graph[neighbour].distance:
                    # the current path to the neighbour is better than the previous path
                    self.render_node(neighbour)

                    # Update distance, previous, fscore and visited
                    self.graph[neighbour].distance = tentative_dist
                    self.graph[neighbour].previous = current
                    self.graph[neighbour].fscore = tentative_dist + heuristic(neighbour, target)
                    self.graph[neighbour].visited = True

                    # Add the node to the fringe set
                    fringe.insert((self.graph[neighbour].fscore, tentative_dist, neighbour))
            pygame.display.update() # update display
        #no paths are found
        end_time = time.time() - start_time
        print('Time elapsed:', end_time)
        return -1

    def greedy(self, source, target):
        """
            The greedy best-first search is a greedy algorithm that only considers the
            heuristic value and chooses the best option at each iteration during the search.
            This algorithm is not guaranteed to find the shortest path but will generally
            find a path very quickly if one exists. The heuristic of choice will be the
            Manhattan distance.

            The algorithm works as follows:
                1) Initialize the distance from all nodes to target as infinity
                2) Set the distance of the source node to heuristic(source, target)
                3) Repeat until the fringe set is empty
                    a) Set the current node to be minimum distance in the fringe set
                    b) if the current node is the target then finished!
                    c) otherwise remove current node from the fringe set and add to
                    the visited set
                    d) For every child of the current node that is not in visited set
                        i) Set the distance of the node as heuristic(child, target)
                        ii) insert the child to the fringe set if not in already
                4) if fringe set is empty then there are no paths found

            Inputs: source node and target node
            Outputs: path from source to target, not guaranteed optimal

            Helper function:
                find_neighbours(node): finds the neighbours of a node
                heuristic(node, target): computes the heuristic value
        """
        start_time = time.time()
        fringe = minh.MinHeap()
        self.graph[source].distance = 0         # set the initial distance to 0
        self.graph[source].fscore = heuristic(source, target)   # set heuristic (source, target)
        fringe.insert((self.graph[source].fscore, source))      # insert source to fringe set
        self.graph[source].visited = True                       # mark as visited

        while fringe:
            # Set the current node as the node with minimum distance (heuristic)
            extracted_min = fringe.extract_min()
            current = extracted_min[1]

            if current == target:   #reached the target! return path
                end_time = time.time() - start_time
                print('Time elapsed:', end_time)
                return self.find_path(target)

            current_neighbours = self.find_neighbours(current)  # find neighbours

            for neighbour in current_neighbours:
                if not self.graph[neighbour].visited:
                    # Compute the distance (heuristic) of all neighbours and add to fringe set
                    self.render_node(neighbour)

                    # Update previous, fscore, distance and visited
                    self.graph[neighbour].previous = current
                    self.graph[neighbour].fscore = heuristic(neighbour, target)
                    self.graph[neighbour].distance = self.graph[current].distance + 1
                    self.graph[neighbour].visited = True

                    # Insert into fringe
                    fringe.insert((self.graph[neighbour].fscore, neighbour))
                pygame.display.update()
        # no paths found
        end_time = time.time() - start_time
        print('Time elapsed:', end_time)
        return -1

    def bfs(self, source, target):
        """
            The breadth-first search algorithm searches through each node of the
            current depth of the graph before moving onto the next depth level. BFS
            is a brute force algorithm that visits all the nodes and gurantees that
            the path found is optimal (from the source to target node).

            The data structure for this algorithm will be a queue. I will be using
            collections.deque instead of implenting one from scratch
        """
        start_time = time.time()
        fringe = deque()
        self.graph[source].distance = 0
        self.graph[source].visited = True
        fringe.append(source)

        while fringe:
            current = fringe.popleft()

            if current == target:   # reached the target! return path
                end_time = time.time() - start_time
                print('Time elapsed:', end_time)
                return self.find_path(target)

            current_neighbours = self.find_neighbours(current)  # find neighbours

            for neighbour in current_neighbours:
                if not self.graph[neighbour].visited:
                    self.render_node(neighbour)

                    self.graph[neighbour].previous = current
                    self.graph[neighbour].distance = self.graph[current].distance + 1
                    self.graph[neighbour].visited = True

                    fringe.append(neighbour)
            pygame.display.update()
        # no paths found!
        end_time = time.time() - start_time
        print('Time elapsed:', end_time)
        return -1

    def dfs(self, source, target):
        """
            ...
        """
        start_time = time.time()
        fringe = deque()
        self.graph[source].distance = 0
        fringe.append(source)

        while fringe:
            current = fringe.pop()
            self.graph[current].visited = True

            if current == target:
                end_time = time.time() - start_time
                print('Time elapsed:', end_time)
                return self.find_path(target)

            current_neighbours = self.find_neighbours(current)

            for neighbour in current_neighbours:
                if not self.graph[neighbour].visited:

                    self.render_node(neighbour)

                    self.graph[neighbour].previous = current
                    self.graph[neighbour].distance = self.graph[current].distance + 1
                    self.graph[neighbour].visited = True

                    fringe.append(neighbour)
                pygame.display.update()
        end_time = time.time() - start_time
        print('Time elapsed:', end_time)
        return -1

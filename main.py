"""
    ...
"""

import sys
import random
import time
import pygame
import grid as g
import parameters as param
import button as bt


def convert2single(xpos, ypos):
    """
    Helper function that converts an (x,y) coordinate to a
    single number using the formula y * MAXY + x
    """
    return ypos * param.LIMIT + xpos

def convert2xy(num):
    """
    Helper function that converts a single number to an
    (x,y) coordinate. X is computed by num % MAXY and Y
    is computed by num / MAXY
    """
    x_pos = num % param.LIMIT
    y_pos = num / param.LIMIT
    return (x_pos, y_pos)

def render_walls(graph, mousepos, display):
    """
    This function renders the walls onto the display
    """
    (xpos, ypos) = (mousepos[0] // param.NODE_SIZE, mousepos[1] // param.NODE_SIZE)

    # only colour empty nodes within the grid
    if graph.graph[xpos, ypos].status == 'empty' and mousepos[1] < param.HEIGHT:
        # locate the top left corner position of the square
        xstart = xpos * param.NODE_SIZE
        ystart = ypos * param.NODE_SIZE
        # colour in the obstacle
        pygame.draw.rect(display, param.BLACK, \
            [xstart, ystart, param.NODE_SIZE, param.NODE_SIZE])
        # change the status of nodes that have become obstacles ('wall')
        graph.graph[xpos, ypos].status = 'wall'

def render_path(source, target, path, display, speed=None):
    """
    This function renders the computed path onto the display
    """
    for node in reversed(path):
        # Don't colour in the source and target node
        if node in [source, target]:
            continue
        xstart = node[0] * param.NODE_SIZE
        ystart = node[1] * param.NODE_SIZE
        # colour in the path
        pygame.draw.rect(display, param.YELLOW, \
            [xstart, ystart, param.NODE_SIZE, param.NODE_SIZE])
        if speed is None:
            time.sleep(0.03)
            pygame.display.update()

def render_node(node, colour, display):
    """
    This function renders a cell onto the grid corresponding to
    the node
    """
    startx = node[0] * param.NODE_SIZE
    starty = node[1] * param.NODE_SIZE
    # render the colour
    pygame.draw.rect(display, colour, \
        [startx, starty, param.NODE_SIZE, param.NODE_SIZE]) # (x, y, width, height)

def clear_path(graph, display):
    """
    Clear all paths and search process from previous search
    """
    for node in graph:
        graph[node].reset_parameters()
        if graph[node].status in ['empty']:
            render_node(node, param.CREAM, display)
        if graph[node].status in ['start']:
            render_node(node, param.RED, display)
        if graph[node].status in ['end']:
            render_node(node, param.GREEN, display)

def clear_everything(graph, display):
    """
    Resets the board completely
    """
    for node in graph:
        graph[node].reset_parameters()
        if graph[node].status in ['empty', 'wall']:
            graph[node].status = 'empty'
            render_node(node, param.CREAM, display)
        if graph[node].status in ['start']:
            render_node(node, param.RED, display)
        if graph[node].status in ['end']:
            render_node(node, param.GREEN, display)


def start():
    """
    Main function that handles most of the rendering and logic
    """
    # Variables for click and drag functions
    clicked = False
    clicked_node = None
    drag = False
    alg_selected = ''

    # initiate pygame
    pygame.init()
    pygame.display.set_caption('Path Finding Visualizer')
    display = pygame.display.set_mode((param.WIDTH, param.HEIGHT+100))
    display.fill(param.CREAM)

    # Initiate and render the grid
    grid = g.Grid(display)
    grid.build_graph()

    # Initiate and draw the start and end nodes
    source = (random.randint(1, param.LIMIT-2), random.randint(1, param.LIMIT-2))
    target = (random.randint(1, param.LIMIT-2), random.randint(1, param.LIMIT-2))
    while source == target: # if the source and target are the same then re-randomize
        source = (random.randint(1, param.LIMIT-2), random.randint(1, param.LIMIT-2))
        target = (random.randint(1, param.LIMIT-2), random.randint(1, param.LIMIT-2))
    grid.graph[source].status = 'start'
    grid.graph[target].status = 'end'
    render_node(source, param.RED, display)     # render source node (red)
    render_node(target, param.GREEN, display)   # render target node (green)

    # Set up the buttons
    buttons= []

    dijk = bt.Button(param.BUFFER, param.HEIGHT + 4, param.BT_WIDTH, param.BT_HEIGHT, 'Dijkstra')
    astar = bt.Button(dijk.xpos + param.BT_WIDTH + param.BUFFER, param.HEIGHT + 4, \
        param.BT_WIDTH, param.BT_HEIGHT, 'A*')
    greedy = bt.Button(astar.xpos + param.BT_WIDTH + param.BUFFER, param.HEIGHT + 4, \
        param.BT_WIDTH, param.BT_HEIGHT, 'Greedy')
    dfs = bt.Button(greedy.xpos + param.BT_WIDTH + param.BUFFER, param.HEIGHT + 4, \
        param.BT_WIDTH, param.BT_HEIGHT, 'DFS')
    randmaze = bt.Button(param.BUFFER, param.HEIGHT+param.BT_HEIGHT+8, \
        param.BT_WIDTH, param.BT_HEIGHT, 'Random Obstacles')
    recursive = bt.Button(randmaze.xpos + param.BT_WIDTH + param.BUFFER, \
        param.HEIGHT+param.BT_HEIGHT+8, param.BT_WIDTH, param.BT_HEIGHT, 'Recursive Maze')
    reset = bt.Button(recursive.xpos + param.BT_WIDTH + param.BUFFER, \
        param.HEIGHT+param.BT_HEIGHT+8, param.BT_WIDTH, param.BT_HEIGHT, 'Reset')
    escape = bt.Button(reset.xpos + param.BT_WIDTH + param.BUFFER, param.HEIGHT+param.BT_HEIGHT+8, \
        param.BT_WIDTH, param.BT_HEIGHT, 'Quit')

    buttons.append(dijk)
    buttons.append(astar)
    buttons.append(greedy)
    buttons.append(dfs)
    buttons.append(randmaze)
    buttons.append(recursive)
    buttons.append(reset)
    buttons.append(escape)

    # draw the buttons
    for bts in buttons:
        bts.render(display)

    # start the game
    game_exit = False
    while not game_exit:
        # Get the mouse position
        mousepos = pygame.mouse.get_pos()

        # Activate buttons
        for bts in buttons:
            bts.enable(*mousepos, display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the application
                print('Shutting down...')
                pygame.quit()
                sys.exit()

            # Click functionalities (set source and target nodes, drag walls, buttons)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (xpos, ypos) = (mousepos[0] // param.NODE_SIZE, mousepos[1] // param.NODE_SIZE)
                if event.button == 1 and mousepos[1] < param.LIMIT * param.NODE_SIZE:
                    cell_num = (mousepos[0] // param.NODE_SIZE, mousepos[1] // param.NODE_SIZE)

                    if cell_num in (source, target):
                        clicked = True
                        clicked_node = cell_num

                elif event.button == 1:     # button management
                    algorithms = [dijk, astar, greedy, dfs]
                    other_functions = [randmaze, recursive, reset, escape]
                    for alg in algorithms:      # loop through algorithms
                        if alg.ypos < mousepos[1] < alg.ypos + alg.height and \
                            alg.xpos < mousepos[0] < alg.xpos + alg.width:

                            clear_path(grid.graph, display)   # clear the previous results

                            # compute the solution
                            solution = -1
                            if alg == dijk:
                                solution = grid.dijkstra(source, target)
                                alg_selected = 'dijk'
                            elif alg == astar:
                                solution = grid.astar(source, target)
                                alg_selected = 'astar'
                            elif alg == greedy:
                                solution = grid.greedy(source, target)
                                alg_selected = 'greedy'
                            elif alg == dfs:
                                solution = grid.dfs(source, target)
                                alg_selected = 'dfs'

                            if solution != -1:
                                # render in the blocks for the path found
                                render_path(source, target, solution, display)

                    for func in other_functions:    # loop through other functions
                        if func.ypos < mousepos[1] < func.ypos + func.height and \
                            func.xpos < mousepos[0] < func.xpos + func.width:

                            if func == randmaze:
                                # generate obstacles randomly
                                clear_everything(grid.graph, display)   # resets board
                                grid.generate_obstacles()
                                alg_selected = ''
                            if func == recursive:
                                # generate a perfect maze with recursive backtracking
                                clear_everything(grid.graph, display)
                                grid.recursive_backtracking()
                                render_node(source, param.RED, display)
                                render_node(target, param.GREEN, display)
                                alg_selected = ''
                            if func == reset:
                                start()
                            if func == escape:
                                pygame.quit()
                                sys.exit()

                elif event.button == 3: # left click starts drag mode
                    drag = True

            elif event.type == pygame.MOUSEBUTTONUP:
                # update click variables
                clicked = False
                drag = False
                clicked_node = None

            elif event.type == pygame.MOUSEMOTION and drag:
                # render the walls where the mouse drags to
                (xpos, ypos) = (mousepos[0] // param.NODE_SIZE, mousepos[1] // param.NODE_SIZE)
                if xpos >= param.LIMIT or ypos >= param.LIMIT:
                    # mouse out of bounds
                    continue
                render_walls(grid, mousepos, display)

            elif event.type == pygame.MOUSEMOTION and clicked:
                # move the node if it's in source or target
                cell_num = (mousepos[0] // param.NODE_SIZE, mousepos[1] // param.NODE_SIZE)
                if cell_num[0] >= param.LIMIT or cell_num[1] >= param.LIMIT:
                    # out of bounds
                    continue
                if grid.graph[cell_num].status != 'wall' and cell_num not in (source, target):
                    # update grid status
                    grid.graph[clicked_node].status = 'empty'
                    # render new location of node
                    if clicked_node == source:
                        render_node(source, param.CREAM, display)
                        render_node(cell_num, param.RED, display)
                        clicked_node = source = cell_num
                    elif clicked_node == target:
                        render_node(target, param.CREAM, display)
                        render_node(cell_num, param.GREEN, display)
                        clicked_node = target = cell_num
                    grid.graph[source].status = 'source'
                    grid.graph[target].status = 'target'

                    # compute new solution
                    solution = -1
                    if alg_selected == 'dijk':
                        clear_path(grid.graph, display)
                        solution = grid.dijkstra(source, target, 1)
                    elif alg_selected == 'astar':
                        clear_path(grid.graph, display)
                        solution = grid.astar(source, target, 1)
                    elif alg_selected == 'greedy':
                        clear_path(grid.graph, display)
                        solution = grid.greedy(source, target, 1)
                    elif alg_selected == 'dfs':
                        clear_path(grid.graph, display)
                        solution = grid.dfs(source, target, 1)

                    if solution != -1:
                        render_path(source, target, solution, display, 1)

        pygame.display.update()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    start()

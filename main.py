"""
    ...
"""

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

def render_path(source, target, path, display):
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

def start():
    """
    Main function that handles the rendering and logic
    """
    # Variables for click and drag functions
    clicked = False
    drag = False
    solve = False

    # initiate pygame
    pygame.init()
    pygame.display.set_caption('Path Finding Visualizer')
    display = pygame.display.set_mode((param.WIDTH, param.HEIGHT+100))
    display.fill(param.CREAM)

    # Initiate and render the grid
    grid = g.Grid(display)
    grid.build_graph()

    # Initiate and draw the start and end nodes
    source = (random.randint(0, param.LIMIT-1), random.randint(0, param.LIMIT-1))
    target = (random.randint(0, param.LIMIT-1), random.randint(0, param.LIMIT-1))
    while source == target: # if the source and target are the same then re-randomize
        source = (random.randint(0, param.LIMIT-1), random.randint(0, param.LIMIT-1))
        target = (random.randint(0, param.LIMIT-1), random.randint(0, param.LIMIT-1))
    grid.graph[source].status = 'start'
    grid.graph[target].status = 'end'
    render_node(source, param.RED, display)     # render source node (red)
    render_node(target, param.DRK_GREEN, display)   # render target node (green)

    # Draw buttons
    solve_d = bt.Button(15, param.HEIGHT+15, 250, 75, 'Solve')
    reset = bt.Button(635, param.HEIGHT+4, (param.LIMIT/5)*param.NODE_SIZE, 45, 'Reset')
    escape = bt.Button(635, param.HEIGHT+reset.height+6, \
        (param.LIMIT/5)*param.NODE_SIZE, 45, 'Quit')
    solve_d.render(display)
    reset.render(display)
    escape.render(display)

    # start the game
    game_exit = False
    while not game_exit:
        # Get the mouse position
        mousepos = pygame.mouse.get_pos()
        # Activate button
        solve_d.enable(*mousepos, display)
        reset.enable(*mousepos, display)
        escape.enable(*mousepos, display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the application
                print('Shutting down...')
                pygame.quit()
                quit()

            # Click functionalities (set source and target nodes, drag walls, buttons)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (xpos, ypos) = (mousepos[0] // param.NODE_SIZE, mousepos[1] // param.NODE_SIZE)
                if event.button == 1 and mousepos[1] < param.HEIGHT:
                    # TODO: add functionality to adjust start and end nodes
                    clicked = True
                    if clicked:
                        print('clicked:', (xpos, ypos))
                        grid_num = convert2single(xpos, ypos)
                        print('corresponding grid number:', grid_num)
                        print('status:', grid.graph[xpos, ypos].status)
                elif event.button == 1:     # button management
                    if solve_d.ypos < mousepos[1] < solve_d.ypos+solve_d.height and \
                        solve_d.xpos < mousepos[0] < solve_d.xpos+solve_d.width:
                        # this region is within the solve button
                        solve = True
                    if reset.ypos < mousepos[1] < reset.ypos+reset.height and \
                        reset.xpos < mousepos[0] < reset.xpos+reset.width:
                        # this region is within the reset button
                        start()
                    if escape.ypos < mousepos[1] < escape.ypos+escape.height and \
                        escape.xpos < mousepos[0] < escape.xpos+escape.width:
                        # this region is within the quit button
                        pygame.quit()
                        quit()
                elif event.button == 3: # left click starts drag mode
                    drag = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if solve:
                    solution = grid.a_star(source, target)
                    if solution != -1:
                        # render in the blocks for the path found
                        render_path(source, target, solution[0], display)
                    else:
                        print('No path found!')

                # update click variables
                solve = False
                clicked = False
                drag = False

            elif event.type == pygame.MOUSEMOTION and drag:
                # render the walls where the mouse drags to
                (xpos, ypos) = (mousepos[0] // param.NODE_SIZE, mousepos[1] // param.NODE_SIZE)
                if xpos >= param.LIMIT or ypos >= param.LIMIT:
                    # mouse out of bounds
                    continue
                render_walls(grid, mousepos, display)

        pygame.display.update()
    pygame.quit()
    quit()

if __name__ == '__main__':
    start()

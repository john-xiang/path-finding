"""
    ...
"""

import time
import pygame
import grid as g
import colour as col
import button

# Define width and height
WIDTH = 800
HEIGHT = 800
NODE_SIZE = 40
LIMIT = int(WIDTH/NODE_SIZE)
FONT_PATH = '/home/johnx/Projects/path-finding/font/OpenSans-Semibold.ttf'


def convert2single(xpos, ypos):
    """
        Helper function that converts an (x,y) coordinate to a
        single number using the formula y * MAXY + x
    """
    return ypos * LIMIT + xpos


def convert2xy(num):
    """
        Helper function that converts a single number to an
        (x,y) coordinate. X is computed by num % MAXY and Y
        is computed by num / MAXY
    """
    x_pos = num % LIMIT
    y_pos = num / LIMIT
    return (x_pos, y_pos)


def render_walls(graph, mousepos, display):
    """
        This function renders the walls onto the display
    """
    (xpos, ypos) = (int(mousepos[0]/NODE_SIZE), int(mousepos[1]/NODE_SIZE))

    # only colour empty nodes within the grid
    if graph.graph[xpos, ypos].status == 'empty' and mousepos[1] < HEIGHT:
        # locate the top left corner position of the square
        xstart = ((xpos) * NODE_SIZE) + 1
        ystart = ((ypos) * NODE_SIZE) + 1
        # colour in the obstacle
        pygame.draw.rect(display, col.BLACK, [xstart, ystart, NODE_SIZE-1, NODE_SIZE-1])
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
        xstart = (node[0] * NODE_SIZE) + 1
        ystart = (node[1] * NODE_SIZE) + 1
        # colour in the path
        pygame.draw.rect(display, col.YELLOW, [xstart, ystart, NODE_SIZE-1, NODE_SIZE-1])
        time.sleep(0.05)
        pygame.display.update()


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
    display = pygame.display.set_mode((WIDTH, HEIGHT+100))
    display.fill(col.CREAM)
    button_font = pygame.font.Font(FONT_PATH, 20)

    # Initiate and render the grid
    grid = g.Grid(display, NODE_SIZE, WIDTH)
    grid.render_grid()
    # Initiate and draw the start and end nodes
    source = (0, 0)
    target = (LIMIT-1, LIMIT-1)
    grid.graph[source].status = 'start'
    grid.graph[target].status = 'end'
    pygame.draw.rect(display, col.RED, [1, 1, NODE_SIZE-1, NODE_SIZE-1]) # (x, y, width, height)
    pygame.draw.rect(display, col.GREEN, [HEIGHT-NODE_SIZE+1, WIDTH-NODE_SIZE+1, NODE_SIZE-1, NODE_SIZE-1])

    # Draw buttons
    solve_d = button.Button(15, HEIGHT+15, button_font)
    reset = button.Button(635, HEIGHT+4, button_font, width=4*NODE_SIZE, height=45)
    escape = button.Button(635, HEIGHT+reset.height+6, button_font, width=4*NODE_SIZE, height=45)
    solve_d.render(display)
    reset.render(display)
    escape.render(display)

    # start the game
    game_exit = False
    while not game_exit:
        # Get the mouse position
        mousepos = pygame.mouse.get_pos()
        # Activate button
        solve_d.activate(mousepos[0], mousepos[1], display)
        reset.reset(mousepos[0], mousepos[1], display)
        escape.quit(mousepos[0], mousepos[1], display)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the application
                print('Shutting down...')
                pygame.quit()
                quit()

            # Click functionalities (set source and target nodes, drag walls, buttons)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (xpos, ypos) = (int(mousepos[0]/NODE_SIZE), int(mousepos[1]/NODE_SIZE))
                if event.button == 1 and mousepos[1] < HEIGHT:   # right click sets start/end nodes
                    # TODO: add functionality to adjust start and end nodes
                    clicked = True
                    if clicked:
                        print('clicked:', (xpos, ypos))
                        grid_num = convert2single(xpos, ypos)
                        print('corresponding grid number:', grid_num)
                        print('status:', grid.graph[xpos, ypos].status)
                elif event.button == 1:     # button management
                    if solve_d.ypos < mousepos[1] < solve_d.ypos+solve_d.height and solve_d.xpos < mousepos[0] < solve_d.xpos+solve_d.width:
                        # this region is within the solve button
                        solve = True
                    if reset.ypos < mousepos[1] < reset.ypos+reset.height and reset.xpos < mousepos[0] < reset.xpos+reset.width:
                        # this region is within the reset button
                        start()
                    if escape.ypos < mousepos[1] < escape.ypos+escape.height and escape.xpos < mousepos[0] < escape.xpos+escape.width:
                        # this region is within the quit button
                        pygame.quit()
                        quit()
                elif event.button == 3: # left click starts drag mode
                    drag = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if solve:
                    solution = grid.dijkstra(source, target)
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
                (xpos, ypos) = (int(mousepos[0]/NODE_SIZE), int(mousepos[1]/NODE_SIZE))
                if xpos >= LIMIT or ypos >= LIMIT:
                    # mouse out of bounds
                    continue
                render_walls(grid, mousepos, display)

        pygame.display.update()
    pygame.quit()
    quit()

if __name__ == '__main__':
    start()

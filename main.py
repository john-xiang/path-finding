"""
    ...
"""

import pygame
import grid as g
import colour as col
#import dijkstra

# Define width and height
WIDTH = 800
HEIGHT = 800
NODE_SIZE = 40
LIMIT = int(WIDTH/NODE_SIZE)


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


def start():
    """
        Main function that handles the rendering and logic
    """
    # Variables for click and drag functions
    clicked = False
    drag = False

    # initiate pygame
    pygame.init()
    pygame.display.set_caption('Path Finding Visualizer')
    display = pygame.display.set_mode((WIDTH, HEIGHT+100))
    display.fill(col.CREAM)

    # Initiate and render the grid
    grid = g.Grid(display, NODE_SIZE, WIDTH)
    grid.render_grid()
    # Initiate and draw the start and end nodes
    grid.graph[0].status = 'start'
    grid.graph[LIMIT*LIMIT-1].status = 'end'
    pygame.draw.rect(display, col.RED, [1, 1, NODE_SIZE-1, NODE_SIZE-1]) # (x, y, width, height)
    pygame.draw.rect(display, col.GREEN, [761, 761, NODE_SIZE-1, NODE_SIZE-1])

    # Draw buttons
    pygame.draw.rect(display, col.GREY, [15, HEIGHT+15, 250, 75])
    # gameTime = pygame.time.Clock()
    game_exit = False

    while not game_exit:
        # Get the mouse position
        mousepos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the application
                print('Shutting down...')
                game_exit = True

            # Left click enables drag mode for building obstacles
            #   right click sets the start and end nodes
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (xpos, ypos) = (int(mousepos[0]/NODE_SIZE), int(mousepos[1]/NODE_SIZE))
                if event.button == 1 and mousepos[1] < HEIGHT:   # right click sets start and end nodes
                    clicked = True
                    if clicked:
                        print('clicked', (xpos, ypos))
                        grid_num = convert2single(xpos, ypos)
                        print('corresponding grid number: ', grid_num)
                elif event.button == 3: # left click starts drag mode
                    drag = True

            elif event.type == pygame.MOUSEBUTTONUP:
                clicked = False
                drag = False

            elif event.type == pygame.MOUSEMOTION and drag:
                (xpos, ypos) = (int(mousepos[0]/NODE_SIZE), int(mousepos[1]/NODE_SIZE))
                # convert positions to (x,y) coordinates
                index = convert2single(xpos, ypos)
                # only colour empty nodes witin the grid
                if grid.graph[index].status == 'empty' and mousepos[1] < HEIGHT:
                    # locate the top left corner position of the square
                    xstart = ((xpos) * NODE_SIZE) + 1
                    ystart = ((ypos) * NODE_SIZE) + 1
                    # colour in the obstacle
                    pygame.draw.rect(display, col.BLACK, [xstart, ystart, NODE_SIZE-1, NODE_SIZE-1])
                    # change the status of nodes that have become obstacles ('wall')
                    grid.graph[index].status = 'wall'

        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    start()

"""
    ...
"""

import pygame
import grid as g

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CREAM = (244, 244, 228)
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
        ...
    """
    pygame.init()
    pygame.display.set_caption('Path Finding Visualizer')
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    display.fill(CREAM)

    #############
    grid = g.Grid(display, NODE_SIZE, WIDTH)
    grid.render_grid()
    ##############

    # gameTime = pygame.time.Clock()
    game_exit = False

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the application
                print('Shutting down...')
                game_exit = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                (xpos, ypos) = pygame.mouse.get_pos()
                (xpos, ypos) = (int(xpos/NODE_SIZE), int(ypos/NODE_SIZE))

                print('clicked', (xpos, ypos))
                grid_num = convert2single(xpos, ypos)
                print('corresponding grid number: ', grid_num)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    start()

"""
    Handles the functionality of all buttons.
    Each button will need x, y, z, w
"""

import pygame
import colour as col

class Button:
    """
        Button class
    """
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.width = 250
        self.height = 75
        self.colour = col.GREY
        self.act_colour = col.LIGHT_GREY
        self.message = ''

    def quit(self, xpos, ypos, display):
        """
            Function which handles the QUIT button
        """
        self.message = 'Quit'
        self.width = 250
        self.height = 75
        self.colour = col.GREY
        self.act_colour = col.LIGHT_GREY

    def dijkstra(self, x_pos, y_pos, display):
        """
            Function which starts dijkstra on the current grid
        """
        self.message = 'Dijkstra'

        # button interactions
        if self.xpos < x_pos < self.xpos + self.width and self.ypos < y_pos < self.ypos+self.height:
            pygame.draw.rect(display, col.LIGHT_GREY, [self.xpos, self.ypos, self.width, self.height])
        else:
            pygame.draw.rect(display, col.GREY, [self.xpos, self.ypos, self.width, self.height])
"""
    Handles the functionality of all buttons.
    Each button will need x, y, z, w
"""

import pygame
import colour as col

def text_object(text, font):
    """
        Function returns the text to render and the rectangle it covers
    """
    textsurface = font.render(text, True, col.BLACK)
    return textsurface, textsurface.get_rect()

class Button:
    """
        Button class
    """
    def __init__(self, xpos, ypos, font):
        self.xpos = xpos
        self.ypos = ypos
        self.font = font
        self.width = 250
        self.height = 75
        self.message = ''

    def render(self, display):
        """
            Renders the button onto the display
        """
        pygame.draw.rect(display, col.GREY, [self.xpos, self.ypos, self.width, self.height])

    # def quit(self, xpos, ypos, display):
    #     """
    #         Function which handles the QUIT button
    #     """
    #     self.message = 'Quit'
    #     self.width = 250
    #     self.height = 75
    #     self.colour = col.GREY
    #     self.act_colour = col.LT_GREY

    def activate(self, x_pos, y_pos, display, action=None):
        """
            Function which starts dijkstra on the current grid
        """
        self.message = 'Solve'
        # create a text object which is a tuple containing the text and the
        #   surface to render on
        text = text_object(self.message, self.font)
        text[1].center = ((self.xpos+(self.width/2)), (self.ypos+(self.height/2)))

        # activates the button if mouse is within boundaries
        if self.xpos < x_pos < self.xpos + self.width and self.ypos < y_pos < self.ypos+self.height:
            pygame.draw.rect(display, col.LT_GREY, [self.xpos, self.ypos, self.width, self.height])
            display.blit(text[0], text[1])
            if action:
                print('Solving...')
        else:
            pygame.draw.rect(display, col.GREY, [self.xpos, self.ypos, self.width, self.height])
            display.blit(text[0], text[1])

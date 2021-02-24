"""
Handles the functionality of all buttons.
Each button will need x, y, width, height, message and font
"""

import pygame
import parameters as param

class Button:
    """
        Button class
    """
    def __init__(self, xpos, ypos, width, height, message=None):
        self.xpos = xpos
        self.ypos = ypos
        self.width = width
        self.height = height
        self.message = message
        self.font = param.FONT_PATH

    def render(self, display):
        """
        Renders the button onto the display
        """
        pygame.draw.rect(display, param.GREY, [self.xpos, self.ypos, self.width, self.height])

    def text_object(self, text):
        """
        Function returns the text to render and the rectangle it covers
        """
        font = pygame.font.Font(self.font, 19)
        textsurface = font.render(text, True, param.BLACK)
        return textsurface, textsurface.get_rect()

    def enable(self, mousex, mousey, display):
        """
        This function makes the button change colour when the mouse hovers
        over the defined area of the button.

        input:
            mousex: the current x position of the mouse
            mousey: the current y position of the mouse
            button: the button to be activated
            display: the main display
        """
        # create a text object which is a tuple containing the text and the
        #   surface to render on
        text = self.text_object(self.message)
        text[1].center = ((self.xpos+(self.width/2)), (self.ypos+(self.height/2)))

        # activates the button if mouse is within boundaries
        if self.xpos < mousex < self.xpos + self.width and \
            self.ypos < mousey < self.ypos + self.height:
            pygame.draw.rect(display, param.LT_GREY, \
                [self.xpos, self.ypos, self.width, self.height])
            display.blit(text[0], text[1])
        else:
            pygame.draw.rect(display, param.GREY, \
                [self.xpos, self.ypos, self.width, self.height])
            display.blit(text[0], text[1])

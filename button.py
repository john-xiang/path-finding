"""
    Handles the functionality of all buttons.
    Each button will need x, y, width, height, message and font
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
    def __init__(self, xpos, ypos, font, width=None, height=None):
        self.xpos = xpos
        self.ypos = ypos
        self.font = font
        if not width:
            self.width = 250
        else:
            self.width = width
        if not height:
            self.height = 75
        else:
            self.height = height
        self.message = ''

    def render(self, display):
        """
            Renders the button onto the display
        """
        pygame.draw.rect(display, col.GREY, [self.xpos, self.ypos, self.width, self.height])

    def quit(self, mousex, mousey, display):
        """
            Function which handles the QUIT button
        """
        self.message = 'Quit'
        # create a text object which is a tuple containing the text and the
        #   surface to render on
        text = text_object(self.message, self.font)
        text[1].center = ((self.xpos+(self.width/2)), (self.ypos+(self.height/2)))

        # activates the button if mouse is within boundaries
        if self.xpos < mousex < self.xpos+self.width and self.ypos < mousey < self.ypos+self.height:
            pygame.draw.rect(display, col.LT_GREY, [self.xpos, self.ypos, self.width, self.height])
            display.blit(text[0], text[1])
        else:
            pygame.draw.rect(display, col.GREY, [self.xpos, self.ypos, self.width, self.height])
            display.blit(text[0], text[1])

    def reset(self, mousex, mousey, display):
        """
            Funtion which handles the reset button
        """
        self.message = 'Reset'
        # create a text object which is a tuple containing the text and the
        #   surface to render on
        text = text_object(self.message, self.font)
        text[1].center = ((self.xpos+(self.width/2)), (self.ypos+(self.height/2)))

        # activates the button if mouse is within boundaries
        if self.xpos < mousex < self.xpos+self.width and self.ypos < mousey < self.ypos+self.height:
            pygame.draw.rect(display, col.LT_GREY, [self.xpos, self.ypos, self.width, self.height])
            display.blit(text[0], text[1])
        else:
            pygame.draw.rect(display, col.GREY, [self.xpos, self.ypos, self.width, self.height])
            display.blit(text[0], text[1])

    def activate(self, mousex, mousey, display):
        """
            Function which activates the selected solve method on the grid

            NOTE: The mousex argument is the current mouse x position and is different
                from self.xpos which is the x position of the button. Same goes for mousey.
        """
        self.message = 'Find Path'
        # create a text object which is a tuple containing the text and the
        #   surface to render on
        text = text_object(self.message, self.font)
        text[1].center = ((self.xpos+(self.width/2)), (self.ypos+(self.height/2)))

        # activates the button if mouse is within boundaries
        if self.xpos < mousex < self.xpos+self.width and self.ypos < mousey < self.ypos+self.height:
            pygame.draw.rect(display, col.LT_GREY, [self.xpos, self.ypos, self.width, self.height])
            display.blit(text[0], text[1])
        else:
            pygame.draw.rect(display, col.GREY, [self.xpos, self.ypos, self.width, self.height])
            display.blit(text[0], text[1])

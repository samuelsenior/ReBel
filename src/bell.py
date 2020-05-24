import pygame

import os
import sys

class Bell:
    '''
    The Bell object displays the image of a bell, along with its given bell
    number. It also stores the key value that is used to ring the bell and
    updates the bell from handstroke to backstroke, and visa versa, when the
    key is pressed to ring the bell.

    Parameters
    ----------
    bellNumber : int
        The number of the bell.

    location : (int, int)
        The (x, y) coordinate of the top most left position of the bell image.
    
    bellImageFile : string
        The file name and location of the bell image.

    width : int
        The width of the bell image.

    height : int
        The height of the bell image.

    textLocation : (int, int)
        The (x, y) coordinate of the top most left position of the bell number text.

    font : Font
        An initialised Font instance.

    stroke : string
        The stroke of the bell, either 'H' for 'handstroke' or 'B' for
        backstroke.

    key : pygame key
        The pygame key used to ring the bell.

    backgroundColour : (int, int, int)
        A tuple of the RGB vales of the ringing screen background colour.
    '''
    def __init__(self, bellNumber, location, bellImageFile, width, height, textLocation, font, stroke='H', key=None, backgroundColour=(255, 255, 255)):
        # Set the working directory based on if ReBel is being run from an
        # executable or the Python source code.
        if getattr(sys, 'frozen', False):
            # In a bundle
            self.exeDir = os.path.dirname(sys.executable)
        else:
            # In normal python
            self.exeDir = ""

        self.font = font
        self.stroke = stroke

        # Set the width and height of the bell image.
        self.width = width
        self.height = height
        self.backgroundColour = backgroundColour

        # Read in bell image and create handstroke and backstroke images from
        # it. The backstroke image being a rotation and flip of the handstroke
        # image. 'Blanks' are also made and are used to 'erase' the previous
        # stroke when updating to the new stroke so that artifacts do not
        # remain.
        bell = pygame.image.load(bellImageFile)
        self.handstrokeBell = pygame.transform.scale(bell, (self.width, self.height))
        self.handstrokeBellBlank = self.handstrokeBell.copy()
        self.handstrokeBellBlank.fill(self.backgroundColour)
        self.backstrokeBell = pygame.transform.scale(bell, (self.width, self.height))
        self.backstrokeBell = pygame.transform.rotate(self.backstrokeBell, -90.0)
        self.backstrokeBell = pygame.transform.flip(self.backstrokeBell, True, False)
        self.backstrokeBellBlank = self.backstrokeBell.copy()
        self.backstrokeBellBlank.fill(self.backgroundColour)

        # Location of the bell, with the (x, y) coordinates corresponding to
        # the top most left part of the bell image.
        self.x = location[0]
        self.y = location[1]

        # Location of the bell number text, with the (x, y) coordinates
        # corresponding to the top most left part of the bell number text.
        self.textX = textLocation[0]
        self.textY = textLocation[1]

        self.bellNumber = bellNumber
        self.bellNumberText = self.font.FONT.render(str(self.bellNumber), True, (0, 0, 0))
        self.bellNumberTextBlank = pygame.Rect(self.textX, self.textY, self.bellNumberText.get_width(), self.bellNumberText.get_height())

        self.key = key

    def fill(self, surface, colour):
        '''
        Fills a pygame surface with a given colour.

        Parameters
        ----------
        surface : pygame.surface
            The pygame surface to be filled.

        colour : (int, int, int)
            A tuple of the RGB vales of the desired surface colour.
        '''
        surface.fill(colour)

    def setKey(self, key):
        '''
        Sets the key that the bell is rung with.

        Parameters
        ----------

        key : pygame key
            The pygame key value that the bell is rung with.
        '''
        self.key = key

    def clearKey(self):
        '''
        Clears the current key value that the bell is rung with.
        '''
        self.key = None

    def updateLocation(self, x, y, textX, textY):
        '''
        Updates the locations of the bell and associated bell number text.

        Parameters
        ----------
        x : int
            The x-position of the left most point of the bell image.

        y : int
            The y-position of the top most point of the bell image.

        textX : int
            The x-position of the left most point of the bell number text.

        textY : int
            The y-position of the top most point of the bell number text.
        '''
        self.x = x
        self.y = y
        self.textX = textX
        self.textY = textY

        # Update the position of the 'blank' bell image too.
        self.bellNumberTextBlank = pygame.Rect(self.textX, self.textY, self.bellNumberText.get_width(), self.bellNumberText.get_height())

    def draw(self, win, renderNumber=True):
        '''
        Draws the bell image and bell number text to the screen, with the bell
        stroke being drawn corresponding to the current value of the internal
        'stroke' variable.

        Parameters
        ----------
        win : pygame.display
            The pygame display window.

        renderNumber : bool
            The flag to decide whether to draw the bell number text.
        '''
        if self.stroke == 'H':
            win.blit(self.backstrokeBellBlank, (self.x, self.y))
            win.blit(self.handstrokeBell, (self.x, self.y))
        else:
            win.blit(self.handstrokeBellBlank, (self.x, self.y))
            win.blit(self.backstrokeBell, (self.x, self.y))
        if renderNumber:
            pygame.draw.rect(win, self.backgroundColour, self.bellNumberTextBlank, 0)
            win.blit(self.bellNumberText, (self.textX, self.textY))

    def handle_event(self, send):
        '''
        The event handler that sends a message to the server saying the bell
        has been rung.

        Parameters
        ----------
        send : Client.send
            The Client function used to send messages to the server.
        '''
        send("R:" + self.stroke + str(self.bellNumber))

    def bellRung(self, stroke):
        '''
        Changes the current stroke of the bell to the opposite value of the
        stroke passed in.

        Parameters
        ----------
        stroke : string
            The current stroke value of the bell.
        '''
        self.stroke = 'B' if stroke == 'H' else 'H'
        
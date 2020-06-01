import pygame

from button import Button
from textBox import TextBox

class AboutScreen:
    '''
    The AboutScreen object displays an About screen with About information.
    It contains the needed text, the position and dimenions of the about screen,
    as well as a background fade for the previous screen and a background for
    the About screen.

    Parameters
    ----------
    win : pygame.display
        The pygame display window.

    font : Font
        A Font object instance.

    frameRate : int
        The frame rate at which the pygame display is updated.

    version : string
        The version of ReBel.
    '''
    def __init__(self, win, font, frameRate, version):
        self.win = win
        self.font = font
        self.frameRate = frameRate
        self.version = version

        # Set the width and the height of the About screen to 80% of the main window.
        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        # In the AboutScreen frame of reference x and y would both be 0 though their
        # positions are needed in terms of the main screen reference frame. Therefore
        # calculate them in terms of main screen reference frame.
        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        # Generate the background fade so that the previous screen will be faded to
        # show the focus is no longer on it. Fade done via a white surface with an
        # alpha channel.
        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        # Generate the background of the AboutScreen.
        self.aboutBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)

        # Generate the buttons present.
        self.button_back = Button("Back", (self.x + 20, self.height + self.y - 20), font=self.font)
        self.button_back.rect.y -= self.button_back.rect.h
        self.buttons = [self.button_back]

        # Generate the text of the AboutScreen. Each text box has word wrapping and
        # takes the height and y-position of the previous text box, plus an extra
        # y-spacing of 10, to give its y-position.
        self.aboutTitleText = TextBox('About:',
                                       (self.x+20, self.y+20), width=self.width-40, backgroundColour=(150, 150, 150), font=self.font, fontSize='large')
        self.aboutText_1 = TextBox("ReBel version {}".format(self.version[1:]),
                                   (self.x+20, self.aboutTitleText.y+self.aboutTitleText.h+7), width=self.width-40, font=self.font, fontSize='small')
        self.aboutText_2 = TextBox("ReBel is a client-server-based multiuser online ringing software. Developed by Samuel M. Senior and " + \
                                   "open-sourced using the BSD-3-Clause license.",
                                   (self.x+20, self.aboutText_1.y+self.aboutText_1.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.aboutText_3 = TextBox("Source code can be downloaded from 'https://github.com/samuelsenior/ReBel'.",
                                   (self.x+20, self.aboutText_2.y+self.aboutText_2.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.aboutText_4 = TextBox("The latest release can be downloaded from 'https://github.com/samuelsenior/ReBel/releases'.",
                                   (self.x+20, self.aboutText_3.y+self.aboutText_3.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.aboutText = [self.aboutTitleText, self.aboutText_1, self.aboutText_2, self.aboutText_3, self.aboutText_4]

    def drawBackground(self, display):
        '''
        Draws the background of the AboutScreen with a border line drawn around
        it too.

        Parameters
        ----------
        display : Display
            The Display instance used for displaying to the screen.
        '''
        display.draw.rect((170, 170, 170), self.aboutBackground, 0)
        display.draw.rect((100, 100, 100), self.aboutBackground, 2)

    def display(self, display, source):
        '''
        Displays the AboutScreen.

        Parameters
        ----------
        display : Display
            The display instance used for displaying to the screen.

        source : string
            The name of the screen type from where the user is coming from.

        '''
        self.win = display.win

        # Set the width and the height of the About screen to 80% of the main window.
        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        # Generate the background fade so that the previous screen will be faded to
        # show the focus is no longer on it. Fade done via a white surface with an
        # alpha channel.
        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        # Generate the background of the AboutScreen.
        self.aboutBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)

        # In the AboutScreen frame of reference x and y would both be 0 though their
        # positions are needed in terms of the main screen reference frame. Therefore
        # calculate them in terms of main screen reference frame.
        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        # The width of the main screen, and therefore the AboutScreen, could have
        # changed since the text generation. This means that the text needs to be
        # regenerated to fill the new width. Due to word wrapping this can change
        # the heights of each text box and so their y-positions need to be re-
        # calculated.
        for i, aboutText in enumerate(self.aboutText):
            aboutText.rect.x = self.x + 20
            if i == 0:
                startingY = aboutText.y
            else:
                startingY = self.aboutText[i-1].y + self.aboutText[i-1].h+10
            aboutText.generateFormattedText(startingY=startingY, width=self.width-40)
        # The width of the main screen could have changed, meaning the AboutScreen
        # width and x could have changed. Therefore need to update the button -
        # postions
        self.button_back.rect.x = self.x + 20

        # Apply the bakground fade to the previous screen the user is coming from
        # and draw the background of the AboutScreen.
        display.blit(self.backgroundFade, (0, 0))
        self.drawBackground(display)

        # Update the button to not being hovered over by the mouse and draw them.
        for button in self.buttons:
            if button.updated:
                button.hovered = False
                button.draw(display)

        # Draw the text to the screen.
        for txt in self.aboutText:
            txt.draw(display)

        # Update the screen to display the updated draws.
        display.flip()
        
        # Pygame clock for setting frame rate.
        clock = pygame.time.Clock()
        
        # Switch for limiting the display.flip calls to just when a display
        # update has occured.
        self.updated = True

        # Main display loop.
        run_about = True
        while run_about:
            # Get the event.
            for event in pygame.event.get():
                # If the event is a quit event then quit the display loop and
                # return 'quit' so that the main program loop can do a clean
                # quit.
                if event.type == pygame.QUIT:
                    run_about = False
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the event is a mouse down click and its position is 
                    # on the back button then return name of the previous
                    # screen so that the user goes back to that screen.
                    if self.button_back.rect.collidepoint(event.pos):
                        run_about = False
                        return source

                for button in self.buttons:
                    # If the mouse is hovering over a button then update the
                    # button to have the hovered text colour. If the button
                    # is active and is no longer being hovered over then
                    # return the text colour back to its original colour.
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                        button.updated = True
                        button.draw(display)
                        self.updated = True
                    elif button.active == True and button.hovered == True:
                        button.hovered = False
                        button.updated = True
                        button.draw(display)
                        self.updated = True

            # Update the screen to display the updated draws.
            if self.updated:
                display.flip()
                self.updated = False

            # Pause the loop until all of the frame rate time has passed.
            clock.tick(self.frameRate)

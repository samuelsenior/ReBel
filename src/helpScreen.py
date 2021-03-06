import pygame

from button import Button
from textBox import TextBox

class HelpScreen:

    def __init__(self, win, font, frameRate):
        self.win = win
        self.font = font
        self.frameRate = frameRate

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        self.helpBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)

        self.button_back = Button("Back", (self.x + 20, self.height + self.y - 20), font=self.font)
        self.button_back.rect.y -= self.button_back.rect.h
        #
        self.button_serverPage = Button("Server", (self.x + self.width - 20, self.y + 20), font=self.font)
        self.button_serverPage.rect.x -= self.button_serverPage.rect.w
        #
        self.button_ringingPage = Button("Ringing", (self.button_serverPage.x - self.button_serverPage.rect.w - 10, self.y + 20), font=self.font)
        self.button_ringingPage.rect.x -= self.button_ringingPage.rect.w
        #
        self.buttons = [self.button_back, self.button_ringingPage, self.button_serverPage]

        self.serverTitleText = TextBox('Server Help:',
                                       (self.x+20, self.y+self.button_serverPage.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font=self.font, fontSize='large')
        self.serverSubTitleText = TextBox('Connecting to a server:',
                                          (self.x+20, self.serverTitleText.y+self.serverTitleText.h+10), width=self.width-40, font=self.font, fontSize='small')
        self.serverText_1 = TextBox("In 'Your Name' enter your name.",
                                    (self.x+20, self.serverSubTitleText.y+self.serverSubTitleText.h+7), width=self.width-40, font=self.font, fontSize='tiny')
        self.serverText_2 = TextBox("In 'Server IP' enter the public IP of the server as told by the person running the server, or the local IP of the " + \
                                    "server if on the same network, or leave it blank if you are on the same machine as the one runnning the server.",
                                    (self.x+20, self.serverText_1.y+self.serverText_1.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.serverText_3 = TextBox("Leave 'Server Port' as the default value if the person running the server hasn't changed it, " + \
                                    "otherwise change it to the number they give.",
                                    (self.x+20, self.serverText_2.y+self.serverText_2.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.serverText_4 = TextBox("Once these details have been entered click 'Connect to Server'. If you are able to connect to the " + \
                                    "server successfully a 'Connected' message will appear, if not a 'Server Offline' message will appear. " +
                                    "If you can't connect make sure to check your internet connection, the server IP, and the server port.",
                                    (self.x+20, self.serverText_3.y+self.serverText_3.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.serverText_5 = TextBox("To reconnect to a server or to connect to a new one go back to the home screen, enter in the " + \
                                    "details of the new server (or leave the original details in if reconnecting), then click 'Connect " +
                                    "to Server' and then click 'Start Ringing' like normal.",
                                    (self.x+20, self.serverText_4.y+self.serverText_4.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.serverText = [self.serverTitleText, self.serverSubTitleText, self.serverText_1, self.serverText_2, self.serverText_3, self.serverText_4, self.serverText_5]

        self.ringingTitleText = TextBox('Ringing Help:',
                                        (self.x+20, self.y+self.button_serverPage.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font=self.font, fontSize='large')
        self.ringingSubTitleText_1 = TextBox('Ringing Keys:',
                                             (self.x+20, self.ringingTitleText.y+self.ringingTitleText.h+10), width=self.width-40, font=self.font, fontSize='small')
        self.ringingText_1 = TextBox("By default bells 1 and 2 are set as the ringable and are rung with the 'j' and 'f' keys.",
                                     (self.x+20, self.ringingSubTitleText_1.y+self.ringingSubTitleText_1.h+7), width=self.width-40, font=self.font, fontSize='tiny')
        self.ringingText_2 = TextBox("All the bells can be configured to be rung and can be set to use any letter or number key. The key bindings are " + \
                                     "set in the 'Options' menu found in the ringing screen.",
                                     (self.x+20, self.ringingText_1.y+self.ringingText_1.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.ringingText_3 = TextBox("The bell you set as your first bell will be placed at the bottom of the ringing circle, just to the right of the " + \
                                     "center.",
                                     (self.x+20, self.ringingText_2.y+self.ringingText_2.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.ringingSubTitleText_2 = TextBox('Bell Tunings and Scales:',
                                             (self.x+20, self.ringingText_3.y+self.ringingText_3.h+16), width=self.width-40, font=self.font, fontSize='small')
        self.ringingText_4 = TextBox("By default the bells are in the key of C and are generated from a size 15 handbell in C. The key of the bells can " + \
                                     "changed by shifting them by both an integer number of semitones and an integer number of octaves. Currently this " + \
                                     "can only be done by manually changing the config file.",
                                     (self.x+20, self.ringingSubTitleText_2.y+self.ringingSubTitleText_2.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.ringingText_5 = TextBox("The bells are tuned to a major scale by default though they can also be changed to natural, harmonic, and melodic " + \
                                     "minor scales. Currently this can only be done manually changing the config file.",
                                     (self.x+20, self.ringingText_4.y+self.ringingText_4.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        
        self.ringingText = [self.ringingTitleText, self.ringingSubTitleText_1, self.ringingText_1, self.ringingText_2, self.ringingText_3]#,
                            #self.ringingSubTitleText_2, self.ringingText_3, self.ringingText_4]

    def drawBackground(self, display):
        '''
        Draws the background of the HelpScreen with a border line drawn around
        it too.

        Parameters
        ----------
        display : Display
            The Display instance used for displaying to the screen.
        '''
        display.draw.rect((170, 170, 170), self.helpBackground, 0)
        display.draw.rect((100, 100, 100), self.helpBackground, 2)

    def display(self, display, source):
        self.win = display.win

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        self.helpBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)


        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        for i, serverText in enumerate(self.serverText):
            serverText.rect.x = self.x + 20
            if i == 0:
                startingY = serverText.y
            else:
                startingY = self.serverText[i-1].y + self.serverText[i-1].h+10
            serverText.generateFormattedText(startingY=startingY, width=self.width-40)
        for i, ringingText in enumerate(self.ringingText):
            ringingText.rect.x = self.x + 20
            if i == 0:
                startingY = ringingText.y
            else:
                startingY = self.ringingText[i-1].y + self.ringingText[i-1].h+10
            ringingText.generateFormattedText(startingY=startingY, width=self.width-40)
        self.button_back.rect.x = self.x + 20
        self.button_serverPage.rect.x = self.x + self.width - 20 - self.button_serverPage.rect.w
        self.button_ringingPage.rect.x = self.button_serverPage.rect.x - 10 - self.button_ringingPage.rect.w

        display.blit(self.backgroundFade, (0, 0))
        display.flip()

        if source == "menuScreen":
            helpPage = "server"
        elif source == "ringingScreen":
            helpPage = "ringing"
        else:
            helpPage = "ringing"

        if helpPage == "server":
            text = self.serverText
            self.button_serverPage.active = False
            self.button_ringingPage.active = True
        elif helpPage == "ringing":
            text = self.ringingText
            self.button_ringingPage.active = False
            self.button_serverPage.active = True
        else:
            text = self.ringingText
            self.button_ringingPage.active = False
            self.button_serverPage.active = True

        self.drawBackground(display)
        display.flip()

        for button in self.buttons:
            if button.updated:
                button.hovered = False
                button.draw(display)

        for txt in text:
            txt.draw(display)

        display.flip()
        
        clock = pygame.time.Clock()

        self.updated = True
        
        run_help = True
        while run_help:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_help = False
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_back.rect.collidepoint(event.pos):
                        run_help = False
                        return source
                    elif self.button_serverPage.rect.collidepoint(event.pos) and self.button_serverPage.active == True:
                        text = self.serverText
                        self.button_serverPage.active = False
                        self.button_ringingPage.active = True
                        self.drawBackground(display)
                        for button in self.buttons:
                            button.draw(display)
                        for txt in text:
                            txt.draw(display)
                        self.updated = True
                    elif self.button_ringingPage.rect.collidepoint(event.pos) and self.button_ringingPage.active == True:
                        text = self.ringingText
                        self.button_serverPage.active = True
                        self.button_ringingPage.active = False
                        self.drawBackground(display)
                        for button in self.buttons:
                            button.draw(display)
                        for txt in text:
                            txt.draw(display)
                        self.updated = True

                for button in self.buttons:
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

            if self.updated:
                display.flip()
                self.updated = False

            clock.tick(self.frameRate)

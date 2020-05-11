import pygame

from button import Button
from textBox import TextBox

class HelpScreen:

    def __init__(self, win, frameRate):
        self.win = win
        self.frameRate = frameRate

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        self.helpBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)

        self.button_back = Button("Back", (self.x + 20, self.height + self.y - 20))
        self.button_back.rect.y -= self.button_back.rect.h
        #
        self.button_serverPage = Button("Server", (self.x + self.width - 20, self.y + 20))
        self.button_serverPage.rect.x -= self.button_serverPage.rect.w
        #
        self.button_ringingPage = Button("Ringing", (self.button_serverPage.x - self.button_serverPage.rect.w - 10, self.y + 20))
        self.button_ringingPage.rect.x -= self.button_ringingPage.rect.w
        #
        self.buttons = [self.button_back, self.button_ringingPage, self.button_serverPage]

        self.serverTitleText = TextBox('Server Help:',
                                       (self.x+20, self.y+self.button_serverPage.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font='large')
        self.serverSubTitleText = TextBox('Connecting to a server:',
                                          (self.x+20, self.serverTitleText.y+self.serverTitleText.h+10), width=self.width-40, font='small')
        self.serverText_1 = TextBox("In 'Your Name' enter your name.",
                                    (self.x+20, self.serverSubTitleText.y+self.serverSubTitleText.h+7), width=self.width-40, font='tiny')
        self.serverText_2 = TextBox("In 'Server IP' enter the public IP of the server as told by the person running the server, or the local IP of the " + \
                                    "server if on the same network, or leave it blank if you are on the same machine as the one runnning the server.",
                                    (self.x+20, self.serverText_1.y+self.serverText_1.h+10), width=self.width-40, font='tiny')
        self.serverText_3 = TextBox("Leave 'Server Port' as the default value if the person running the server hasn't changed it, " + \
                                    "otherwise change it to the number they give.",
                                    (self.x+20, self.serverText_2.y+self.serverText_2.h+10), width=self.width-40, font='tiny')
        self.serverText_4 = TextBox("Once these details have been entered click 'Connect to Server'. If you are able to connect to the " + \
                                    "server successfully a 'Connected' message will appear, if not a 'Server Offline' message will appear. " +
                                    "If you can't connect make sure to check your internet connection, the server IP, and the server port.",
                                    (self.x+20, self.serverText_3.y+self.serverText_3.h+10), width=self.width-40, font='tiny')
        self.serverText = [self.serverTitleText, self.serverSubTitleText, self.serverText_1, self.serverText_2, self.serverText_3, self.serverText_4]

        self.ringingTitleText = TextBox('Ringing Help:',
                                        (self.x+20, self.y+self.button_serverPage.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font='large')
        self.ringingSubTitleText_1 = TextBox('Ringing Keys:',
                                             (self.x+20, self.ringingTitleText.y+self.ringingTitleText.h+10), width=self.width-40, font='small')
        self.ringingText_1 = TextBox("By default the keys to ring your first two bells are the 'j' and 'f' keys. All the bells can be configured to be rung, " + \
                                     "and their key bindings are set in the 'Options' menu.",
                                     (self.x+20, self.ringingSubTitleText_1.y+self.ringingSubTitleText_1.h+7), width=self.width-40, font='tiny')
        self.ringingText_2 = TextBox("The bell you set as your first bell will be placed at the bottom of the ringing circle, just to the right of the " + \
                                     "center.",
                                     (self.x+20, self.ringingText_1.y+self.ringingText_1.h+10), width=self.width-40, font='tiny')
        self.ringingSubTitleText_2 = TextBox('Bell Tunings and Scales:',
                                             (self.x+20, self.ringingText_2.y+self.ringingText_2.h+16), width=self.width-40, font='small')
        
        self.ringingText = [self.ringingTitleText, self.ringingSubTitleText_1, self.ringingText_1, self.ringingText_2, self.ringingSubTitleText_2]

    def drawBackground(self):
        pygame.draw.rect(self.win, (170, 170, 170), self.helpBackground, 0)
        pygame.draw.rect(self.win, (100, 100, 100), self.helpBackground, 2)

    def display(self, win, source):
        self.win = win

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

        self.win.blit(self.backgroundFade, (0, 0))

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

        self.drawBackground()

        for button in self.buttons:
            if button.updated:
                button.hovered = False
                button.draw(self.win)

        for txt in text:
            txt.draw(self.win)

        pygame.display.update()
        
        clock = pygame.time.Clock()
        
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
                        self.drawBackground()
                        for txt in text:
                            txt.draw(self.win)
                    elif self.button_ringingPage.rect.collidepoint(event.pos) and self.button_ringingPage.active == True:
                        text = self.ringingText
                        self.button_serverPage.active = True
                        self.button_ringingPage.active = False
                        self.drawBackground()
                        for txt in text:
                            txt.draw(self.win)

                for button in self.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                        button.updated = True
                    elif button.active == True:
                        button.hovered = False
                        button.updated = True

            for button in self.buttons:
                if button.updated:
                    button.draw(self.win)

            pygame.display.flip()
            clock.tick(self.frameRate)

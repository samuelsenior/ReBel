import pygame

from button import Button
from textBox import TextBox

class HelpScreen:

    def __init__(self, win, frameRate):
        self.win = win
        self.frameRate = frameRate

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.helpBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)

    def drawBackground(self):
        pygame.draw.rect(self.win, (150, 150, 150), self.helpBackground, 0)
        pygame.draw.rect(self.win, (100, 100, 100), self.helpBackground, 2)

    def display(self, source):

        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        s = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        s.fill((255, 255, 255, 156))
        self.win.blit(s, (0, 0))

        button_back = Button("Back", (self.x + 20, self.height + self.y - 20))
        button_back.rect.y -= button_back.rect.h
        #
        button_serverPage = Button("Server", (self.x + self.width - 20, self.y + 20))
        button_serverPage.rect.x -= button_serverPage.rect.w
        #
        button_ringingPage = Button("Ringing", (button_serverPage.x - button_serverPage.rect.w - 10, self.y + 20))
        button_ringingPage.rect.x -= button_ringingPage.rect.w
        #
        buttons = [button_back, button_ringingPage, button_serverPage]

        self.drawBackground()

        #pygame.draw.rect(self.win, (150, 150, 150), helpBackground, 0)
        #pygame.draw.rect(self.win, (100, 100, 100), helpBackground, 2)

        for button in buttons:
            if button.updated:
                button.draw(self.win)

        self.serverTitleText = TextBox('Server Help:', (self.x+20, self.y+button_serverPage.rect.h+20), backgroundColour=(150, 150, 150), font='large')
        self.serverSubTitleText = TextBox('Connecting to a server:', (self.x+20, self.serverTitleText.y+self.serverTitleText.h), font='small')
        self.serverText_1 = TextBox("In 'Your Name' enter your name.", (self.x+20, self.serverSubTitleText.y+self.serverSubTitleText.h*1.25), font='tiny')
        self.serverText_2 = TextBox("In 'Server IP' enter the public IP of the server as told by the person running", (self.x+20, self.serverText_1.y+self.serverText_1.h*1.5), font='tiny')
        self.serverText_3 = TextBox("the server, or the local IP of the server if on the same network, or leave it", (self.x+20, self.serverText_2.y+self.serverText_2.h), font='tiny')
        self.serverText_4 = TextBox("blank if you are on the same machine as the one runnning the server.", (self.x+20, self.serverText_3.y+self.serverText_3.h), font='tiny')
        self.serverText_5 = TextBox("Leave 'Server Port' as the default value if the person running the server", (self.x+20, self.serverText_4.y+self.serverText_4.h*1.5), font='tiny')
        self.serverText_6 = TextBox("hasn't changed it, otherwise change it to the number they give.", (self.x+20, self.serverText_5.y+self.serverText_5.h), font='tiny')
        self.serverText_7 = TextBox("Once these details have been entered click 'Connect to Server'. If you are", (self.x+20, self.serverText_6.y+self.serverText_6.h*1.5), font='tiny')
        self.serverText_8 = TextBox("able to connect to the server successfully a 'Connected' message will", (self.x+20, self.serverText_7.y+self.serverText_7.h), font='tiny')
        self.serverText_9 = TextBox("appear, if not a 'Server Offline' message will appear. If you can't connect", (self.x+20, self.serverText_8.y+self.serverText_8.h), font='tiny')
        self.serverText_10 = TextBox("make sure to check your internet connection, the server IP, and the server", (self.x+20, self.serverText_9.y+self.serverText_9.h), font='tiny')
        self.serverText_11 = TextBox("port.", (self.x+20, self.serverText_10.y+self.serverText_10.h), font='tiny')

        serverText = [self.serverTitleText,
                      self.serverSubTitleText, self.serverText_1, self.serverText_2, self.serverText_3, self.serverText_4, self.serverText_5, self.serverText_6,
                      self.serverText_7, self.serverText_8, self.serverText_9, self.serverText_10, self.serverText_11]

        self.ringingTitleText = TextBox('Ringing Help:', (self.x+20, self.y+button_serverPage.rect.h+20), backgroundColour=(150, 150, 150), font='large')
        self.ringingSubTitleText = TextBox('Ringing Keys:', (self.x+20, self.ringingTitleText.y+self.ringingTitleText.h), font='small')
        
        ringingText = [self.ringingTitleText,
                       self.ringingSubTitleText]


        helpPage = "server"


        if helpPage == "server":
            text = serverText
            button_serverPage.active = False
        else:# helpPage == "ringing":
            text = ringingText
            button_ringingPage.active = False

        for txt in text:
            txt.draw(self.win)

        pygame.display.update()
        
        clock = pygame.time.Clock()
        
        run_help = True
        while run_help:

            for button in buttons:
                if button.updated:
                    button.draw(self.win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_help = False
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_back.rect.collidepoint(event.pos):
                        run_help = False
                        break

                    if button_serverPage.rect.collidepoint(event.pos) and button_serverPage.active == True:
                        text = serverText
                        button_serverPage.active = False
                        button_ringingPage.active = True
                        self.drawBackground()
                        for txt in text:
                            txt.draw(self.win)
                    elif button_ringingPage.rect.collidepoint(event.pos) and button_ringingPage.active == True:
                        text = ringingText
                        button_serverPage.active = True
                        button_ringingPage.active = False
                        self.drawBackground()
                        for txt in text:
                            txt.draw(self.win)

                for button in buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                        button.updated = True
                    elif button.active == True:
                        button.hovered = False
                        button.updated = True
                        button.draw(self.win)

            pygame.display.flip()
            clock.tick(self.frameRate)

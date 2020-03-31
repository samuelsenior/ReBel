"""
ReBel v0.0.2
author: S. M. Senior
"""

import pygame
import os

from client import Network

from font import Font
from titledInputBox import TitledInputBox
from button import Button
from keyPress import KeyPress
from bell import Bell
from config import Config

        
class Rebel(Font, KeyPress):
    def __init__(self, menuWidth, menuHeight, mainWidth, mainHeight, configFile='config.txt'):

        super().__init__()

        self.menuWidth = menuWidth
        self.menuHeight = menuHeight

        self.mainWidth = mainWidth
        self.mainHeight = mainHeight

        self.configFile = configFile

        pygame.init()
        self.win = pygame.display.set_mode((self.menuWidth, self.menuHeight))
        pygame.display.set_caption("ReBel")

        self.menuBackground = pygame.image.load(os.path.join("img", "menuBackground.png"))
        self.mainBackground = pygame.image.load(os.path.join("img", "mainBackground.png"))

        self.offlineMessage = self.smallFont.render("Server offline, try again later...", 1, (255, 0, 0))
        self.connectingMessage = self.smallFont.render("Connecting to server...", 1, (50, 50, 50))
        self.connectedMessage = self.smallFont.render("Connected to server!", 1, (0, 255, 0))

        self.userName = ""
        self.serverIP = ""
        self.serverPort = None

        self.config = Config(fileName=self.configFile)

        self.frameRate = 25

        self.network = Network(frameRate=self.frameRate)

    def start(self):
        self.menuScreen()

    def menuScreen(self):
        run_menu = True
        offline = False
        self.connection = None

        clock = pygame.time.Clock()
        self.inputBox_userName = TitledInputBox("Your Name:", 150, 350, 140, 32)
        self.inputBox_serverIP = TitledInputBox("Server IP:", 150, 400, 140, 32)
        self.inputBox_serverPort = TitledInputBox("Server Port:", 150, 450, 140, 32)
        self.input_boxes = [self.inputBox_userName, self.inputBox_serverIP, self.inputBox_serverPort]

        self.button_serverConnect = Button("Connect to server", (20, 550))
        self.button_startRinging = Button("Start ringing", (20, 600), active=False)
        self.button_quit = Button("Quit", (20, 650))
        buttons = [self.button_serverConnect, self.button_startRinging, self.button_quit]

        self.connectionActive = False

        while run_menu:
            self.win.blit(self.menuBackground, (0, 0))

            if offline:
                self.win.blit(self.offlineMessage, (self.button_serverConnect.width+25, 557))
            elif self.connection == "connecting":
                self.win.blit(self.connectingMessage, (self.button_serverConnect.width+25, 557))
            elif self.connection == "connected":
                self.win.blit(self.connectedMessage, (self.button_serverConnect.width+25, 557))

            for box in self.input_boxes:
                box.draw(self.win)

            for button in buttons:
                button.draw(self.win)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_menu = False
                    self.network.send("clientDisconnect:Disconnecting")
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_serverConnect.rect.collidepoint(event.pos) and self.connectionActive == False:
                        offline = False
                        try:
                            self.connection = "connecting"
                            if self.connection == "connecting":
                                self.win.blit(self.connectingMessage, (self.button_serverConnect.width+25, 557))

                            self.userName = self.inputBox_userName.text.replace(":", "-")
                            self.userName = self.inputBox_userName.text.replace("/", "-")
                            self.serverIP = self.inputBox_serverIP.text.replace(":", "-")
                            self.serverIP = self.inputBox_serverIP.text.replace("/", "-")
                            self.serverPort = int(self.inputBox_serverPort.text.replace(":", "-"))
                            self.serverPort = int(self.inputBox_serverPort.text.replace("/", "-"))
                            self.connect(self.userName, self.serverIP, self.serverPort)

                            self.connection = "connected"
                            if self.connection == "connected":
                                self.win.blit(self.connectedMessage, (self.button_serverConnect.width+25, 557))

                        except:
                            print("Server offline: {}:{}".format(self.inputBox_serverIP.text, self.inputBox_serverPort.text))
                            offline = True

                        if self.connection == "connected":
                            self.connectionActive = True
                            self.button_startRinging.active = True

                    if self.button_startRinging.rect.collidepoint(event.pos) and self.button_startRinging.active == True:
                        run_menu = False
                        self.network.send("clientCommand:startRinging")
                        self.main()
                        break
    
                    if self.button_quit.rect.collidepoint(event.pos):
                        run_menu = False
                        self.network.send("clientDisconnect:Disconnecting")
                        pygame.quit()

                for box in self.input_boxes:
                    box.handle_event(event)

                for button in buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                    elif button.active == True:
                        button.hovered = False
                    button.draw(self.win)

            for box in self.input_boxes:
                box.update()

            for box in self.input_boxes:
                box.draw(self.win)

            pygame.display.flip()
            clock.tick(self.frameRate)

    def connect(self, userName, serverIP, serverPort):
        self.network.connect(userName, serverIP, serverPort)

    def main(self):
        self.win = pygame.display.set_mode((self.mainWidth, self.mainHeight))
        self.bells = {}
        for i in range(self.config.config['numberOfBells']):
            self.bells[i+1] = Bell(i+1, (self.mainWidth/2 - 100 * self.config.config['numberOfBells']/2 + 25) + i * 100, 550)

        for i, _ in enumerate(self.config.config['ringableBells']):
            key = self.config.config['keys'][i]
            self.bells[self.config.config['ringableBells'][i]].setKey(self.keyPress(key))

        clock = pygame.time.Clock()
        run_main = True
        while run_main:
            self.win.blit(self.mainBackground, (0, 0))
            for bell in self.bells.values():
                bell.draw(self.win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_main = False
                    self.network.send("clientDisconnect:Disconnecting")
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    for bell in self.bells.values():
                        bell.handle_event(event.key, self.network.send)

            try:
                bellNumber = int(self.network.getBellRung())
            except:
                pass
            else:
                self.bells[bellNumber].bellRung()
                self.bells[bellNumber].draw(self.win)
                pygame.display.update()

            pygame.display.update()
            clock.tick(self.frameRate)
   

if __name__ == "__main__":
    rebel = Rebel(750, 700, 1000, 700)
    rebel.start()

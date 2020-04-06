"""
ReBel v0.2.6
author: S. M. Senior
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

import sys

import numpy as np

from client import Network

from font import Font
from titledInputBox import TitledInputBox
from button import Button
from keyPress import KeyPress
from bell import Bell
from config import Config
from audio import Audio

import time

        
class Rebel(Font, KeyPress):
    def __init__(self, menuWidth, menuHeight, mainWidth, mainHeight, configFile='config.txt'):

        super().__init__()

        self.menuWidth = menuWidth
        self.menuHeight = menuHeight

        self.mainWidth = mainWidth
        self.mainHeight = mainHeight

        self.configFile = configFile

        # initialize
        pygame.init()
        pygame.mixer.pre_init(frequency=44100, size=16, channels=1)
        pygame.mixer.init()

        self.win = pygame.display.set_mode((self.menuWidth, self.menuHeight))
        pygame.display.set_caption("ReBel")

        self.menuBackground = pygame.image.load(os.path.join("img", "menuBackground.png"))
        self.mainBackground = pygame.image.load(os.path.join("img", "mainBackground.png"))

        self.offlineMessage = self.smallFont.render("Server offline...", 1, (255, 0, 0))
        self.connectingMessage = self.smallFont.render("Connecting to server...", 1, (50, 50, 50))
        self.connectedMessage = self.smallFont.render("Connected to server!", 1, (0, 255, 0))

        self.userName = ""
        self.serverIP = ""
        self.serverPort = None

        self.offline = None
        self.connection = None

        self.config = Config(fileName=self.configFile)

        self.frameRate = 100

        self.network = Network(frameRate=self.frameRate)

        pygame.mixer.set_num_channels(self.config.config['numberOfBells'])
        self.audio = Audio(self.config.config['numberOfBells'], pygame.mixer, self.config, os.path.join('audio', 'handbell.wav'))

    def start(self):
        self.menuScreen()

    def sanatiseServerInfo(self):
        self.userName = self.inputBox_userName.text.replace(":", "-")
        self.userName = self.inputBox_userName.text.replace("/", "-")
        self.serverIP = self.inputBox_serverIP.text.replace(":", "-")
        self.serverIP = self.inputBox_serverIP.text.replace("/", "-")
        self.serverPort = int(self.inputBox_serverPort.text.replace(":", "-"))
        self.serverPort = int(self.inputBox_serverPort.text.replace("/", "-"))

    def menuScreen(self):
        run_menu = True

        clock = pygame.time.Clock()
        self.inputBox_userName = TitledInputBox("Your Name:", 150, 350, 200, 32)
        self.inputBox_serverIP = TitledInputBox("Server IP:", 150, 400, 200, 32)
        self.inputBox_serverPort = TitledInputBox("Server Port:", 150, 450, 200, 32, text='35555')
        self.input_boxes = [self.inputBox_userName, self.inputBox_serverIP, self.inputBox_serverPort]

        self.button_serverConnect = Button("Connect to server", (20, 550))
        self.button_startRinging = Button("Start ringing", (20, 600), active=False)
        self.button_quit = Button("Quit", (20, 650))
        buttons = [self.button_serverConnect, self.button_startRinging, self.button_quit]

        self.connectionActive = False

        while run_menu:
            pygame.display.update(self.win.blit(self.menuBackground, (0, 0)))

            if self.offline:
                pygame.display.update(self.win.blit(self.offlineMessage, (self.button_serverConnect.width+25, 557)))
            elif self.connection == "connecting":
                pygame.display.update(self.win.blit(self.connectingMessage, (self.button_serverConnect.width+25, 557)))
            elif self.connection == "connected":
                pygame.display.update(self.win.blit(self.connectedMessage, (self.button_serverConnect.width+25, 557)))

            for box in self.input_boxes:
                pygame.display.update(box.draw(self.win))
            for button in buttons:
                pygame.display.update(button.draw(self.win))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_menu = False
                    if self.offline == False:
                        self.network.send("clientDisconnect:Disconnecting")
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_serverConnect.rect.collidepoint(event.pos) and self.connectionActive == False:
                        self.offline = False
                        try:
                            self.connection = "connecting"
                            if self.connection == "connecting":
                                pygame.display.update(self.win.blit(self.connectingMessage, (self.button_serverConnect.width+25, 557)))

                            self.sanatiseServerInfo()
                            self.offline = not self.connect(self.userName, self.serverIP, self.serverPort)
                            while self.network.connected is None:
                                time.sleep(0.1)
                            self.offline = not self.network.connected
                            if self.offline == False:
                                self.connection = "connected"
                                self.connectionActive = True
                                self.button_startRinging.active = True
                                pygame.display.update(self.win.blit(self.connectedMessage, (self.button_serverConnect.width+25, 557)))
                                if self.config.config['testConnectionLatency'][0] == True:
                                    self.testConnectionLatency(numberOfPings=self.config.config['testConnectionLatency'][1],
                                                               outputRate=self.config.config['testConnectionLatency'][2])
                            else:
                                self.connection = "offline"
                                pygame.display.update(self.win.blit(self.offlineMessage, (self.button_serverConnect.width+25, 557)))
                        except:
                            pygame.display.update(self.win.blit(self.offlineMessage, (self.button_serverConnect.width+25, 557)))
                            print("Server offline: {}:{}".format(self.inputBox_serverIP.text, self.inputBox_serverPort.text))
                            self.offline = True

                    if self.button_startRinging.rect.collidepoint(event.pos) and self.button_startRinging.active == True:
                        run_menu = False
                        self.network.send("clientCommand:startRinging")
                        self.main()
                        break
    
                    if self.button_quit.rect.collidepoint(event.pos):
                        run_menu = False
                        if self.offline == False:
                            self.network.send("clientDisconnect:Disconnecting")
                        pygame.quit()
                        sys.exit(0)

                for box in self.input_boxes:
                    pygame.display.update(box.handle_event(event, self.win))

                for button in buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                    elif button.active == True:
                        button.hovered = False
                    pygame.display.update(button.draw(self.win))

            pygame.display.update()
            clock.tick(self.frameRate)

    def connect(self, userName, serverIP, serverPort):
        self.network.connect(userName, serverIP, serverPort)

    def testConnectionLatency(self, numberOfPings, outputRate):
        print("Performing ping test to measure latency...")

        time_start = None
        time_end = None
        average = [0, 0]

        self.network.ringing = True
        for i in range(numberOfPings):
            time_start = time.time()
            self.network.send("ping")
            recvd = False
            while recvd == False:
                try:
                    bellNumber = int(self.network.getBellRung())
                except:
                    pass
                else:
                    if i % outputRate == 0:
                        print("Ping {}/{}".format(i, numberOfPings))
                    i += 1

                    time_end = time.time()
                    average[0] += (time_end - time_start)
                    average[1] += 1
                    #print("Time between send and recieve: {}".format(time_end - time_start))#self.time_end = time.time()
                    recvd = True
        self.network.ringing = False
        print("{} pings, average latency of: {} ms".format(average[1], int(1000*average[0]/average[1])))

    def main(self):
        self.win = pygame.display.set_mode((self.mainWidth, self.mainHeight))
        self.bells = {}
        seperationAngle = 2.0*np.pi / self.config.config['numberOfBells']

        self.a = 1.5#*10/8.0
        self.b = 1.0

        self.radius = 200+5*(self.config.config['numberOfBells']//2)

        for i in range(self.config.config['numberOfBells']):
            self.bells[i+1] = Bell(i+1, (self.mainWidth / 2.0 + self.radius*self.a*np.cos(seperationAngle*i + seperationAngle/2.0)) - 75,
                                        (self.mainHeight*3.0/5.0 + self.radius*self.b*np.sin(seperationAngle*i + seperationAngle/2.0)) - 75,
                                        bellImageFile=os.path.join("img", "handbell.png"))

        for i, _ in enumerate(self.config.config['ringableBells']):
            key = self.config.config['keys'][i]
            self.bells[self.config.config['ringableBells'][i]].setKey(self.keyPress(key))

        clock = pygame.time.Clock()
        pygame.display.update(self.win.blit(self.mainBackground, (0, 0)))
        for bell in self.bells.values():
                pygame.display.update(bell.draw(self.win))
        run_main = True
        while run_main:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_main = False
                    self.network.send("clientDisconnect:Disconnecting")
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    for bell in self.bells.values():
                        if event.key == bell.key:


                            self.time_start = time.time()


                            self.network.send(str(bell.bellNumber))

            try:
                bellNumber = int(self.network.getBellRung())
            except:
                pass
            else:
                self.bells[bellNumber].bellRung()
                pygame.display.update(self.bells[bellNumber].draw(self.win))
                pygame.mixer.Channel(bellNumber-1).play(self.audio.bells[bellNumber])
                pygame.display.update()

            clock.tick(self.frameRate)
   

if __name__ == "__main__":
    rebel = Rebel(750, 700, 1000, 700)
    rebel.start()

import pygame
import os
import sys
import time

from titledInputBox import TitledInputBox
from button import Button

from log import Log


class MenuScreen(Log):
    def __init__(self, win, network, frameRate, logFile, config, font):
        if getattr(sys, 'frozen', False):
            # In a bundle
            self.exeDir = os.path.dirname(sys.executable)
        else:
            # In normal python
            self.exeDir = ""

        self.win = win
        self.network = network
        self.frameRate = frameRate
        self.logFile = logFile
        self.config = config
        self.font = font

        Log.__init__(self, logFile=logFile)

        self.width = self.win.get_width()
        self.height = self.win.get_height()

        self.backgroundColour = (255, 255, 255)
        self.rebelLogo = pygame.image.load(os.path.join(self.exeDir, "..", "img", "logo.png"))

        self.offlineMessage = self.font.smallFont.render("Server offline...", 1, (255, 0, 0))
        self.connectingMessage = self.font.smallFont.render("Connecting to server...", 1, (50, 50, 50))
        self.connectedMessage = self.font.smallFont.render("Connected to server!", 1, (0, 255, 0))
        self.blankMessage = self.font.smallFont.render("", 1, (255, 255, 255))

        self.userName = ""
        self.serverIP = ""
        self.serverPort = None

        self.offline = None
        self.connection = None

        self.connectionActive = False

        self.button_quit = Button("Quit", (20, self.height-20), font=self.font)
        self.button_quit.rect.y -= self.button_quit.rect.h
        #
        self.button_about = Button("About", (20, self.button_quit.rect.y-10), font=self.font, active=True)
        self.button_about.rect.y -= self.button_about.rect.h
        #
        self.button_help = Button("Help Info", (20, self.button_about.rect.y-10), font=self.font, active=True)
        self.button_help.rect.y -= self.button_help.rect.h
        #
        self.button_startRinging = Button("Start ringing", (20, self.button_help.rect.y-10), font=self.font, active=False)
        self.button_startRinging.rect.y -= self.button_startRinging.rect.h
        #
        self.button_serverConnect = Button("Connect to server", (20, self.button_startRinging.rect.y-10), font=self.font)
        self.button_serverConnect.rect.y -= self.button_serverConnect.rect.h
        #
        self.buttons = [self.button_serverConnect, self.button_startRinging, self.button_help, self.button_about, self.button_quit]

        self.inputBox_serverPort = TitledInputBox("Server Port:", 160, self.button_serverConnect.rect.y-85, 200, 32, font=self.font, text='35555')
        self.inputBox_serverIP = TitledInputBox("Server IP:", 160, self.inputBox_serverPort.y-50, 200, 32, font=self.font)
        self.inputBox_userName = TitledInputBox("Your Name:", 160, self.inputBox_serverIP.y-50, 200, 32, font=self.font)
        self.input_boxes = [self.inputBox_userName, self.inputBox_serverIP, self.inputBox_serverPort]
        self.activeBox = None

        self.connectionRectWhite = pygame.Rect(self.button_serverConnect.width+25, self.button_serverConnect.rect.y+5, self.connectingMessage.get_width(), self.connectingMessage.get_height())

        self.connectionActive = False

    def connectionStatusMessage(self):
        if self.connection == "offline":
            return self.offlineMessage
        elif self.connection == "connecting":
            return self.connectingMessage
        elif self.connection == "connected":
            return self.connectedMessage
        else:
            return self.blankMessage

    def updateConnectionStatusMessage(self):
        pygame.draw.rect(self.win, (255, 255, 255), self.connectionRectWhite, 0)
        if self.connection:
            self.win.blit(self.connectionStatusMessage(), (self.button_serverConnect.width+25, self.button_serverConnect.rect.y+5))

    def sanatiseServerInfo(self):
        self.userName = self.inputBox_userName.text.replace(":", "-")
        self.userName = self.inputBox_userName.text.replace("/", "-")
        self.serverIP = self.inputBox_serverIP.text.replace(":", "-")
        self.serverIP = self.inputBox_serverIP.text.replace("/", "-")
        self.serverPort = int(self.inputBox_serverPort.text.replace(":", "-"))
        self.serverPort = int(self.inputBox_serverPort.text.replace("/", "-"))

    def testConnectionLatency(self, numberOfPings, outputRate):
        self.log("Performing ping test to measure latency...")

        time_start = None
        time_end = None
        average = [0, 0]

        self.network.setVar('ringing', True)
        for i in range(numberOfPings):
            time_start = time.time()
            self.network.send("ping")
            recvd = False
            while recvd == False:
                try:
                    stroke, bellNumber = self.network.getBellRung()
                    bellNumber = int(bellNumber)
                except:
                    pass
                else:
                    if i % outputRate == 0:
                        self.log("Ping {}/{}".format(i, numberOfPings))
                    i += 1

                    time_end = time.time()
                    average[0] += (time_end - time_start)
                    average[1] += 1
                    recvd = True
        self.network.setVar('ringing', False)
        self.log("{} pings, average latency of: {} ms".format(average[1], int(1000*average[0]/average[1])))

    def display(self):

        self.run_menu = True

        clock = pygame.time.Clock()

        self.win.fill(self.backgroundColour)
        self.win.blit(self.rebelLogo, (self.width/2-self.rebelLogo.get_width()/2, (self.inputBox_userName.rect.y - self.rebelLogo.get_height())*3/8))

        for box in self.input_boxes:
            box.draw(self.win, redrawTitle=True)
            box.updated = False
        for button in self.buttons:
            button.hovered = False
            button.draw(self.win)

        self.updateConnectionStatusMessage()

        while self.run_menu:
            for box in self.input_boxes:
                if box.updated:
                    box.draw(self.win, redrawTitle=False)
                    box.updated = False
            for button in self.buttons:
                if button.updated:
                    button.draw(self.win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_menu = False
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_serverConnect.rect.collidepoint(event.pos):
                        if self.network.getVar('connected'):
                            self.network.disconnect()
                        self.offline = False
                        self.connectionActive = False
                        try:
                            self.connection = "connecting"
                            self.updateConnectionStatusMessage()

                            self.sanatiseServerInfo()
                            self.offline = not self.network.connect(self.userName, self.serverIP, self.serverPort)
                            while self.network.getVar('connected') is None:
                                time.sleep(0.1)
                            self.offline = not self.network.getVar('connected')
                            if self.offline == False:
                                self.connection = "connected"
                                self.connectionActive = True
                                self.button_startRinging.active = True
                                self.updateConnectionStatusMessage()
                                if self.config.get('testConnectionLatency')[0] == True:
                                    self.testConnectionLatency(numberOfPings=self.config.get('testConnectionLatency')[1],
                                                               outputRate=self.config.get('testConnectionLatency')[2])
                            else:
                                self.connection = "offline"
                                self.updateConnectionStatusMessage()
                        except:
                            self.connection = "offline"
                            self.updateConnectionStatusMessage()
                            self.log("[INFO] Server offline: {}:{}".format(self.inputBox_serverIP.text, self.inputBox_serverPort.text))
                            self.offline = True

                    if self.button_startRinging.rect.collidepoint(event.pos) and self.button_startRinging.active == True:
                        self.run_menu = False
                        self.network.send("clientCommand:startRinging")
                        return 'ringingScreen'

                    if self.button_help.rect.collidepoint(event.pos):
                        self.run_menu = False
                        return 'helpScreen'

                    if self.button_about.rect.collidepoint(event.pos):
                        self.run_menu = False
                        return 'aboutScreen'

                    if self.button_quit.rect.collidepoint(event.pos):
                        self.run_menu = False
                        return 'quit'

                    for box in self.input_boxes:
                        box.mouseDownEvent(event, self.win)
                        if box.active == True:
                            self.activeBox = box

                if event.type == pygame.KEYDOWN:
                    if self.activeBox and self.activeBox.active:
                        self.activeBox.keyDownEvent(event, self.win)

                for button in self.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                        button.updated = True
                    elif button.active == True:
                        button.hovered = False
                        button.updated = True
                        button.draw(self.win)

            pygame.display.flip()
            clock.tick(self.frameRate)
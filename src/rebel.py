"""
ReBel
author: Samuel M Senior
"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

import sys

import numpy as np

from log import Log

from client import Network

from font import Font
from titledInputBox import TitledInputBox
from button import Button
from keyPress import KeyPress
from bell import Bell
from config import Config
from audio import Audio

from helpScreen import HelpScreen
from menuScreen import MenuScreen

        
class Rebel(Font, KeyPress, Log):
    def __init__(self, menuWidth, menuHeight, mainWidth, mainHeight, configFile=os.path.join("..", "config", "config.txt")):

        # initialize
        pygame.init()
        pygame.mixer.pre_init(frequency=44100, size=16, channels=1)
        pygame.mixer.init()
        pygame.font.init()

        Font.__init__(self)
        KeyPress.__init__(self)

        self.logFile = os.path.join("..", "log", "log.txt")
        Log.__init__(self, logFile=self.logFile)
        self.clearLog()

        self.reBelClientVersion = "v0.2.13"
        self.log("[INFO] Running ReBel client {}".format(self.reBelClientVersion))

        self.menuWidth = menuWidth
        self.menuHeight = menuHeight

        self.mainWidth = mainWidth
        self.mainHeight = mainHeight

        self.configFile = configFile

        self.win = pygame.display.set_mode((self.menuWidth, self.menuHeight))
        pygame.display.set_caption("ReBel")

        self.mainBackground = pygame.image.load(os.path.join("..", "img", "mainBackground.png"))

        self.frameRate = 100

        self.config = Config(fileName=self.configFile)

        self.network = Network(self.logFile, frameRate=self.frameRate)

        self.helpScreen = HelpScreen(self.win, frameRate=self.frameRate)

        self.menuScreen = MenuScreen(win=self.win, network=self.network, frameRate=self.frameRate, logFile=self.logFile, config=self.config)

        self.screen = 'menuScreen'

    def quit(self):
        self.running = False
        if self.network.connected == True:#offline == False:
            self.network.send("clientDisconnect:Disconnecting")
        self.log("[INFO] Quitting...")
        pygame.quit()
        sys.exit(0)

    def ringingScreen(self):
        self.win = pygame.display.set_mode((self.mainWidth, self.mainHeight))
        self.network.send("numberOfBells:get")

        waitingForNumberOFBells = True
        while waitingForNumberOFBells:
            try:
                self.config.set('numberOfBells', self.network.getNumberOfBells())
            except:
                pass
            else:
                waitingForNumberOFBells = False
                self.log("[Client] Number of bells set to {}".format(self.config.get('numberOfBells')))

        self.bells = {}
        seperationAngle = 2.0*np.pi / self.config.get('numberOfBells')

        self.a = 1.5#*10/8.0
        self.b = 1.0

        self.radius = 200+5*(self.config.get('numberOfBells')//2)

        for i in range(self.config.get('numberOfBells')):

            width = 140
            height = 140

            x = (self.mainWidth / 2.0 + self.radius*self.a*np.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0
            y = (self.mainHeight*3.0/5.0 + self.radius*self.b*np.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0

            if (seperationAngle*i + seperationAngle/2.0) <= np.pi/2.0 or (seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0) >= 3.0*np.pi/2.0:
                textX = (self.mainWidth / 2.0 + (self.radius-0)*self.a*np.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) + width/2.0 - width/14.0
                textY = (self.mainHeight*3.0/5.0 + (self.radius+0)*self.b*np.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0
            else:
                textX = (self.mainWidth / 2.0 + (self.radius+0)*self.a*np.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0
                textY = (self.mainHeight*3.0/5.0 + (self.radius+0)*self.b*np.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0

            self.bells[i+1] = Bell(i+1, location=(x, y), width=width, height=height,
                                   textLocation=(textX, textY),
                                   bellImageFile=os.path.join("..", "img", "handbell.png"))

        for i, _ in enumerate(self.config.get('ringableBells')) if len(self.config.get('ringableBells')) < self.config.get('numberOfBells') else enumerate(range(self.config.get('numberOfBells'))):
            key = self.config.get('keys')[i]
            self.bells[self.config.get('ringableBells')[i]].setKey(self.keyPress(key))

        pygame.mixer.set_num_channels(self.config.get('numberOfBells'))
        self.audio = Audio(self.config.get('numberOfBells'), pygame.mixer, self.config, self.logFile)

        clock = pygame.time.Clock()
        pygame.display.update(self.win.blit(self.mainBackground, (0, 0)))
        for bell in self.bells.values():
                pygame.display.update(bell.draw(self.win, renderNumber=True))
        run_ringing = True
        while run_ringing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_ringing = False
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    for bell in self.bells.values():
                        if event.key == bell.key:
                            bell.handle_event(self.network.send)
            try:
                stroke, bellNumber = self.network.getBellRung()
                bellNumber = int(bellNumber)
            except:
                pass
            else:
                self.bells[bellNumber].bellRung(stroke)
                self.bells[bellNumber].draw(self.win)
                pygame.mixer.Channel(bellNumber-1).play(self.audio.bells[bellNumber])
                pygame.display.flip()

            clock.tick(self.frameRate)

    def run(self):
        self.running = True
        while self.running:
            if self.screen == 'menuScreen':
                self.previousScreen = 'menuScreen'
                self.screen = self.menuScreen.display()
                if self.screen == 'quit':
                    self.quit()
            elif self.screen == 'helpScreen':
                self.screen = self.helpScreen.display(source=self.previousScreen)
                if self.screen == 'quit':
                    self.quit()
                else:
                    self.screen = self.previousScreen
            elif self.screen == 'ringingScreen':
                self.previousScreen = 'ringingScreen'
                self.screen = self.ringingScreen()
            else:
                self.quit()
   

if __name__ == "__main__":
    rebel = Rebel(750, 700, 1000, 700)
    rebel.run()

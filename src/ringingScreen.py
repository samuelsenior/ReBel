import pygame
import os

import numpy as np

from audio import Audio
from bell import Bell
from button import Button
from keyPress import KeyPress
from log import Log

class RingingScreen(KeyPress, Log):
    def __init__(self, network, width, height, frameRate, logFile, config):
        self.logFile = logFile
        Log.__init__(self, logFile=logFile)

        KeyPress.__init__(self)

        self.network = network
        self.width = width
        self.height = height
        self.frameRate = frameRate
        self.config = config

        #self.backgroundColour = (150, 150, 150)
        self.backgroundColour = (255, 255, 255)

        self.button_options = Button("Options", (0, 0), active=False, border=True, fontSize="medium")
        self.button_help = Button("Help", (self.button_options.rect.x+self.button_options.rect.w, 0), border=True, fontSize="medium")
        self.button_about = Button("About", (self.button_help.rect.x+self.button_help.rect.w, 0), active=False, border=True, fontSize="medium")
        self.button_back = Button("Back", (self.button_about.rect.x+self.button_about.rect.w, 0), border=True, fontSize="medium")
        self.button_quit = Button("Quit", (self.button_back.rect.x+self.button_back.rect.w, 0), border=True, fontSize="medium")
        self.buttons = [self.button_options, self.button_help, self.button_about, self.button_back, self.button_quit]

        self.initialised = False

    def initialise(self):
        self.network.getNumberOfBells(empty=True)
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

        self.a = 1.35#*10/8.0
        self.b = 1.0

        self.radius = 225+5*(self.config.get('numberOfBells')//2)

        for i in range(self.config.get('numberOfBells')):

            width = 140
            height = 140

            x = (self.width / 2.0 + self.radius*self.a*np.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0
            #y = (self.height*3.0/5.0 + self.radius*self.b*np.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0
            y = (self.height / 2.0 + self.button_options.rect.h + self.radius*self.b*np.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0

            if (seperationAngle*i + seperationAngle/2.0) <= np.pi/2.0 or (seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0) >= 3.0*np.pi/2.0:
                textX = (self.width / 2.0 + (self.radius-0)*self.a*np.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) + width/2.0 - width/14.0
                #textY = (self.height*3.0/5.0 + (self.radius+0)*self.b*np.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0
                textY = (self.height / 2.0 + self.button_options.rect.h + (self.radius+0)*self.b*np.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0
            else:
                textX = (self.width / 2.0 + (self.radius+0)*self.a*np.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0
                #textY = (self.height*3.0/5.0 + (self.radius+0)*self.b*np.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0
                textY = (self.height / 2.0 + self.button_options.rect.h + (self.radius+0)*self.b*np.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + np.pi/2.0)) - width/2.0

            self.bells[i+1] = Bell(i+1, location=(x, y), width=width, height=height,
                                   textLocation=(textX, textY),
                                   bellImageFile=os.path.join("..", "img", "handbell.png"),
                                   backgroundColour=self.backgroundColour)

        for i, _ in enumerate(self.config.get('ringableBells')) if len(self.config.get('ringableBells')) < self.config.get('numberOfBells') else enumerate(range(self.config.get('numberOfBells'))):
            key = self.config.get('keys')[i]
            self.bells[self.config.get('ringableBells')[i]].setKey(self.keyPress(key))

        pygame.mixer.set_num_channels(self.config.get('numberOfBells'))
        self.audio = Audio(self.config.get('numberOfBells'), pygame.mixer, self.config, self.logFile)

        self.initialised = True

    def display(self):
        self.win = pygame.display.set_mode((self.width, self.height))
        
        if self.initialised == False:
            self.initialise()

        self.network.getNumberOfBells(empty=True)
        self.network.send("numberOfBells:get")
        waitingForNumberOFBells = True
        while waitingForNumberOFBells:
            try:
                numberOfBells = self.network.getNumberOfBells()
            except:
                pass
            else:
                if numberOfBells != self.config.get('numberOfBells'):
                    self.initialise()
                waitingForNumberOFBells = False

        clock = pygame.time.Clock()

        #self.win.fill((255, 255, 255))
        self.win.fill(self.backgroundColour)
        for bell in self.bells.values():
                bell.draw(self.win, renderNumber=True)
        for button in self.buttons:
            button.active = True
            button.hovered = False
            button.draw(self.win)

        self.button_options.active = False
        self.button_about.active = False

        run_ringing = True
        while run_ringing:

            for button in self.buttons:
                if button.updated:
                    button.draw(self.win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_ringing = False
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_help.rect.collidepoint(event.pos):
                        run_help = False
                        return 'helpScreen'
                    elif self.button_back.rect.collidepoint(event.pos):
                        run_help = False
                        return 'menuScreen'
                    elif self.button_quit.rect.collidepoint(event.pos):
                        run_help = False
                        return 'quit'

                if event.type == pygame.KEYDOWN:
                    for bell in self.bells.values():
                        if event.key == bell.key:
                            bell.handle_event(self.network.send)

                for button in self.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                        button.updated = True
                    elif button.active == True:
                        button.hovered = False
                        button.updated = True
                        button.draw(self.win)

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
import pygame
import os
import sys
import time

import math

from audio import Audio
from bell import Bell
from button import Button
from keyPress import KeyPress
from log import Log

class RingingScreen(KeyPress, Log):
    def __init__(self, network, width, height, font, frameRate, logFile, config):
        if getattr(sys, 'frozen', False):
            # In a bundle
            self.exeDir = os.path.dirname(sys.executable)
        else:
            # In normal python
            self.exeDir = ""
        self.logFile = logFile
        Log.__init__(self, logFile=logFile)

        KeyPress.__init__(self)

        self.network = network
        self.width = width
        self.height = height
        self.font = font
        self.frameRate = frameRate
        self.config = config

        #self.backgroundColour = (150, 150, 150)
        self.backgroundColour = (230, 230, 230)
        #self.backgroundColour = (255, 255, 255)

        self.button_reloadBells = Button("Reload Bells", (0, 0), font=self.font, active=True, border=True, fontSize="small")
        self.button_options = Button("Options", (self.button_reloadBells.rect.x+self.button_reloadBells.rect.w, 0), font=self.font, border=True, fontSize="small")
        self.button_help = Button("Help", (self.button_options.rect.x+self.button_options.rect.w, 0), font=self.font, border=True, fontSize="small")
        self.button_about = Button("About", (self.button_help.rect.x+self.button_help.rect.w, 0), font=self.font, border=True, fontSize="small")
        self.button_back = Button("Back", (self.button_about.rect.x+self.button_about.rect.w, 0), font=self.font, border=True, fontSize="small")
        self.button_quit = Button("Quit", (self.button_back.rect.x+self.button_back.rect.w, 0), font=self.font, border=True, fontSize="small")
        self.button_blankSpace = Button("", (self.button_quit.rect.x+self.button_quit.rect.w, 0), font=self.font, border=True, fontSize="small", buttonColour=(self.button_options.borderColour))
        self.button_blankSpace.rect.w = self.width - self.button_blankSpace.rect.x
        self.buttons = [self.button_reloadBells, self.button_options, self.button_help, self.button_about, self.button_back, self.button_quit, self.button_blankSpace]

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

        ringableBells_tmp = self.config.get('ringableBells').copy()
        keys_tmp = self.config.get('keys').copy()
        for i in range(len(self.config.get('ringableBells'))):
            if self.config.get('ringableBells')[i] > self.config.get('numberOfBells') or self.config.get('ringableBells')[i] < 1:
                del ringableBells_tmp[i]
                del keys_tmp[i]
        self.config.set('ringableBells', ringableBells_tmp)
        self.config.set('keys', keys_tmp)

        self.bells = {}
        seperationAngle = 2.0*math.pi / self.config.get('numberOfBells')

        if self.config.get('numberOfBells') >= 8:
            self.a = 1.35#*10/8.0
            self.b = 1.0
        elif self.config.get('numberOfBells') > 4:
            self.a = 1.0 + 0.35 / 4 * (self.config.get('numberOfBells') - 4)
            self.b = 1.0
        else:
            self.a = 1.0
            self.b = 1.0

        self.radius = 215+5*(self.config.get('numberOfBells'))

        for i in range(self.config.get('numberOfBells')):

            if self.config.get('numberOfBells') > 12:
                width = 90 + 60 * 8//12
                height = 90 + 60 * 8//12
            else:
                width = 90 + 60 * 8 // self.config.get('numberOfBells')
                height = 90 + 60 * 8 // self.config.get('numberOfBells')

            x = (self.width / 2.0 - 10 + self.radius*self.a*math.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) - width/2.0
            y = (self.height / 2.0 - 10 + self.button_options.rect.h + self.radius*self.b*math.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) - width/2.0

            if (seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0) <= math.pi/2.0 or (seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0) >= 3.0*math.pi/2.0:
                textX = (self.width / 2.0 - 10 + (self.radius-0)*self.a*math.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) + width/2.0 - width/14.0
                textY = (self.height / 2.0 - 10 + self.button_options.rect.h + (self.radius+0)*self.b*math.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) - width/2.0
            else:
                textX = (self.width / 2.0 - 10 + (self.radius+0)*self.a*math.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) - width/2.0
                textY = (self.height / 2.0 - 10 + self.button_options.rect.h + (self.radius+0)*self.b*math.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) - width/2.0

            self.bells[i+1] = Bell(i+1, location=(x, y), width=width, height=height,
                                   textLocation=(textX, textY), font=self.font,
                                   bellImageFile=os.path.join(self.exeDir, "..", "img", "handbell.png"),
                                   backgroundColour=self.backgroundColour)

        for i, _ in enumerate(self.config.get('ringableBells')) if len(self.config.get('ringableBells')) < self.config.get('numberOfBells') else enumerate(range(self.config.get('numberOfBells'))):
            try:
                key = self.config.get('keys')[i]
                self.bells[self.config.get('ringableBells')[i]].setKey(self.keyPress(key))
            except:
                self.log("[WARNING] RingingScreen.initialise: Incorrect bell/key configuration of bell no. '{}' and key '{}'".format(self.config.get('ringableBells')[i], self.config.get('keys')[i]))

        pygame.mixer.set_num_channels(self.config.get('numberOfBells'))
        self.audio = Audio(self.config.get('numberOfBells'), pygame.mixer, self.config, self.logFile)

        self.updateBellStates()

        self.initialised = True

    def updateBellStates(self):
        self.network.getBellStates(empty=True)
        self.network.send("bellStates:get")
        waitingForBellStates = True
        while waitingForBellStates:
            try:
                self.config.set('bellStates', self.network.getBellStates())
            except:
                pass
            else:
                waitingForBellStates = False
                self.log("[Client] Bell States set to {}".format(self.config.get('bellStates')))
        bellStates = self.config.get('bellStates')

        for i in range(self.config.get('numberOfBells')):
            self.bells[i+1].stroke = bellStates[i]

    def updateBellKeys(self):
        for i in range(1, self.config.get('numberOfBells')+1, 1):
            self.bells[i].clearKey()
        for i, _ in enumerate(self.config.get('ringableBells')) if len(self.config.get('ringableBells')) < self.config.get('numberOfBells') else enumerate(range(self.config.get('numberOfBells'))):
            try:
                key = self.config.get('keys')[i]
                self.bells[self.config.get('ringableBells')[i]].setKey(self.keyPress(key))
            except:
                self.log("[WARNING] RingingScreen.updateBellKeys: Incorrect bell/key configuration of bell no. '{}' and key '{}'".format(self.config.get('ringableBells')[i], self.config.get('keys')[i]))

    def updateBellDisplayLocations(self):
        seperationAngle = 2.0*math.pi / self.config.get('numberOfBells')

        if self.config.get('numberOfBells') >= 8:
            self.a = 1.35#*10/8.0
            self.b = 1.0
        elif self.config.get('numberOfBells') > 4:
            self.a = 1.0 + 0.35 / 4 * (self.config.get('numberOfBells') - 4)
            self.b = 1.0
        else:
            self.a = 1.0
            self.b = 1.0

        self.radius = 215+5*(self.config.get('numberOfBells'))

        for i, bell in self.bells.items():
            i -= 1

            if self.config.get('numberOfBells') > 12:
                width = 90 + 60 * 8//12
                height = 90 + 60 * 8//12
            else:
                width = 90 + 60 * 8 // self.config.get('numberOfBells')
                height = 90 + 60 * 8 // self.config.get('numberOfBells')

            x = (self.width / 2.0 - 10 + self.radius*self.a*math.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) - width/2.0
            y = (self.height / 2.0 - 10 + self.button_options.rect.h + self.radius*self.b*math.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) - width/2.0

            if (seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0) <= math.pi/2.0 or (seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0) >= 3.0*math.pi/2.0:
                textX = (self.width / 2.0 - 10 + (self.radius-0)*self.a*math.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) + width/2.0 - width/14.0
                textY = (self.height / 2.0 - 10 + self.button_options.rect.h + (self.radius+0)*self.b*math.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) - width/2.0
            else:
                textX = (self.width / 2.0 - 10 + (self.radius+0)*self.a*math.cos(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) - width/2.0
                textY = (self.height / 2.0 - 10 + self.button_options.rect.h + (self.radius+0)*self.b*math.sin(seperationAngle*(i-self.config.get('ringableBells')[0]+1) - seperationAngle/2.0 + math.pi/2.0)) - width/2.0

            bell.updateLocation(x, y, textX, textY)

    def display(self, display):

        self.win = display.set_mode((self.width, self.height))
        
        if self.initialised == False:
            self.initialise()
        else:
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
                    else:
                        self.updateBellStates()
                    waitingForNumberOFBells = False

        #self.updateBellStates()

        clock = pygame.time.Clock()

        self.win.fill(self.backgroundColour)
        for bell in self.bells.values():
                bell.draw(display, renderNumber=True)
        for button in self.buttons:
            button.active = True
            button.hovered = False
            button.draw(display)

        self.updated = True

        run_ringing = True
        while run_ringing:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_ringing = False
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_reloadBells.rect.collidepoint(event.pos):
                        self.initialise()
                        self.win.fill(self.backgroundColour)
                        for bell in self.bells.values():
                                bell.draw(display, renderNumber=True)
                        for button in self.buttons:
                            button.hovered = False
                            button.draw(display)
                        self.updated = True
                    elif self.button_options.rect.collidepoint(event.pos):
                        run_ringing = False
                        return 'optionsScreen'
                    elif self.button_about.rect.collidepoint(event.pos):
                        run_ringing = False
                        return 'aboutScreen'
                    elif self.button_help.rect.collidepoint(event.pos):
                        run_ringing = False
                        return 'helpScreen'
                    elif self.button_back.rect.collidepoint(event.pos):
                        run_ringing = False
                        return 'menuScreen'
                    elif self.button_quit.rect.collidepoint(event.pos):
                        run_ringing = False
                        return 'quit'

                if event.type == pygame.KEYDOWN:
                    for bell in self.bells.values():
                        if event.key == bell.key:
                            bell.handle_event(self.network.send)

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

            try:
                stroke, bellNumber = self.network.getBellRung()
                bellNumber = int(bellNumber)

            except:
                pass
            else:
                self.bells[bellNumber].bellRung(stroke)
                self.bells[bellNumber].draw(display)
                pygame.mixer.Channel(bellNumber-1).play(self.audio.bells[bellNumber])
                self.updated = True

            if self.updated:
                display.flip()
                self.updated = False

            clock.tick(self.frameRate)
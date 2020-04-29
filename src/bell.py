import pygame
from font import Font

import os

class Bell(Font):
    def __init__(self, bellNumber, location, bellImageFile, width, height, textLocation, key=None, backgroundColour=(255, 255, 255)):
        super().__init__()
        self.stroke = 'H'

        # Read in bell image and create handstroke and backstroke images from it
        self.width = width
        self.height = height
        self.backgroundColour = backgroundColour
        bell = pygame.image.load(bellImageFile)
        self.handstrokeBell = pygame.transform.scale(bell, (self.width, self.height))
        self.handstrokeBellBlank = self.handstrokeBell.copy()
        self.fill(self.handstrokeBellBlank, pygame.Color(*self.backgroundColour))
        self.backstrokeBell = pygame.transform.scale(bell, (self.width, self.height))
        self.backstrokeBell = pygame.transform.rotate(self.backstrokeBell, -90.0)
        self.backstrokeBell = pygame.transform.flip(self.backstrokeBell, True, False)
        self.backstrokeBellBlank = self.backstrokeBell.copy()
        self.fill(self.backstrokeBellBlank, pygame.Color(*self.backgroundColour))

        self.bellNumber = bellNumber
        self.bellNumberText = self.FONT.render(str(self.bellNumber), True, (0, 0, 0))

        self.x = location[0]
        self.y = location[1]

        self.textX = textLocation[0]
        self.textY = textLocation[1]

        self.key = key

    def fill(self, surface, colour):
        w, h = surface.get_size()
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(colour[0], colour[1], colour[2], a))

    def setKey(self, key):
        self.key = key

    def draw(self, win, renderNumber=False):
        if renderNumber:
            win.blit(self.bellNumberText, (self.textX, self.textY))
        if self.stroke == 'H':
            win.blit(self.backstrokeBellBlank, (self.x, self.y))
            return win.blit(self.handstrokeBell, (self.x, self.y))
        else:
            win.blit(self.handstrokeBellBlank, (self.x, self.y))
            return win.blit(self.backstrokeBell, (self.x, self.y))

    def handle_event(self, send):
        send("R:" + self.stroke + str(self.bellNumber))

    def bellRung(self, stroke):
        # Change the bell stroke 
        self.stroke = 'B' if stroke == 'H' else 'H'
        
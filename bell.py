import pygame

import os

class Bell:
    def __init__(self, bellNumber, x, y, bellImageFile, key=None):

        self.stroke = 'H'

        # Read in bell image and create handstroke and backstroke images from it
        self.width = 50
        self.height = 50
        bell = pygame.image.load(bellImageFile)
        self.handstrokeBell = pygame.transform.scale(bell, (self.width, self.height))
        self.handstrokeBellBlank = self.handstrokeBell.copy()
        self.fill(self.handstrokeBellBlank, pygame.Color(255, 255, 255))
        self.backstrokeBell = pygame.transform.scale(bell, (135, 135))
        self.backstrokeBell = pygame.transform.rotate(self.backstrokeBell, -90.0)
        self.backstrokeBell = pygame.transform.flip(self.backstrokeBell, True, False)
        self.backstrokeBellBlank = self.backstrokeBell.copy()
        self.fill(self.backstrokeBellBlank, pygame.Color(255, 255, 255))

        self.bellNumber = bellNumber

        self.x = x
        self.y = y

        self.key = key

    def fill(self, surface, colour):
        w, h = surface.get_size()
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(colour[0], colour[1], colour[2], a))

    def setKey(self, key):
        self.key = key

    def draw(self, win):
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
        
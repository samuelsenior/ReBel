import pygame

import os

class Bell:
    def __init__(self, bellNumber, x, y, bellImageFile, key=None):

        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')

        self.stroke = "handstroke"

        # Read in bell
        # transform bell to smaller size and rotate to make handstroke bell and backstroke bell
        # Want the bell png to have the same width and height surely, so position doesn't change in rotation?
        bell = pygame.image.load(bellImageFile)
        self.handstrokeBell = pygame.transform.scale(bell, (140, 140))
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
        self.width = 50
        self.height = 50

        self.key = key

        self.colour = self.COLOR_INACTIVE
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.active = False

    def fill(self, surface, colour):
        w, h = surface.get_size()
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(colour[0], colour[1], colour[2], a))

    def setKey(self, key):
        self.key = key

    def draw(self, win):
        if self.stroke == "handstroke":
            win.blit(self.backstrokeBellBlank, self.rect)
            #pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 135, 135), 0)
            return win.blit(self.handstrokeBell, self.rect)
        else:
            win.blit(self.handstrokeBellBlank, self.rect)
            #pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, 135, 135), 0)
            return win.blit(self.backstrokeBell, self.rect)
        #return pygame.draw.rect(win, self.colour, self.rect, 0)

    def handle_event(self, event, send):
        if event == self.key:
            send(str(self.bellNumber))

    def bellRung(self):
        # Change the current colour of the bell
        self.active = not self.active
        self.stroke = "backstroke" if self.active else "handstroke"
        self.colour = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        
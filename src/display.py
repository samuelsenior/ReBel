import pygame

class Draw:
    def __init__(self, win):
        self.win = win

    def rect(self, *args):
        pygame.draw.rect(self.win, *args)

class Display:

    def __init__(self, width, height, caption=None, iconFile=None):

        self.width = width
        self.height = height
        self.caption = caption
        self.iconFile = iconFile

        self.win = pygame.display.set_mode((self.width, self.height))
        if self.caption:
            pygame.display.set_caption("ReBel")
        if self.iconFile:
            self.icon = pygame.image.load(self.iconFile)
            pygame.display.set_icon(self.icon)

        self.draw = Draw(self.win)

    def set_mode(self, *args):
        self.win = pygame.display.set_mode(*args)
        return self.win

    def updateScreenSize(self, width, height):
        self.win = pygame.display.set_mode((width, height))

    def blit(self, *args):
        self.win.blit(*args)

    def flip(self):
        pygame.display.flip()

    def subprocess(self):
        pass

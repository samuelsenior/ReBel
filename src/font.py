import pygame

import os

class Font(object):
    def __init__(self, directory):
        self.directory = directory
        pygame.font.init()
        self.FONT = pygame.font.Font(os.path.join(self.directory, "FreeSansBold.ttf"), 24)
        self.largeFont = pygame.font.Font(os.path.join(self.directory, "FreeSansBold.ttf"), 28)
        self.mediumFont = pygame.font.Font(os.path.join(self.directory, "FreeSansBold.ttf"), 24)
        self.smallFont = pygame.font.Font(os.path.join(self.directory, "FreeSansBold.ttf"), 20)
        self.tinyFont = pygame.font.Font(os.path.join(self.directory, "FreeSansBold.ttf"), 16)
        self.menu_font = pygame.font.Font(os.path.join(self.directory, "FreeSansBold.ttf"), 28)

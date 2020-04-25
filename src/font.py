import pygame

import os

class Font(object):
    def __init__(self):
        pygame.font.init()
        self.FONT = pygame.font.Font(os.path.join("..", "fonts", "freesansbold.ttf"), 24)
        self.largeFont = pygame.font.Font(os.path.join("..", "fonts", "freesansbold.ttf"), 28)
        self.mediumFont = pygame.font.Font(os.path.join("..", "fonts", "freesansbold.ttf"), 24)
        self.smallFont = pygame.font.Font(os.path.join("..", "fonts", "freesansbold.ttf"), 20)
        self.tinyFont = pygame.font.Font(os.path.join("..", "fonts", "freesansbold.ttf"), 16)
        self.menu_font = pygame.font.Font(os.path.join("..", "fonts", "freesansbold.ttf"), 28)

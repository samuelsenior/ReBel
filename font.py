import pygame

class Font(object):
    def __init__(self):
        pygame.font.init()
        self.FONT = pygame.font.Font(None, 32)
        self.smallFont = pygame.font.SysFont("comicsans", 32)
        self.menu_font = pygame.font.Font(None, 40)

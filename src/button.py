import pygame
import os
import sys

class Button:
    
    def __init__(self, text, pos, font, active=True, border=False, fontSize='menu', buttonColour=(200, 200, 200), borderColour=(170, 170, 170)):
        if getattr(sys, 'frozen', False):
            # In a bundle
            self.exeDir = os.path.dirname(sys.executable)
        else:
            # In normal python
            self.exeDir = ""
        self.font = font
        self.text = text
        self.pos = pos

        self.x = self.pos[0]
        self.y = self.pos[0]

        self.hovered = False
        self.active = active

        self.border = border

        self.fontSize = fontSize
        if self.fontSize == 'menu':
            self.font = self.font.menu_font
        elif self.fontSize == 'tiny':
            self.font = self.font.tinyFont
        elif self.fontSize == 'small':
            self.font = self.font.smallFont
        elif self.fontSize == 'medium':
            self.font = self.mediumFont
        elif self.fontSize == 'large':
            self.font = self.font.largeFont

        self.buttonColour = buttonColour
        self.borderColour = borderColour

        self.set_rect()
        self.width = self.rect.width

        self.updated = True

    def set_inactive(self):
        self.active = False
        self.hovered = True
            
    def draw(self, display):
        self.set_rend()

        if self.border:
            display.draw.rect(self.buttonColour, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
            display.blit(self.rend, (self.rect.x+5, self.rect.y))
            display.draw.rect(self.borderColour,(self.rect.x, self.rect.y, self.rect.w, self.rect.h), 2)
        else:
            display.draw.rect(self.buttonColour, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
            display.blit(self.rend, (self.rect.x+5, self.rect.y))
        
    def set_rend(self):
        self.rend = self.font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered and self.active == True:
            return (150, 150, 150)
        elif self.active == False:
            return (175, 175, 175)
        else:
            return (0, 0, 0)
        
    def set_rect(self):
        self.set_rend()
        self.rect = pygame.Rect(self.rend.get_rect().x, self.rend.get_rect().y, self.rend.get_rect().w+10, self.rend.get_rect().h)
        self.rect.topleft = self.pos

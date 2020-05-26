import pygame
import os
import sys

class TextBox:
    
    def __init__(self, text, pos, width, font, drawRect=False, textColour=(0, 0, 0), backgroundColour=None, fontSize=None):
        if getattr(sys, 'frozen', False):
            # In a bundle
            self.exeDir = os.path.dirname(sys.executable)
        else:
            # In normal python
            self.exeDir = ""
        self.text = text
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.width = width
        self.font = font
        self.drawRect = drawRect
        self.textColour = textColour
        self.backgroundColour = backgroundColour
        if fontSize == None:
            self.font = self.font.tinyFont
        elif fontSize == 'tiny':
            self.font = self.font.tinyFont
        elif fontSize == 'small':
            self.font = self.font.smallFont
        elif fontSize == 'medium':
            self.font = self.font.mediumFont
        elif fontSize == 'large':
            self.font = self.font.largeFont

        self.set_rect()

        self.generateFormattedText(self.y, self.width)

    def generateFormattedText(self, startingY, width):
        self.width = width
        self.textFormatted = []
        self.y = startingY
        y = 0 + self.y
        self.linespacing = -2
        self.fontHeight = self.font.size("Tg")[1]
        text = "" + self.text
        self.rect.h = 0
        while text:
            i = 1
            while self.font.size(text[:i])[0] < self.width and i < len(text):
                i += 1

            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            if self.backgroundColour:
                rend = self.font.render(text[:i], 1, self.textColour, self.backgroundColour)
                rend.set_colorkey(self.backgroundColour)
            else:
                rend = self.font.render(text[:i], 1, self.textColour)

            self.textFormatted.append((rend, (self.rect.x, y)))
            y += self.fontHeight + self.linespacing
            self.rect.h += y

            text = text[i:]

            if text == "":
                text = False
            else:
                pass

        if len(self.textFormatted) <= 2:
            self.h = (y - self.y)
        else:
            self.h = (y - self.y)
            
    def draw(self, display):
        for text in self.textFormatted:
            display.blit(*text)
        
    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, 0)
        self.rect.topleft = self.pos

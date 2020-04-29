import pygame
from font import Font

class TextBox(Font):
    
    def __init__(self, text, pos, width, drawRect=False, textColour=(0, 0, 0), backgroundColour=None, font=None):
        super().__init__()
        self.text = text
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.width = width
        self.drawRect = drawRect
        self.textColour = textColour
        self.backgroundColour = backgroundColour
        if font == None:
            self.font = self.tinyFont
        elif font == 'tiny':
            self.font = self.tinyFont
        elif font == 'small':
            self.font = self.smallFont
        elif font == 'medium':
            self.font = self.mediumFont
        elif font == 'large':
            self.font = self.largeFont

        self.set_rect()

        self.generateFormattedText(self.width)

    def generateFormattedText(self, width):
        self.width = width
        self.textFormatted = []
        y = 0 + self.y
        self.linespacing = -2
        self.fontHeight = self.font.size("Tg")[1]
        text = "" + self.text
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

        self.h = len(self.textFormatted) * (self.fontHeight + self.linespacing)
            
    def draw(self, win):
        for text in self.textFormatted:
            win.blit(*text)
        
    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, 0)
        self.rect.topleft = self.pos

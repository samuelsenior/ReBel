import pygame
from font import Font

class TextBox(Font):
    
    def __init__(self, text, pos, drawRect=False, textColour=(0, 0, 0), backgroundColour=(255, 255, 255), font=None):
        super().__init__()
        self.text = text
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
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

        #if self.drawRect:
        self.set_rect()

        self.w = self.rend.get_width()
        self.h = self.rend.get_height()
            
    def draw(self, win):
        self.set_rend()

        if self.drawRect:
            pygame.draw.rect(win, self.backgroundColour, (self.rect.x, self.rect.y, self.rect.w, self.rect.h))
        win.blit(self.rend, (self.rect.x, self.rect.y))
        
    def set_rend(self):
        self.rend = self.font.render(self.text, True, self.textColour)
        
    def set_rect(self):
        self.set_rend()
        self.rect = pygame.Rect(self.rend.get_rect().x, self.rend.get_rect().y, self.rend.get_rect().w, self.rend.get_rect().h)
        self.rect.topleft = self.pos

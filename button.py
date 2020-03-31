import pygame
from font import Font

class Button(Font):
    
    def __init__(self, text, pos, active=True):
        super().__init__()
        self.text = text
        self.pos = pos

        self.hovered = False
        self.active = active

        self.set_rect()
        self.width = self.rect.width

    def set_inactive(self):
        self.active = False
        self.hovered = True
            
    def draw(self, win):
        self.set_rend()

        pygame.draw.rect(win, (200, 200, 200), self.rect)
        win.blit(self.rend, (self.rect.x, self.rect.y+2))
        
    def set_rend(self):
        self.rend = self.menu_font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered and self.active == True:
            return (150, 150, 150)
        elif self.active == False:
            return (175, 175, 175)
        else:
            return (0, 0, 0)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

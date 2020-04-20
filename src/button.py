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

        self.updated = True

    def set_inactive(self):
        self.active = False
        self.hovered = True
            
    def draw(self, win):
        self.set_rend()

        return pygame.draw.rect(win, (200, 200, 200), (self.rect.x, self.rect.y, self.rect.w, self.rect.h)), win.blit(self.rend, (self.rect.x+5, self.rect.y))
        
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
        self.rect = pygame.Rect(self.rend.get_rect().x, self.rend.get_rect().y, self.rend.get_rect().w+10, self.rend.get_rect().h)
        self.rect.topleft = self.pos

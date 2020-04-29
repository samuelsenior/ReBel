import pygame
from font import Font

class Button(Font):
    
    def __init__(self, text, pos, active=True, border=False, fontSize='menu'):
        super().__init__()
        self.text = text
        self.pos = pos

        self.x = self.pos[0]
        self.y = self.pos[0]

        self.hovered = False
        self.active = active

        self.border = border

        self.fontSize = fontSize
        if self.fontSize == 'menu':
            self.font = self.menu_font
        elif self.fontSize == 'tiny':
            self.font = self.tinyFont
        elif self.fontSize == 'small':
            self.font = self.smallFont
        elif self.fontSize == 'medium':
            self.font = self.mediumFont
        elif self.fontSize == 'large':
            self.font = self.largeFont

        self.set_rect()
        self.width = self.rect.width

        self.updated = True

    def set_inactive(self):
        self.active = False
        self.hovered = True
            
    def draw(self, win):
        self.set_rend()

        if self.border:
            return pygame.draw.rect(win, (200, 200, 200), (self.rect.x, self.rect.y, self.rect.w, self.rect.h)), \
                   win.blit(self.rend, (self.rect.x+5, self.rect.y)), \
                   pygame.draw.rect(win, (100, 100, 100),(self.rect.x, self.rect.y, self.rect.w, self.rect.h), 2)
        else:
            return pygame.draw.rect(win, (200, 200, 200), (self.rect.x, self.rect.y, self.rect.w, self.rect.h)), win.blit(self.rend, (self.rect.x+5, self.rect.y))
        
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

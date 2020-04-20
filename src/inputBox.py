import pygame
from font import Font

class InputBox(Font):

    def __init__(self, x, y, w, h, text=''):

        super().__init__()

        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')

        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.rect = pygame.Rect(x, y, w, h)
        self.rectOld = self.rect.copy()
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.updated = True

    def mouseDownEvent(self, event, screen):
        # If the user clicked on the input_box rect.
        if self.rect.collidepoint(event.pos):
            # Toggle the active variable on.
            self.active = True
        else:
            self.active = False
        # Change the current color of the input box.
        self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

        self.updated = True

    def keyDownEvent(self, event, screen):
        if event.key == pygame.K_RETURN:
            pass
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode
        # Re-render the text.
        self.txt_surface = self.FONT.render(self.text, True, self.color)
        self.update()

        self.updated = True

        return [screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+2)), pygame.draw.rect(screen, self.color, self.rect, 2)]

    def update(self):
        # Resize the box if the text is too long.
        self.rectOld = self.rect.copy()
        self.rectOld.w = self.rectOld.w + 10
        self.rectOld.h = self.rectOld.h + 10
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        return [pygame.draw.rect(screen, (255, 255, 255), self.rectOld, 0), screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+2)), pygame.draw.rect(screen, self.color, self.rect, 2)]
        
import pygame
import os
import sys
from font import Font

class InputBox(Font):

    def __init__(self, x, y, w, h, font, text='', fontSize='medium', resizable=True, startActiveText=False, characterLimit=1000, inputType=None):
        if getattr(sys, 'frozen', False):
            # In a bundle
            self.exeDir = os.path.dirname(sys.executable)
        else:
            # In normal python
            self.exeDir = ""
        Font.__init__(self, directory=os.path.join(self.exeDir, "..", "fonts"))

        self.colour_inactive = pygame.Color('lightskyblue3')
        self.colour_active = pygame.Color('dodgerblue2')

        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.font = font
        self.rect = pygame.Rect(x, y, w, h)
        self.rectOld = self.rect.copy()
        self.color = self.colour_inactive
        self.text = text
        self.resizable = resizable
        self.characterLimit = characterLimit
        self.inputType = inputType

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

        if startActiveText:
            self.txt_surface = self.font.render(text, True, self.colour_active)
        else:
            self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.updated = True

        self.characterWidth = self.font.size("W")[0]
        self.text_width = self.txt_surface.get_width()

    def get(self):
        return self.text

    def mouseDownEvent(self, event, screen):
        # If the user clicked on the input_box rect.
        if self.rect.collidepoint(event.pos):
            # Toggle the active variable on.
            self.active = True
        else:
            self.active = False
        # Change the current color of the input box.
        self.color = self.colour_active if self.active else self.colour_inactive

        self.updated = True

    def keyDownEvent(self, event, screen):
        if event.key == pygame.K_RETURN:
            pass
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif self.rect.w < self.text_width + self.characterWidth:
            if self.text[0] == " " and len(self.text[1:]) < self.characterLimit:
                if self.inputType == 'numeric' and event.unicode.isdigit():
                    self.text = self.text[1:] + event.unicode
                elif self.inputType == 'numericAndLetter' and (event.unicode.isdigit() or event.unicode.isalpha()):
                    self.text = self.text[1:] + event.unicode
                elif self.inputType == None:
                    self.text = self.text[1:] + event.unicode
        elif len(self.text) < self.characterLimit:
            if self.inputType == 'numeric' and event.unicode.isdigit():
                self.text += event.unicode
            elif self.inputType == 'numericAndLetter' and (event.unicode.isdigit() or event.unicode.isalpha()):
                self.text += event.unicode
            elif self.inputType == None:
                self.text += event.unicode
        elif self.text[0] == " " and len(self.text[1:]) < self.characterLimit:
            if self.inputType == 'numeric' and event.unicode.isdigit():
                self.text += event.unicode
            elif self.inputType == 'numericAndLetter' and (event.unicode.isdigit() or event.unicode.isalpha()):
                self.text += event.unicode
            elif self.inputType == None:
                self.text += event.unicode
        # Re-render the text.
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.text_width = self.txt_surface.get_width()
        self.update()

        self.updated = True

        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+2))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self):
        # Resize the box if the text is too long.
        self.rectOld = self.rect.copy()
        if self.resizable == True:
            self.rectOld.w = self.rectOld.w + 1
            self.rectOld.h = self.rectOld.h + 1
            width = max(self.width, self.txt_surface.get_width()+10)
            self.rect.w = width
        else:
            self.rectOld.w = self.rectOld.w
            self.rectOld.h = self.rectOld.h
            self.rect.w = self.width

    def draw(self, display):
        display.draw.rect((255, 255, 255), self.rectOld, 0)
        display.blit(self.txt_surface, (self.rect.x+5, self.rect.y+2))
        display.draw.rect(self.color, self.rect, 2)
        
from inputBox import InputBox

class TitledInputBox(InputBox):
    def __init__(self, title, x, y, w, h, font, text='', fontSize='medium', resizable=True, startActiveText=False, characterLimit=1000, inputType=None):
        super().__init__(x, y, w, h, text=text, font=font, fontSize=fontSize, resizable=resizable, startActiveText=startActiveText,
                         characterLimit=characterLimit, inputType=inputType)

        self.font = font
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

        self.title = self.font.render(title, True, (0, 0, 0))

        self.redrawTitle = True

    def draw(self, win, redrawTitle=False):
        if redrawTitle or self.redrawTitle:
            self.redrawTitle = False
            super().draw(win)
            win.blit(self.title, (self.x - self.title.get_width()-5, self.y+2))
        else:
            super().draw(win)
        
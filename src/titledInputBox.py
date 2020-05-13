from inputBox import InputBox

class TitledInputBox(InputBox):
    def __init__(self, title, x, y, w, h, text='', font='medium', resizable=True, startActiveText=False, characterLimit=1000, inputType=None):
        super().__init__(x, y, w, h, text=text, font=font, resizable=resizable, startActiveText=startActiveText,
                         characterLimit=characterLimit, inputType=inputType)

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

        self.title = self.font.render(title, True, (0, 0, 0))

        self.redrawTitle = True

    def draw(self, win, redrawTitle=False):
        if redrawTitle or self.redrawTitle:
            self.redrawTitle = False
            super().draw(win)
            win.blit(self.title, (self.x - self.title.get_width()-5, self.y+2))
        else:
            super().draw(win)
        
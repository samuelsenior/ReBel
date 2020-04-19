from inputBox import InputBox

class TitledInputBox(InputBox):
    def __init__(self, title, x, y, w, h, text=''):
        super().__init__(x, y, w, h, text=text)
        self.title = self.FONT.render(title, True, (0, 0, 0))

    def draw(self, win, redrawTitle=True):
        if redrawTitle:
            return super().draw(win).append(win.blit(self.title, (self.x - self.title.get_width() - 5, self.y + self.title.get_height() / 2 - 7)))
        else:
            return super().draw(win)
        
import pygame

from button import Button
from inputBox import InputBox
from textBox import TextBox
from titledInputBox import TitledInputBox

class OptionsScreen:

    def __init__(self, win, config, frameRate):
        self.win = win
        self.config = config
        self.frameRate = frameRate

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        self.optionsBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)

        self.button_back = Button("Back", (self.x + 20, self.height + self.y - 20))
        self.button_back.rect.y -= self.button_back.rect.h
        #
        self.button_other = Button("Other", (self.x + self.width - 20, self.y + 20))
        self.button_other.rect.x -= self.button_other.rect.w
        #
        self.button_tuning = Button("Tuning", (self.button_other.x - self.button_other.rect.w - 10, self.y + 20))
        self.button_tuning.rect.x -= self.button_tuning.rect.w
        #
        self.button_keys = Button("keys", (self.button_tuning.x - self.button_tuning.rect.w - 10, self.y + 20))
        self.button_keys.rect.x -= self.button_keys.rect.w
        #
        self.buttons = [self.button_back, self.button_keys, self.button_tuning, self.button_other]

        self.keysTitleText = TextBox('Keys Options:',
                                        (self.x+20, self.y+self.button_keys.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font='large')
        self.keysSubTitleText_1 = TextBox('Bell Keys:',
                                             (self.x+20, self.keysTitleText.y+self.keysTitleText.h+10), width=self.width-40, font='small')
        self.keysText_1 = TextBox("",
                                     (self.x+20, self.keysSubTitleText_1.y+self.keysSubTitleText_1.h+7), width=self.width-40, font='tiny')
        self.keysText_2 = TextBox("",
                                     (self.x+20, self.keysText_1.y+self.keysText_1.h+10), width=self.width-40, font='tiny')
        self.keysText = [self.keysTitleText, self.keysSubTitleText_1, self.keysText_1, self.keysText_2]

        self.tuningTitleText = TextBox('Tuning Options:',
                                       (self.x+20, self.y+self.button_tuning.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font='large')
        self.tuningSubTitleText_1 = TextBox('Octave and Semitone Shift:',
                                            (self.x+20, self.tuningTitleText.y+self.tuningTitleText.h+10), width=self.width-40, font='small')
        self.tuningText_1 = TextBox("... still to do...",
                                     (self.x+20, self.tuningSubTitleText_1.y+self.tuningSubTitleText_1.h+7), width=self.width-40, font='tiny')
        self.tuningText = [self.tuningTitleText, self.tuningSubTitleText_1, self.tuningText_1]

        self.otherTitleText = TextBox('Other Options:',
                                       (self.x+20, self.y+self.button_other.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font='large')
        self.otherSubTitleText_1 = TextBox('...:',
                                            (self.x+20, self.otherTitleText.y+self.otherTitleText.h+10), width=self.width-40, font='small')
        self.otherText_1 = TextBox("... still to do...",
                                     (self.x+20, self.otherSubTitleText_1.y+self.otherSubTitleText_1.h+7), width=self.width-40, font='tiny')
        self.otherText = [self.otherTitleText, self.otherSubTitleText_1, self.otherText_1]

    def realignButtons(self):
        self.button_back.rect.x = self.x + 20

        self.button_other.rect.x = self.x + self.width - 20 - self.button_other.rect.w
        self.button_tuning.rect.x = self.button_other.rect.x - self.button_tuning.rect.w - 10
        self.button_keys.rect.x = self.button_tuning.rect.x - self.button_keys.rect.w - 10

    def generateBellKeyInputBoxes(self, startingX, y):
        self.bellNumberInputBoxes = []
        self.bellKeyInputBoxes = []
        if self.config.get('numberOfBells') >= 100:
            width = 48
        else:
            width = 32
        for i in range(self.config.get('numberOfBells')):
            if i+1 < 10:
                bellNo = " " + str(self.config.get('ringableBells')[i])
            else:
                bellNo = str(self.config.get('ringableBells')[i])
            key = " " + str(self.config.get('keys')[i])
            if i == 0:
                try:
                    self.bellNumberInputBoxes.append(TitledInputBox("Ringable Bells:", startingX+i*10, y, width, 30, font='small',
                                                     resizable=False, text=bellNo, startActiveText=True, inputType='numeric'))
                    self.bellKeyInputBoxes.append(TitledInputBox("Key Press:", startingX+i*10, y+30+5, width, 30, font='small',
                                                  resizable=False, text=key, startActiveText=True, characterLimit=1))
                except:
                    self.bellNumberInputBoxes.append(TitledInputBox("Bell No.", startingX+i*10, y, width, 30, font='small',
                                                     resizable=False, startActiveText=True, inputType='numeric'))
                    self.bellKeyInputBoxes.append(TitledInputBox("Key Press:", startingX+i*10, y+30+5, width, 30, font='small',
                                                  resizable=False, startActiveText=True, characterLimit=1))
            else:
                try:
                    self.bellNumberInputBoxes.append(InputBox(self.bellNumberInputBoxes[-1].x+width+10, y, width, 30, font='small',
                                                  resizable=False, text=bellNo, startActiveText=True, inputType='numeric'))
                    self.bellKeyInputBoxes.append(InputBox(self.bellKeyInputBoxes[-1].x+width+10, y+30+5, width, 30, font='small',
                                                  resizable=False, text=key, startActiveText=True, characterLimit=1))
                except:
                    self.bellNumberInputBoxes.append(InputBox(self.bellNumberInputBoxes[-1].x+width+10, y, width, 30, font='small',
                                                     resizable=False, startActiveText=True, inputType='numeric'))
                    self.bellKeyInputBoxes.append(InputBox(self.bellKeyInputBoxes[-1].x+width+10, y+30+5, width, 30, font='small',
                                                  resizable=False, startActiveText=True, characterLimit=1))
        self.activeBox = None

    def drawBackground(self):
        pygame.draw.rect(self.win, (170, 170, 170), self.optionsBackground, 0)
        pygame.draw.rect(self.win, (100, 100, 100), self.optionsBackground, 2)

    def display(self, win, source):
        self.win = win

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        self.optionsBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)


        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        for keysText in self.keysText:
            keysText.rect.x = self.x + 20
            keysText.generateFormattedText(width=self.width-40)
        for tuningText in self.tuningText:
            tuningText.rect.x = self.x + 20
            tuningText.generateFormattedText(width=self.width-40)
        for otherText in self.otherText:
            otherText.rect.x = self.x + 20
            otherText.generateFormattedText(width=self.width-40)

        self.realignButtons()

        self.generateBellKeyInputBoxes(self.x+170, self.keysText_1.rect.y)

        self.win.blit(self.backgroundFade, (0, 0))

        optionsPage = "keys"

        if optionsPage == "keys":
            text = self.keysText
            self.button_keys.active = False
            self.button_tuning.active = True
            self.button_other.active = True
        else:
            text = self.keysText
            self.button_keys.active = False
            self.button_tuning.active = True
            self.button_other.active = True

        self.drawBackground()

        self.bellNumberInputBoxes[0].draw(self.win, redrawTitle=True)
        self.bellNumberInputBoxes[0].updated = False
        for box in self.bellNumberInputBoxes[1:]:
            box.draw(self.win)
            box.updated = False
        self.bellKeyInputBoxes[0].draw(self.win, redrawTitle=True)
        self.bellKeyInputBoxes[0].updated = False
        for box in self.bellKeyInputBoxes[1:]:
            box.draw(self.win)
            box.updated = False
        for button in self.buttons:
            if button.updated:
                button.hovered = False
                button.draw(self.win)

        for txt in text:
            txt.draw(self.win)

        pygame.display.update()
        
        clock = pygame.time.Clock()
        
        run_options = True
        while run_options:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_options = False
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_back.rect.collidepoint(event.pos):
                        run_options = False
                        return source
                    elif self.button_keys.rect.collidepoint(event.pos) and self.button_keys.active == True:
                        optionsPage = 'keys'
                        self.bellNumberInputBoxes[0].redrawTitle = True
                        self.bellKeyInputBoxes[0].redrawTitle = True
                        text = self.keysText
                        self.button_tuning.active = True
                        self.button_keys.active = False
                        self.button_other.active = True
                        self.drawBackground()
                        for txt in text:
                            txt.draw(self.win)
                    elif self.button_tuning.rect.collidepoint(event.pos) and self.button_tuning.active == True:
                        optionsPage = 'tuning'
                        text = self.tuningText
                        self.button_keys.active = True
                        self.button_tuning.active = False
                        self.button_other.active = True
                        self.drawBackground()
                        for txt in text:
                            txt.draw(self.win)
                    elif self.button_other.rect.collidepoint(event.pos) and self.button_other.active == True:
                        optionsPage = 'other'
                        text = self.otherText
                        self.button_keys.active = True
                        self.button_tuning.active = True
                        self.button_other.active = False
                        self.drawBackground()
                        for txt in text:
                            txt.draw(self.win)

                    for box in self.bellNumberInputBoxes:
                        box.mouseDownEvent(event, self.win)
                        if box.active == True:
                            self.activeBox = box
                    for box in self.bellKeyInputBoxes:
                        box.mouseDownEvent(event, self.win)
                        if box.active == True:
                            self.activeBox = box

                if event.type == pygame.KEYDOWN:
                    if self.activeBox and self.activeBox.active:
                        self.activeBox.keyDownEvent(event, self.win)

                for button in self.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                        button.updated = True
                    elif button.active == True:
                        button.hovered = False
                        button.updated = True

            if optionsPage == 'keys':
                for box in self.bellNumberInputBoxes:
                    if box.updated:
                        box.draw(self.win)
                        box.updated = False
                for box in self.bellKeyInputBoxes:
                    if box.updated:
                        box.draw(self.win)
                        box.updated = False

            for button in self.buttons:
                if button.updated:
                    button.draw(self.win)

            pygame.display.flip()
            clock.tick(self.frameRate)

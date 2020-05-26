import pygame

from button import Button
from inputBox import InputBox
from textBox import TextBox
from titledInputBox import TitledInputBox

class OptionsScreen:

    def __init__(self, win, font, config, frameRate):
        self.win = win
        self.font = font
        self.config = config
        self.frameRate = frameRate

        self.bellKeysUpdated = False

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        self.optionsBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)

        self.button_back = Button("Cancel", (self.x + 20, self.height + self.y - 20), font=self.font)
        self.button_back.rect.y -= self.button_back.rect.h
        #
        self.button_save = Button("Save", (self.x + self.width - 20, self.height + self.y - 20), font=self.font)
        self.button_save.rect.x -= self.button_save.rect.w
        self.button_save.rect.y -= self.button_save.rect.h
        #
        self.button_other = Button("Other", (self.x + self.width - 20, self.y + 20), font=self.font)
        self.button_other.rect.x -= self.button_other.rect.w
        #
        self.button_tuning = Button("Tuning", (self.button_other.x - self.button_other.rect.w - 10, self.y + 20), font=self.font)
        self.button_tuning.rect.x -= self.button_tuning.rect.w
        #
        self.button_keys = Button("keys", (self.button_tuning.x - self.button_tuning.rect.w - 10, self.y + 20), font=self.font)
        self.button_keys.rect.x -= self.button_keys.rect.w
        #
        self.buttons = [self.button_back, self.button_save]#, self.button_keys, self.button_tuning, self.button_other]

        self.keysTitleText = TextBox('Keys Options:',
                                     (self.x+20, self.y+self.button_keys.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font=self.font, fontSize='large')
        self.keysSubTitleText_1 = TextBox('Bell Keys:',
                                          (self.x+20, self.keysTitleText.y+self.keysTitleText.h+10), width=self.width-40, font=self.font, fontSize='small')
        self.keysText_1 = TextBox("In the 'Ringable Bells' row of boxes enter in the bell numbers of the bells that you want to ring.",
                                  (self.x+20, self.keysSubTitleText_1.y+self.keysSubTitleText_1.h+7), width=self.width-40, font=self.font, fontSize='tiny')
        self.keysText_2 = TextBox("In the 'Key Press' row of boxes enter in the keys you want to press to ring each bell.",
                                  (self.x+20, self.keysText_1.y+self.keysText_1.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.keysText_3 = TextBox("Each 'Key Press' box corresponds to the 'Ringable Bell' box above it.",
                                  (self.x+20, self.keysText_2.y+self.keysText_2.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.keysText_4 = TextBox("Only numbers can be entered into the 'Ringable Bell' boxes and only letters and numbers can be entered " + \
                                  "into the 'Key Press' boxes.",
                                  (self.x+20, self.keysText_3.y+self.keysText_3.h+10), width=self.width-40, font=self.font, fontSize='tiny')
        self.keysText = [self.keysTitleText, self.keysSubTitleText_1, self.keysText_1, self.keysText_2, self.keysText_3, self.keysText_4]

        self.tuningTitleText = TextBox('Tuning Options:',
                                       (self.x+20, self.y+self.button_tuning.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font=self.font, fontSize='large')
        self.tuningSubTitleText_1 = TextBox('Octave and Semitone Shift:',
                                            (self.x+20, self.tuningTitleText.y+self.tuningTitleText.h+10), width=self.width-40, font=self.font, fontSize='small')
        self.tuningText_1 = TextBox("... still to do...",
                                     (self.x+20, self.tuningSubTitleText_1.y+self.tuningSubTitleText_1.h+7), width=self.width-40, font=self.font, fontSize='tiny')
        self.tuningText = [self.tuningTitleText, self.tuningSubTitleText_1, self.tuningText_1]

        self.otherTitleText = TextBox('Other Options:',
                                       (self.x+20, self.y+self.button_other.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font=self.font, fontSize='large')
        self.otherSubTitleText_1 = TextBox('...:',
                                            (self.x+20, self.otherTitleText.y+self.otherTitleText.h+10), width=self.width-40, font=self.font, fontSize='small')
        self.otherText_1 = TextBox("... still to do...",
                                     (self.x+20, self.otherSubTitleText_1.y+self.otherSubTitleText_1.h+7), width=self.width-40, font=self.font, fontSize='tiny')
        self.otherText = [self.otherTitleText, self.otherSubTitleText_1, self.otherText_1]

    def realignButtons(self):
        self.button_back.rect.x = self.x + 20
        self.button_save.rect.x = self.x + self.width - self.button_save.rect.w - 20

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
                try:
                    bellNo = " " + str(self.config.get('ringableBells')[i])
                except:
                    bellNo = ""
            else:
                try:
                    bellNo = str(self.config.get('ringableBells')[i])
                except:
                    bellNo = ""
            try:
                key = " " + str(self.config.get('keys')[i])
            except:
                key = ""
            if i == 0:
                try:
                    self.bellNumberInputBoxes.append(TitledInputBox("Ringable Bells:", startingX+i*10, y, width, 30, font=self.font, fontSize='small',
                                                     resizable=False, text=bellNo, startActiveText=True, inputType='numeric'))
                    self.bellKeyInputBoxes.append(TitledInputBox("Key Press:", startingX+i*10, y+30+5, width, 30, font=self.font, fontSize='small',
                                                  resizable=False, text=key, startActiveText=True, characterLimit=1, inputType='numericAndLetter'))
                except:
                    self.bellNumberInputBoxes.append(TitledInputBox("Bell No.", startingX+i*10, y, width, 30, font=self.font, fontSize='small',
                                                     resizable=False, startActiveText=True, inputType='numeric'))
                    self.bellKeyInputBoxes.append(TitledInputBox("Key Press:", startingX+i*10, y+30+5, width, 30, font=self.font, fontSize='small',
                                                  resizable=False, startActiveText=True, characterLimit=1, inputType='numericAndLetter'))
            else:
                try:
                    self.bellNumberInputBoxes.append(InputBox(self.bellNumberInputBoxes[-1].x+width+10, y, width, 30, font=self.font, fontSize='small',
                                                  resizable=False, text=bellNo, startActiveText=True, inputType='numeric'))
                    self.bellKeyInputBoxes.append(InputBox(self.bellKeyInputBoxes[-1].x+width+10, y+30+5, width, 30, font=self.font, fontSize='small',
                                                  resizable=False, text=key, startActiveText=True, characterLimit=1, inputType='numericAndLetter'))
                except:
                    self.bellNumberInputBoxes.append(InputBox(self.bellNumberInputBoxes[-1].x+width+10, y, width, 30, font=self.font, fontSize='small',
                                                     resizable=False, startActiveText=True, inputType='numeric'))
                    self.bellKeyInputBoxes.append(InputBox(self.bellKeyInputBoxes[-1].x+width+10, y+30+5, width, 30, font=self.font, fontSize='small',
                                                  resizable=False, startActiveText=True, characterLimit=1, inputType='numericAndLetter'))
        self.activeBox = None

    def saveConfig(self):
        bellNumberList = []
        bellKeyList = []
        for i, bellNumberBox in enumerate(self.bellNumberInputBoxes):
            bellNumber = bellNumberBox.get().replace(" ", "")
            bellKey = self.bellKeyInputBoxes[i].get().replace(" ", "")

            try:
                bellNumber = int(bellNumber)
            except:
                pass
            else:
                if bellNumber != "" and bellKey != "" and bellNumber > 0 and bellNumber <= self.config.get('numberOfBells'):
                    try:
                        bellNumberList.append(bellNumber)
                        bellKeyList.append(bellKey)
                    except:
                        pass

        self.config.set('ringableBells', bellNumberList)
        self.config.set('keys', bellKeyList)

    def drawBackground(self, display):
        display.draw.rect((170, 170, 170), self.optionsBackground, 0)
        display.draw.rect((100, 100, 100), self.optionsBackground, 2)

    def display(self, display, source):
        self.win = display.win

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        self.optionsBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)


        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        for i, keysText in enumerate(self.keysText):
            keysText.rect.x = self.x + 20
            if i == 0:
                startingY = keysText.y
            else:
                startingY = self.keysText[i-1].y + self.keysText[i-1].h+10
            keysText.generateFormattedText(startingY=startingY, width=self.width-40)
        for i, tuningText in enumerate(self.tuningText):
            tuningText.rect.x = self.x + 20
            if i == 0:
                startingY = tuningText.y
            else:
                startingY = self.tuningText[i-1].y + self.tuningText[i-1].h+10
            tuningText.generateFormattedText(startingY=startingY, width=self.width-40)
        for i, otherText in enumerate(self.otherText):
            otherText.rect.x = self.x + 20
            if i == 0:
                startingY = otherText.y
            else:
                startingY = self.otherText[i-1].y + self.otherText[i-1].h+10
            otherText.generateFormattedText(startingY=startingY, width=self.width-40)

        self.realignButtons()

        self.generateBellKeyInputBoxes(self.x+170, self.keysText_4.y+self.keysText_4.h + 10)

        display.blit(self.backgroundFade, (0, 0))

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

        self.drawBackground(display)

        self.bellNumberInputBoxes[0].draw(display, redrawTitle=True)
        self.bellNumberInputBoxes[0].updated = False
        for box in self.bellNumberInputBoxes[1:]:
            box.draw(display)
            box.updated = False
        self.bellKeyInputBoxes[0].draw(display, redrawTitle=True)
        self.bellKeyInputBoxes[0].updated = False
        for box in self.bellKeyInputBoxes[1:]:
            box.draw(display)
            box.updated = False
        for button in self.buttons:
            if button.updated:
                button.hovered = False
                button.draw(display)

        for txt in text:
            txt.draw(display)

        display.flip()
        
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
                        self.bellKeysUpdated = False
                        return source
                    elif self.button_save.rect.collidepoint(event.pos):
                        run_options = False
                        self.saveConfig()
                        self.bellKeysUpdated = True
                        return source
                    elif self.button_keys.rect.collidepoint(event.pos) and self.button_keys.active == True:
                        optionsPage = 'keys'
                        self.bellNumberInputBoxes[0].redrawTitle = True
                        self.bellKeyInputBoxes[0].redrawTitle = True
                        text = self.keysText
                        self.button_tuning.active = True
                        self.button_keys.active = False
                        self.button_other.active = True
                        self.drawBackground(display)
                        for txt in text:
                            txt.draw(display)
                    elif self.button_tuning.rect.collidepoint(event.pos) and self.button_tuning.active == True:
                        optionsPage = 'tuning'
                        text = self.tuningText
                        self.button_keys.active = True
                        self.button_tuning.active = False
                        self.button_other.active = True
                        self.drawBackground(display)
                        for txt in text:
                            txt.draw(display)
                    elif self.button_other.rect.collidepoint(event.pos) and self.button_other.active == True:
                        optionsPage = 'other'
                        text = self.otherText
                        self.button_keys.active = True
                        self.button_tuning.active = True
                        self.button_other.active = False
                        self.drawBackground(display)
                        for txt in text:
                            txt.draw(display)

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
                        box.draw(display)
                        box.updated = False
                for box in self.bellKeyInputBoxes:
                    if box.updated:
                        box.draw(display)
                        box.updated = False

            for button in self.buttons:
                if button.updated:
                    button.draw(display)

            display.flip()
            clock.tick(self.frameRate)

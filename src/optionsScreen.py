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

        self.configUpdated = False

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        self.optionsBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)

        self.generateMenuButtons()

        self.generateKeysPageText()
        self.generateTuningMenu()

        self.generateOtherMenuText()

    def generateMenuButtons(self):
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
        self.button_tuning = Button("Tuning", (self.x + self.width - 20, self.y + 20), font=self.font)
        #self.button_tuning = Button("Tuning", (self.button_other.x - self.button_other.rect.w - 10, self.y + 20), font=self.font)
        self.button_tuning.rect.x -= self.button_tuning.rect.w
        #
        self.button_keys = Button("keys", (self.button_tuning.x - self.button_tuning.rect.w - 10, self.y + 20), font=self.font)
        self.button_keys.rect.x -= self.button_keys.rect.w
        #
        self.buttons = [self.button_back, self.button_save, self.button_keys, self.button_tuning]#, self.button_other]

    def generateKeysPageText(self):
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

    def generateOtherMenuText(self):
        self.otherTitleText = TextBox('Other Options:',
                                       (self.x+20, self.y+self.button_other.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font=self.font, fontSize='large')
        self.otherSubTitleText_1 = TextBox('...:',
                                            (self.x+20, self.otherTitleText.y+self.otherTitleText.h+10), width=self.width-40, font=self.font, fontSize='small')
        self.otherText_1 = TextBox("... still to do...",
                                     (self.x+20, self.otherSubTitleText_1.y+self.otherSubTitleText_1.h+7), width=self.width-40, font=self.font, fontSize='tiny')
        self.otherText = [self.otherTitleText, self.otherSubTitleText_1, self.otherText_1]

    def realignMenuButtons(self):
        self.button_back.rect.x = self.x + 20
        self.button_save.rect.x = self.x + self.width - self.button_save.rect.w - 20

        self.button_other.rect.x = self.x + self.width - 20 - self.button_other.rect.w
        self.button_tuning.rect.x = self.x + self.width - 20 - self.button_tuning.rect.w
        #self.button_tuning.rect.x = self.button_other.rect.x - self.button_tuning.rect.w - 10
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

    def generateTuningMenu(self):
        self.tuningTitleText = TextBox('Tuning Options:',
                                       (self.x+20, self.y+self.button_tuning.rect.h+20), width=self.width-40, backgroundColour=(150, 150, 150), font=self.font, fontSize='large')
        self.tuningText_1 = TextBox("The tuning of the bells can be set from the server so that everyone has the same bell tunings. " + \
                                    "Alternatively, they can be set manually below.",
                                     (self.x+20, self.tuningTitleText.y+self.tuningTitleText.h+10), width=self.width-40, font=self.font, fontSize='tiny')

        self.tuningServerButton = Button("X", (self.x+40, self.tuningText_1.y+self.tuningText_1.h+15), font=self.font, fontSize='small', activeNotHoveredTextColour=(0, 0, 0), textColour=(200, 200, 200))
        self.tuningServerButtonText = TextBox("Get bell tunings from the server.",
                                              (self.tuningServerButton.x+self.tuningServerButton.width+10, self.tuningServerButton.y+3),
                                              width=self.width-40, font=self.font, fontSize='tiny')


        self.tuningClientButton = Button("X", (self.x+40, self.tuningServerButton.y+self.tuningServerButton.h+10), font=self.font, fontSize='small', activeNotHoveredTextColour=(0, 0, 0), textColour=(200, 200, 200))
        self.tuningClientButtonText = TextBox("Get bell tunings from below.",
                                              (self.tuningClientButton.x+self.tuningClientButton.width+10, self.tuningClientButton.y+3),
                                              width=self.width-40, font=self.font, fontSize='tiny')

        self.tuningSubTitleText_1 = TextBox('Octave Shift:',
                                            (self.x+20, self.tuningClientButton.y+self.tuningClientButton.h+15), width=self.width-40, font=self.font, fontSize='small')
        self.bellOctaveShiftBox = InputBox(self.x+40, self.tuningSubTitleText_1.y+self.tuningSubTitleText_1.h+7, self.tuningClientButton.width, 30, font=self.font, fontSize='small',
                                           resizable=False, text=str(self.config.get('octaveShift')), startActiveText=True, inputType='numeric')
        self.tuningText_2 = TextBox("Number of octaves to shift the bells by (positive for higher pitches, negative for lower).",
                                     (self.bellOctaveShiftBox.x+self.bellOctaveShiftBox.width+10, self.tuningSubTitleText_1.y+self.tuningSubTitleText_1.h+12),
                                     width=self.width-40, font=self.font, fontSize='tiny')
        self.tuningSubTitleText_2 = TextBox('Semitone Shift:',
                                            (self.x+20, self.tuningText_2.y+self.tuningText_2.h+15), width=self.width-40, font=self.font, fontSize='small')
        self.bellSemitoneShiftBox = InputBox(self.x+40, self.tuningSubTitleText_2.y+self.tuningSubTitleText_2.h+7, self.tuningClientButton.width, 30, font=self.font, fontSize='small',
                                           resizable=False, text=str(self.config.get('semitoneShift')), startActiveText=True, inputType='numeric')
        self.tuningText_3 = TextBox("Number of semitones to shift the bells by (positive for higher pitches, negative for lower).",
                                     (self.bellOctaveShiftBox.x+self.bellOctaveShiftBox.width+10, self.tuningSubTitleText_2.y+self.tuningSubTitleText_2.h+12),
                                     width=self.width-40, font=self.font, fontSize='tiny')

        self.tuningSubTitleText_3 = TextBox('Scale:',
                                            (self.x+20, self.tuningText_3.y+self.tuningText_3.h+15), width=self.width-40, font=self.font, fontSize='small')
        self.tuningText_4 = TextBox("The bells can be set to either the major scale or the natural, harmonic, or melodic minor scale.",
                                     (self.x+20, self.tuningSubTitleText_3.y+self.tuningSubTitleText_3.h+10), width=self.width-40, font=self.font, fontSize='tiny')

        self.tuningMajorScaleButton = Button("Major", (self.x+40, self.tuningText_4.y+self.tuningText_4.h+10), font=self.font, fontSize='small')
        self.tuningNaturalMinorScaleButton = Button("Natural Minor", (self.tuningMajorScaleButton.x+self.tuningMajorScaleButton.width+10, self.tuningText_4.y+self.tuningText_4.h+10), font=self.font, fontSize='small')
        self.tuningHarmonicMinorScaleButton = Button("Harmonic Minor", (self.tuningNaturalMinorScaleButton.x+self.tuningNaturalMinorScaleButton.width+10, self.tuningText_4.y+self.tuningText_4.h+10), font=self.font, fontSize='small')
        self.tuningMelodicMinorScaleButton = Button("Melodic Minor", (self.tuningHarmonicMinorScaleButton.x+self.tuningHarmonicMinorScaleButton.width+10, self.tuningText_4.y+self.tuningText_4.h+10), font=self.font, fontSize='small')

        self.tuningText = [self.tuningTitleText, self.tuningText_1, self.tuningServerButtonText, self.tuningClientButtonText,
                           self.tuningSubTitleText_1, self.tuningText_2, self.tuningSubTitleText_2, self.tuningText_3,
                           self.tuningSubTitleText_3, self.tuningText_4]

        self.buttons_tuning = [self.tuningServerButton, self.tuningClientButton,
                               self.tuningMajorScaleButton, self.tuningNaturalMinorScaleButton, self.tuningHarmonicMinorScaleButton, self.tuningMelodicMinorScaleButton]

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

        if not self.tuningServerButton.active:
            self.config.set('tuningSource', 'server')
        elif not self.tuningClientButton.active:
            self.config.set('tuningSource', 'client')
        else:
            self.config.set('tuningSource', 'server')

        if not self.tuningMajorScaleButton.active:
            self.config.set('scale', 'major')
        elif not self.tuningNaturalMinorScaleButton.active:
            self.config.set('scale', 'naturalMinor')
        elif not self.tuningHarmonicMinorScaleButton.active:
            self.config.set('scale', 'harmonicMinor')
        elif not self.tuningMelodicMinorScaleButton.active:
            self.config.set('scale', 'melodicMinor')
        else:
            self.config.set('scale', 'major')

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

        self.realignMenuButtons()

        self.generateBellKeyInputBoxes(self.x+170, self.keysText_4.y+self.keysText_4.h + 10)

        self.generateTuningMenu()

        if self.config.get('tuningSource') == 'server':
            self.tuningServerButton.active = False
            self.tuningClientButton.active = True
        else:
            self.tuningServerButton.active = True
            self.tuningClientButton.active = False

        if self.config.get('scale') == 'major':
            self.tuningMajorScaleButton.active = False
            self.tuningNaturalMinorScaleButton.active = True
            self.tuningHarmonicMinorScaleButton.active = True
            self.tuningMelodicMinorScaleButton.active = True
        elif self.config.get('scale') == 'naturalMinor':
            self.tuningMajorScaleButton.active = True
            self.tuningNaturalMinorScaleButton.active = False
            self.tuningHarmonicMinorScaleButton.active = True
            self.tuningMelodicMinorScaleButton.active = True
        elif self.config.get('scale') == 'harmonicMinor':
            self.tuningMajorScaleButton.active = True
            self.tuningNaturalMinorScaleButton.active = True
            self.tuningHarmonicMinorScaleButton.active = False
            self.tuningMelodicMinorScaleButton.active = True
        elif self.config.get('scale') == 'melodicMinor':
            self.tuningMajorScaleButton.active = True
            self.tuningNaturalMinorScaleButton.active = True
            self.tuningHarmonicMinorScaleButton.active = True
            self.tuningMelodicMinorScaleButton.active = False

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

        self.updated = True
        
        run_options = True
        while run_options:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_options = False
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_back.rect.collidepoint(event.pos):
                        run_options = False
                        self.configUpdated = False
                        return source
                    elif self.button_save.rect.collidepoint(event.pos):
                        run_options = False
                        self.saveConfig()
                        self.configUpdated = True
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
                        self.button_keys.draw(display)
                        self.button_tuning.draw(display)
                        self.button_back.draw(display)
                        self.button_save.draw(display)
                        self.updated = True
                    elif self.button_tuning.rect.collidepoint(event.pos) and self.button_tuning.active == True:
                        optionsPage = 'tuning'
                        text = self.tuningText
                        self.button_keys.active = True
                        self.button_tuning.active = False
                        self.button_other.active = True
                        self.drawBackground(display)
                        for txt in text:
                            txt.draw(display)
                        self.button_keys.draw(display)
                        self.button_tuning.draw(display)
                        self.button_back.draw(display)
                        self.button_save.draw(display)
                        for button in self.buttons_tuning:
                            button.draw(display)
                        self.bellOctaveShiftBox.draw(display)
                        self.bellSemitoneShiftBox.draw(display)
                        self.updated = True
                    elif self.button_other.rect.collidepoint(event.pos) and self.button_other.active == True:
                        optionsPage = 'other'
                        text = self.otherText
                        self.button_keys.active = True
                        self.button_tuning.active = True
                        self.button_other.active = False
                        self.drawBackground(display)
                        for txt in text:
                            txt.draw(display)
                        self.button_keys.draw(display)
                        self.button_tuning.draw(display)
                        self.button_back.draw(display)
                        self.button_save.draw(display)
                        self.updated = True

                    elif self.tuningServerButton.rect.collidepoint(event.pos) and self.tuningServerButton.active == True:
                        self.tuningServerButton.active = False
                        self.tuningClientButton.active = True
                        self.tuningServerButton.draw(display)
                        self.tuningClientButton.draw(display)
                        self.updated = True
                    elif self.tuningClientButton.rect.collidepoint(event.pos) and self.tuningClientButton.active == True:
                        self.tuningClientButton.active = False
                        self.tuningServerButton.active = True
                        self.tuningClientButton.draw(display)
                        self.tuningServerButton.draw(display)
                        self.updated = True

                    elif self.tuningMajorScaleButton.rect.collidepoint(event.pos) and self.tuningMajorScaleButton.active == True:
                        self.tuningMajorScaleButton.active = False
                        self.tuningNaturalMinorScaleButton.active = True
                        self.tuningHarmonicMinorScaleButton.active = True
                        self.tuningMelodicMinorScaleButton.active = True
                        for button in self.buttons_tuning:
                            button.draw(display)
                        self.updated = True
                    elif self.tuningNaturalMinorScaleButton.rect.collidepoint(event.pos) and self.tuningNaturalMinorScaleButton.active == True:
                        self.tuningMajorScaleButton.active = True
                        self.tuningNaturalMinorScaleButton.active = False
                        self.tuningHarmonicMinorScaleButton.active = True
                        self.tuningMelodicMinorScaleButton.active = True
                        for button in self.buttons_tuning:
                            button.draw(display)
                        self.updated = True
                    elif self.tuningHarmonicMinorScaleButton.rect.collidepoint(event.pos) and self.tuningHarmonicMinorScaleButton.active == True:
                        self.tuningMajorScaleButton.active = True
                        self.tuningNaturalMinorScaleButton.active = True
                        self.tuningHarmonicMinorScaleButton.active = False
                        self.tuningMelodicMinorScaleButton.active = True
                        for button in self.buttons_tuning:
                            button.draw(display)
                        self.updated = True
                    elif self.tuningMelodicMinorScaleButton.rect.collidepoint(event.pos) and self.tuningMelodicMinorScaleButton.active == True:
                        self.tuningMajorScaleButton.active = True
                        self.tuningNaturalMinorScaleButton.active = True
                        self.tuningHarmonicMinorScaleButton.active = True
                        self.tuningMelodicMinorScaleButton.active = False
                        for button in self.buttons_tuning:
                            button.draw(display)
                        self.updated = True

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
                        self.updated = True

                for button in self.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                        button.updated = True
                        button.draw(display)
                        self.updated = True
                    elif button.active == True and button.hovered == True:
                        button.hovered = False
                        button.updated = True
                        button.draw(display)
                        self.updated = True

                if optionsPage == 'tuning':
                    for button in self.buttons_tuning:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            button.hovered = True
                            button.updated = True
                            button.draw(display)
                            self.updated = True
                        elif button.active == True and button.hovered == True:
                            button.hovered = False
                            button.updated = True
                            button.draw(display)
                            self.updated = True

            if optionsPage == 'keys':
                for box in self.bellNumberInputBoxes:
                    if box.updated:
                        box.draw(display)
                        box.updated = False
                        self.updated = True
                for box in self.bellKeyInputBoxes:
                    if box.updated:
                        box.draw(display)
                        box.updated = False
                        self.updated = True

            if self.updated:
                display.flip()
                self.updated = False

            clock.tick(self.frameRate)

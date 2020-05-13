import pygame

from button import Button
from textBox import TextBox

class AboutScreen:

    def __init__(self, win, frameRate, version):
        self.win = win
        self.frameRate = frameRate
        self.version = version

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        self.aboutBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)

        self.button_back = Button("Back", (self.x + 20, self.height + self.y - 20))
        self.button_back.rect.y -= self.button_back.rect.h
        self.buttons = [self.button_back]

        self.aboutTitleText = TextBox('About:',
                                       (self.x+20, self.y+20), width=self.width-40, backgroundColour=(150, 150, 150), font='large')
        self.aboutText_1 = TextBox("ReBel version {}".format(self.version[1:]),
                                   (self.x+20, self.aboutTitleText.y+self.aboutTitleText.h+7), width=self.width-40, font='small')
        self.aboutText_2 = TextBox("ReBel is a client-server-based multiuser online ringing software. Developed by Samuel M. Senior and " + \
                                   "open-sourced using the BSD-3-Clause license.",
                                   (self.x+20, self.aboutText_1.y+self.aboutText_1.h+10), width=self.width-40, font='tiny')
        self.aboutText_3 = TextBox("Source code can be downloaded from 'https://github.com/samuelsenior/ReBel'.",
                                   (self.x+20, self.aboutText_2.y+self.aboutText_2.h+10), width=self.width-40, font='tiny')
        self.aboutText_4 = TextBox("The latest release can be downloaded from 'https://github.com/samuelsenior/ReBel/releases'.",
                                   (self.x+20, self.aboutText_3.y+self.aboutText_3.h+10), width=self.width-40, font='tiny')
        self.aboutText = [self.aboutTitleText, self.aboutText_1, self.aboutText_2, self.aboutText_3, self.aboutText_4]

    def drawBackground(self):
        pygame.draw.rect(self.win, (170, 170, 170), self.aboutBackground, 0)
        pygame.draw.rect(self.win, (100, 100, 100), self.aboutBackground, 2)

    def display(self, win, source):
        self.win = win

        self.width = int(self.win.get_width() * 0.8)
        self.height = int(self.win.get_height() * 0.8)

        self.backgroundFade = pygame.Surface((self.win.get_width(), self.win.get_height()), pygame.SRCALPHA)
        self.backgroundFade.fill((255, 255, 255, 156))

        self.aboutBackground = pygame.Rect(0 + (self.win.get_width() - self.width) / 2.0, 0 + (self.win.get_height() - self.height) / 2.0, self.width, self.height)


        self.x = (self.win.get_width() - self.width) / 2.0
        self.y = (self.win.get_height() - self.height) / 2.0

        for i, aboutText in enumerate(self.aboutText):
            aboutText.rect.x = self.x + 20
            if i == 0:
                startingY = aboutText.y
            else:
                startingY = self.aboutText[i-1].y + self.aboutText[i-1].h+10
            aboutText.generateFormattedText(startingY=startingY, width=self.width-40)
        self.button_back.rect.x = self.x + 20

        self.win.blit(self.backgroundFade, (0, 0))

        self.drawBackground()

        for button in self.buttons:
            if button.updated:
                button.hovered = False
                button.draw(self.win)

        for txt in self.aboutText:
            txt.draw(self.win)

        pygame.display.flip()
        
        clock = pygame.time.Clock()
        
        run_about = True
        while run_about:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run_about = False
                    return 'quit'

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_back.rect.collidepoint(event.pos):
                        run_about = False
                        return source

                for button in self.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        button.hovered = True
                        button.updated = True
                    elif button.active == True:
                        button.hovered = False
                        button.updated = True

            for button in self.buttons:
                if button.updated:
                    button.draw(self.win)

            pygame.display.flip()
            clock.tick(self.frameRate)

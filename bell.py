import pygame

class Bell:
    def __init__(self, bellNumber, x, y, key=None):

        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('dodgerblue2')

        self.bellNumber = bellNumber

        self.x = x
        self.y = y
        self.width = 50
        self.height = 50

        self.key = key

        self.colour = self.COLOR_INACTIVE
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.active = False

    def setKey(self, key):
        self.key = key

    def draw(self, win):
        pygame.draw.rect(win, self.colour, self.rect, 0)

    def handle_event(self, event, send):
        if event == self.key:
            # Toggle the active variable on
            send(str(self.bellNumber))

    def bellRung(self):
        # Change the current colour of the bell
        self.active = not self.active
        self.colour = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        
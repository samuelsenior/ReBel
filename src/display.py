import pygame

import threading, queue
import time

class Draw:
    def __init__(self, win, displayingThread=False):
        self.win = win

        if displayingThread:
            self.rect = self.rect_displayThread
        else:
            self.rect = self.rect_mainThread

    def rect_displayThread(self, *args):
        pygame.draw.rect(self.win, *args)

    def rect_mainThread(self, *args):
        self.displayThreadQueue.put(('draw_rect', args))

class Display:

    def __init__(self, width, height, caption=None, iconFile=None):

        self.frameRate = 100

        self.width = width
        self.height = height
        self.caption = caption
        self.iconFile = iconFile

        self.win = pygame.display.set_mode((self.width, self.height))
        if self.caption:
            pygame.display.set_caption("ReBel")
        if self.iconFile:
            self.icon = pygame.image.load(self.iconFile)
            pygame.display.set_icon(self.icon)

        self.displayOnDedicatedThread = False
        if self.displayOnDedicatedThread:
            self.draw = Draw(self.win)
            self.blit = self.blitLinker
            self.flip = self.flipLinker
            self.running = True
            self.displayThreadQueue = queue.Queue()
            self.displayThread = threading.Thread(target=self.display, args=(self.win, ), daemon=True)
            self.displayThread.start()
            self.displayFunctions = {
                                     'flip':self.flipFunction,
                                     'blit':self.blitFunction,
                                     'draw_rect':self.draw.rect,
            }
        else:
            self.draw = Draw(self.win, displayingThread=True)
            self.blit = self.blitFunction
            self.flip = self.flipFunction

    def set_mode(self, *args):
        self.win = pygame.display.set_mode(*args)
        return self.win

    def updateScreenSize(self, width, height):
        self.win = pygame.display.set_mode((width, height))

    def blitLinker(self, *args):
        self.displayThreadQueue.put(('blit', args))

    def flipLinker(self):
        self.displayThreadQueue.put(('flip', None))

    def blitFunction(self, *args):
        self.win.blit(*args)

    def flipFunction(self, *args):
        pygame.display.flip()

    def display(self, win):
        self.win = win
        self.draw = Draw(self.win, displayingThread=True)
        clock = pygame.time.Clock()
        while self.running:
            try:
                displayObject = self.displayThreadQueue.get_nowait()
            except:
                pass
            else:
                self.displayFunctions[displayObject[0]](displayObject[1])
            clock.tick(self.frameRate)

    def subprocess(self):
        pass

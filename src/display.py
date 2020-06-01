import pygame

import threading, queue
import time

class Draw:
    def __init__(self, win, displayThread=False):
        self.win = win

        if displayThread:
            self.rect = self.rect_displayThread
        else:
            self.rect = self.rect_mainThread

    def rect_displayThread(self, *args):
        pygame.draw.rect(self.win, *args)

    def rect_mainThread(self, *args):
        self.displayThreadQueue.put(('draw_rect', args))

class Display:

    def __init__(self, width, height, caption=None, iconFile=None):

        self.frameRate = 500

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

        self.draw = Draw(self.win)

        self.running = True
        self.displayThreadQueue = queue.Queue()
        self.displayThread = threading.Thread(target=self.display, args=(self.win, ), daemon=True)
        self.displayThread.start()
        self.displayFunctions = {
                                 'flip':self._flip,
                                 'blit':self._blit,
                                 'draw_rect':self.draw.rect,
        }

    def set_mode(self, *args):
        self.win = pygame.display.set_mode(*args)
        return self.win

    def updateScreenSize(self, width, height):
        self.win = pygame.display.set_mode((width, height))

    def blit(self, *args):
        self.displayThreadQueue.put(('blit', args))

    def flip(self):
        self.displayThreadQueue.put(('flip', None))

    def _blit(self, args):
        self.win.blit(*args)

    def _flip(self, args):
        pygame.display.flip()

    def display(self, win):
        self.win = win
        self.draw = Draw(self.win, displayThread=True)
        while self.running:
            start = time.time()
            try:
                displayObject = self.displayThreadQueue.get_nowait()
            except:
                pass
            else:
                self.displayFunctions[displayObject[0]](displayObject[1])
            time.sleep(max(1./self.frameRate - (time.time() - start), 0))

    def subprocess(self):
        pass

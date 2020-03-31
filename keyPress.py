import pygame

class KeyPress:
    def __init__(self):
        pass

    def keyPress(self, key):
        if key.lower() == 'f':
            return pygame.K_f
        elif key.lower() == 'j':
            return pygame.K_j
        elif key.lower() == 'r':
            return pygame.K_r
        elif key.lower() == 'u':
            return pygame.K_u
        # Bells not controlled by this user
        elif key == "-1":
           	pass

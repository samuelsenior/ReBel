import pygame

class KeyPress:
    def __init__(self):
        pass

    def keyPress(self, key):
        if key.lower() == 'q':
            return pygame.K_q
        elif key.lower() == 'w':
            return pygame.K_w
        elif key.lower() == 'e':
            return pygame.K_e
        elif key.lower() == 'r':
            return pygame.K_r
        elif key.lower() == 't':
            return pygame.K_t
        elif key.lower() == 'y':
            return pygame.K_y
        elif key.lower() == 'u':
            return pygame.K_u
        elif key.lower() == 'i':
            return pygame.K_i
        elif key.lower() == 'o':
            return pygame.K_o
        elif key.lower() == 'p':
            return pygame.K_p

        elif key.lower() == 'a':
            return pygame.K_a
        elif key.lower() == 's':
            return pygame.K_s
        elif key.lower() == 'd':
            return pygame.K_d
        elif key.lower() == 'f':
            return pygame.K_f
        elif key.lower() == 'g':
            return pygame.K_g
        elif key.lower() == 'h':
            return pygame.K_h
        elif key.lower() == 'j':
            return pygame.K_j
        elif key.lower() == 'k':
            return pygame.K_k
        elif key.lower() == 'l':
            return pygame.K_l

        elif key.lower() == 'z':
            return pygame.K_z
        elif key.lower() == 'x':
            return pygame.K_x
        elif key.lower() == 'c':
            return pygame.K_c
        elif key.lower() == 'v':
            return pygame.K_v
        elif key.lower() == 'b':
            return pygame.K_b
        elif key.lower() == 'n':
            return pygame.K_n
        elif key.lower() == 'm':
            return pygame.K_m

        elif key == "-1":
            pass

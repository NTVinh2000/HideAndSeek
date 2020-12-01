import pygame
from constants import *


class Hider:

    icon = pygame.transform.scale(pygame.image.load('characterIcon/sheep.png'), (SQUARE_SIZE - 1, SQUARE_SIZE - 1))

    def __init__(self):
        self.Hx = ROW - 1
        self.Hy = COL - 1

    def update(self, newCor):
        self.Hx = newCor[0]
        self.Hy = newCor[1]

    def drawHider(self, win):
        win.blit(Hider.icon, (self.Hy * SQUARE_SIZE, self.Hx * SQUARE_SIZE))

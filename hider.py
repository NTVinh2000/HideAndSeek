import pygame
from constants import *
import random

class Hider:

    icon = pygame.transform.scale(pygame.image.load('characterIcon/sheep.png'), (SQUARE_SIZE - 1, SQUARE_SIZE - 1))

    def __init__(self):
        self.Hx = ROW - 1
        self.Hy = COL - 1
        self.CoveredList = set()
    def update(self, newCor):
        self.Hx = newCor[0]
        self.Hy = newCor[1]

    def drawHider(self, win):
        win.blit(Hider.icon, (self.Hy * SQUARE_SIZE, self.Hx * SQUARE_SIZE))

    def announce(self,map):

        for i in range(self.Hx-3,self.Hx+3):
            for j in range(self.Hy-3,self.Hy+3):
                if  i > 1 and i < len(map) -1 and j > 1 and j < len(map[0]) -1:
                    if map[i][j] == 0:
                        self.CoveredList.add((i,j))


        for i in range(self.Hx-3,self.Hx+3):
            for j in range(self.Hy-3,self.Hy+3):
                if i > 1 and i < len(map) - 1 and j > 1 and j < len(map[0]) - 1:
                    if map[i][j] == 3:


                        print("random at:",random.sample(self.CoveredList,1))
                        return




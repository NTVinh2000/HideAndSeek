import pygame
from constants import *

class Board:

    wall = pygame.transform.scale(pygame.image.load('characterIcon/wall.png'), (SQUARE_SIZE, SQUARE_SIZE))

    def __init__(self):
        self.board = []

    def draw_background(self, win):
        win.fill(BLACK)
        for row in range(ROW):
            for col in range(COL):
                pygame.draw.rect(win, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))

    def draw_board(self, win, map):
        self.draw_background(win)

        for i in range(ROW):
            for j in range(COL):
                if map[i][j] == 1:
                    win.blit(Board.wall, (j * SQUARE_SIZE, i * SQUARE_SIZE))

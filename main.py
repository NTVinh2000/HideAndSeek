import pygame
from constants import *
mapInfo = load_map('map/map3.txt')
from constants import *
from board import Board
from seeker import Seeker
from hider import Hider


def pause():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False

def main():
    #init board
    board = Board()

    #init seeker
    seeker = Seeker()
    seeker.build_visitMap(mapInfo[0])
    seeker.update(mapInfo[1][0], mapInfo[0])

    #init seeker move
    seekerNewMove = [seeker.Sx, seeker.Sy]
    seekerOldMove = []
    seekerOldMove.append(seekerNewMove)

    #init hider
    hiderList = []
    for i in range(len(mapInfo[2])):
        hiderList.append(Hider())
        hiderList[i].update(mapInfo[2][i])

    #init game
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Map")

    running = True
    clock = pygame.time.Clock()

    #init draw
    board.draw_board(WIN, mapInfo[0])
    seeker.drawVison(WIN, mapInfo[0])
    seeker.drawSeeker(WIN)

    for i in range(len(hiderList)):
        hiderList[i].drawHider(WIN)

    pygame.display.update()
    pygame.time.wait(300)

    #start game loop
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()

        #move
        #seekerOldMove.append(seekerNewMove)
        #if len(seekerOldMove) > 4:
        #    seekerOldMove.pop(0)
        seekerNewMove = seeker.randomMove(mapInfo[0])
        if (seekerNewMove is None):
            print('game over')
            return
        seeker.update(seekerNewMove, mapInfo[0])

        #draw
        board.draw_board(WIN, mapInfo[0])
        seeker.drawVison(WIN, mapInfo[0])
        seeker.drawSeeker(WIN)

        for i in range(len(hiderList)):
            hiderList[i].drawHider(WIN)

        pygame.display.update()
        pygame.time.wait(150)

    pygame.quit()

main()
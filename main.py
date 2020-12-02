import pygame
from constants import *
mapInfo = load_map('map/map1.txt')
from constants import *
from board import Board
from seeker import Seeker
from hider import Hider

#for i in range(len(mapInfo)):
#    print(mapInfo[2][i])

#print(mapInfo[1][0])

#hiderList = []
#for i in range(len(mapInfo[2])):
#    print(i)
#print(hiderList[0].Hx, hiderList[0].Hy)

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
    board = Board()
    seeker = Seeker()
    seeker.update(mapInfo[1][0], mapInfo[0])
    hiderList = []
    for i in range(len(mapInfo[2])):
        hiderList.append(Hider())
        hiderList[i].update(mapInfo[2][i])

    'seeker.visionScope(mapInfo[0])'

    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Map")

    running = True
    clock = pygame.time.Clock()
    seekerNewMove = [seeker.Sx, seeker.Sy]
    seekerOldMove = []
    seekerOldMove.append(seekerNewMove)

    board.draw_board(WIN, mapInfo[0])
    seeker.visionScopeUpdate(mapInfo[0])
    seeker.visibleUpdate()
    seeker.drawVison(WIN, mapInfo[0])
    pygame.time.wait(300)
    seeker.drawSeeker(WIN)

    for i in range(len(hiderList)):
        hiderList[i].drawHider(WIN)

    pygame.display.update()


    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()

        #move
        seekerOldMove.append(seekerNewMove)
        #if len(seekerOldMove) > 4:
        #    seekerOldMove.pop(0)
        #print(seekerOldMove)
        seekerNewMove = seeker.randomMove(seekerOldMove, mapInfo[0])
        seeker.update(seekerNewMove, mapInfo[0])
        #seeker.randomMove([0, 0])

        #draw
        board.draw_board(WIN, mapInfo[0])
        seeker.drawVison(WIN, mapInfo[0])
        pygame.time.wait(1000)
        seeker.drawSeeker(WIN)

        for i in range(len(hiderList)):
            hiderList[i].drawHider(WIN)

        pygame.display.update()

    pygame.quit()

main()
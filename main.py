import pygame
from constants import *
mapInfo = load_map('map/map4.txt')
from constants import *
from board import Board
from seeker import Seeker
from hider import Hider
import numpy as np


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
    level = 3
    #init board
    board = Board()
    catchingHider = False
    pathToCurrentHider = []
    hiderPos = []
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
        hiderList[i].update(mapInfo[2][i],mapInfo[0])
    numberOfHiders = len(hiderList)
    list_hider_goals = []
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
    pygame.time.wait(20)


    #start game loop
    turn_count = 0
    hider_time = 5
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
        turn_count = turn_count+1

        if level >=3:
            for i in range(len(hiderList)):
                new_move =hiderList[i].get_goal(mapInfo[0],1000)
                hiderList[i].update(new_move,mapInfo[0])

        if turn_count >hider_time:
            if len(seeker.hiderPositionList) == 0  :
                seekerNewMove = seeker.randomMove(mapInfo[0])

            elif len(seeker.hiderPositionList)>0 :
                hiderPos = seeker.hiderPositionList[0]
                if catchingHider == False:
                    pathToCurrentHider = seeker.FromStartToEnd(list([seeker.Sx,seeker.Sy]), hiderPos,mapInfo[0])
                    print("hider position:",hiderPos)
                    catchingHider = True
                seekerNewMove = pathToCurrentHider.pop(0)
                if seekerNewMove[0] == hiderPos[0] and seekerNewMove[1] == hiderPos[1]:
                    numberOfHiders = numberOfHiders -1
                    catchingHider = False
                    mapInfo[0][hiderPos[0]][hiderPos[1]] = 0
                    seeker.visionScopeUpdate(mapInfo[0])
                    seeker.visibleUpdate()
                    seeker.hiderPositionList.pop(0)
                    print('need to pop: ',seekerNewMove)
                    for i in range(len(hiderList)):
                        print(hiderList[i].Sx,hiderList[i].Sy)
                    
                    for k in range(0,len(hiderList)):
                        if hiderList[k].Sx ==  hiderPos[0] and hiderList[k].Sy == hiderPos[1]:
                            hiderList.pop(k)
                            break

                    if len(hiderList) ==0:
                        print("Find all hiders, game over")
                        return

            if turn_count%3 == 0:
                for i in hiderList:
                    i.announce(mapInfo[0])
            #seekerNewMove = seeker.randomMove(mapInfo[0])
            if (seekerNewMove is None):
                print('game over')
                return

            seeker.update(seekerNewMove, mapInfo[0])
            seeker.findHider()


                


        #draw
        #draw board
        board.draw_board(WIN, mapInfo[0])
        #draw vision
        seeker.drawVison(WIN, mapInfo[0])
        for i in range(len(hiderList)):
            hiderList[i].drawVison(WIN, mapInfo[0], seeker)

        #draw agents
        seeker.drawSeeker(WIN)
        for i in range(len(hiderList)):
            hiderList[i].drawHider(WIN)

        #for i in seeker.vision:
        #    print(i)
        #print("X of seeker:", seeker.Sx)
        #print("Y of seeker:", seeker.Sy, "\n")
        #print hider location
        #print(" hider position list that seeker found", seeker.hiderPositionList)



        pygame.display.update()
        pygame.time.wait(100)

    pygame.quit()

main()
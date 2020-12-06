import pygame
from constants import *
import random
import numpy as np

class Hider:

    icon = pygame.transform.scale(pygame.image.load('characterIcon/sheep.png'), (SQUARE_SIZE - 1, SQUARE_SIZE - 1))

    def __init__(self):
        self.Sx = ROW - 1
        self.Sy = COL - 1
        self.CoveredList = set()
        self.currentTime = 0

    def update(self, newCor, map):
        if self.Sx != -1:
            map[self.Sx][self.Sy] = 0
        self.Sx = newCor[0]
        self.Sy = newCor[1]
        map[self.Sx][self.Sy] = 2
        #self.visionScopeUpdate(map)
        #self.visibleUpdate()
        self.currentTime += 1
        #self.mark_visitMap()

    def drawHider(self, win):
        win.blit(Hider.icon, (self.Sy * SQUARE_SIZE, self.Sx * SQUARE_SIZE))

    def get_state(self, map, pos):
        Ix = [-1, 1, 0, 0]
        Iy = [0, 0, -1, 1]
        cnt = 0
        for i in range(4):
            posX = pos[0]+Ix[i]
            posY = pos[1]+Iy[i]
            if (map[posX][posY] == 1):
                cnt +=1
            #if (map[posX][posY] == 3):
            #    cnt -= 1000
        return cnt

    def get_goal(self, map, longest):
        Ix = [-1, -1, -1, 0, 1, 1,  1,  0]
        Iy = [-1,  0,  1, 1, 1, 0, -1, -1]
        queue = np.array([(self.Sx,self.Sy,0)])
        prev = np.zeros((ROW, COL, 2))
        prev[self.Sx][self.Sy][:] = [self.Sx, self.Sy]
        #print(dd.shape)
        maxX = self.Sx
        maxY = self.Sy
        maxVal = self.get_state(map, [maxX, maxY])
        while queue.shape[0] != 0:
            queue = queue.reshape((-1,3))
            cur = [0,0]
            dis = 0
            (cur[0],cur[1],dis) = queue[0][:]
            #print(queue)
            if (dis == longest):
                break
            queue = np.delete(queue,0,0)
            for i in range(8):
                newPosX = cur[0] + Ix[i]
                newPosY = cur[1] + Iy[i]
                if (newPosX < 1 or newPosX > ROW-2 or newPosY < 1 or newPosY > COL-2):
                    continue
                if (map[newPosX][newPosY] == 1 or map[newPosX][newPosY] == 3 or map[newPosX][newPosY] == 2):
                    continue
                val = self.get_state(map,[newPosX,newPosY])
                if val > maxVal:
                    maxVal = val
                    maxX = newPosX
                    maxY = newPosY
                if prev[newPosX][newPosY][0] == 0 and prev[newPosX][newPosY][1] == 0:
                    prev[newPosX][newPosY][:] = [cur[0], cur[1]]
                    queue = np.append(queue, (newPosX,newPosY,dis+1))
        maxX = int(maxX)
        maxY = int(maxY)
        resX = maxX
        resY = maxY
        while(maxX != self.Sx or maxY != self.Sy):
            resX = maxX
            resY = maxY
            maxX = prev[int(resX)][int(resY)][0]
            maxY = prev[int(resX)][int(resY)][1]
        return (int(resX),int(resY))

        

    def announce(self, map):

        for i in range(self.Sx-3,self.Sx+3):
            for j in range(self.Sy-3,self.Sy+3):
                if  i > 1 and i < len(map) -1 and j > 1 and j < len(map[0]) -1:
                    if map[i][j] == 0:
                        self.CoveredList.add((i,j))


        for i in range(self.Sx-3,self.Sx+3):
            for j in range(self.Sy-3,self.Sy+3):
                if i > 1 and i < len(map) - 1 and j > 1 and j < len(map[0]) - 1:
                    if map[i][j] == 3:


                        print("random at:",random.sample(self.CoveredList,1))
                        return




import pygame
from constants import *
import random
import numpy as np

class Hider:

    icon = pygame.transform.scale(pygame.image.load('characterIcon/sheep.png'), (SQUARE_SIZE - 1, SQUARE_SIZE - 1))
    annouceIcon = pygame.transform.scale(pygame.image.load('characterIcon/footprint.png'), (SQUARE_SIZE - 1, SQUARE_SIZE - 1))

    def __init__(self):
        self.Sx = - 1
        self.Sy = - 1
        self.vision = []
        self.top, self.left, self.bottom, self.right = 0, 0, 0, 0
        self.radius = 2
        self.CoveredList = set()
        self.currentTime = 0

    def update(self, newCor, map):
        if self.Sx != -1:
            map[self.Sx][self.Sy] = 0
        self.Sx = newCor[0]
        self.Sy = newCor[1]
        map[self.Sx][self.Sy] = 2
        self.visionScopeUpdate(map)
        self.visibleUpdate()
        self.currentTime += 1
        #self.mark_visitMap()


    def drawHider(self, win):
        win.blit(Hider.icon, (self.Sy * SQUARE_SIZE, self.Sx * SQUARE_SIZE))

    def drawAnnouce(self, win, row, col):
        win.blit(Hider.annouceIcon, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def run(self, map):
        Ix = [-1, -1, -1, 0, 1, 1,  1,  0]
        Iy = [-1,  0,  1, 1, 1, 0, -1, -1]
        minX = self.Sx
        minY = self.Sy
        minVal = 100000
        for i in range(8):
            newPosX = self.Sx+Ix[i]
            newPosY = self.Sy+Iy[i]
            if (newPosX < 1 or newPosX > ROW - 2 or newPosY < 1 or newPosY > COL - 2):
                continue
            cnt = 0
            if map[newPosX][newPosY] > 0:
                continue
            cnt += self.get_state(map, [newPosX,newPosY])
            Ixx = [-1, 1, 0, 0]
            Iyy = [0, 0, -1, 1]
            for j in range(4):
                if map[newPosX+Ixx[j]][newPosY+Iyy[j]]==3:
                    cnt +=100
            if (cnt<minVal):
                minVal = cnt
                minX = newPosX
                minY = newPosY
        return (minX,minY)


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


    def valueInVision(self, row, col):
        return self.vision[row - self.top][col - self.left]

    def isValidInVision(self, row, col):
        if 0 <= row < len(self.vision) and 0 <= col < len(self.vision[0]):
            return True
        return False

    # this function returns value in Vision: VISIBLE(0) or others
    def valueInVision(self, row, col):
        return self.vision[row - self.top][col - self.left]

    # this function return position of seeker in its vision
    def getPositionInVision(self):
        return [self.Sx - self.top, self.Sy - self.left]

    # draw vision
    def drawVison(self, win, map, seeker):
        vi = 0
        for i in range(self.top, self.bottom + 1):
            vj = 0
            for j in range(self.left, self.right + 1):
                if self.vision[vi][vj] == 0 or self.vision[vi][vj] == 2 or self.vision[vi][vj] == 3:
                    if (i in range(seeker.top, seeker.bottom + 1)) and (j in range(seeker.left, seeker.right + 1)) \
                            and (seeker.vision[i - seeker.top][j - seeker.left] == VISIBLE \
                            or seeker.vision[i - seeker.top][j - seeker.left] == SEEKER_ID \
                            or seeker.vision[i - seeker.top][j - seeker.left] ==HIDER_ID):
                        pygame.draw.rect(win, GREEN,
                                         (j * SQUARE_SIZE, i * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))
                    else:
                        pygame.draw.rect(win, AQUA,
                                         (j * SQUARE_SIZE, i * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))
                vj += 1
            vi += 1

    def visionScopeUpdate(self, map):
        if self.Sx - self.radius >= 0:
            self.top = self.Sx - self.radius

        if self.Sx + self.radius <= ROW - 1:
            self.bottom = self.Sx + self.radius
        else:
            self.bottom = ROW - 1

        if self.Sy - self.radius >= 0:
            self.left = self.Sy - self.radius

        if self.Sy + self.radius <= COL - 1:
            self.right = self.Sy + self.radius
        else:
            self.right = COL - 1

        self.vision = []

        for i in range(self.top, self.bottom + 1):
            temp = list(map[i])
            self.vision.append(temp[self.left: self.right + 1])

    # check which tiles are VISIBLE(0) and mark COVERED(-1) tiles
    def visibleUpdate(self):
        # (i, k): i row, k column
        center = self.getPositionInVision()
        for i in range(0, len(self.vision) + 1):
            for k in range(0, len(self.vision[0]) + 1):

                if not (self.isValidInVision(i, k)): continue
                if i == center[0] and k == center[1]: continue
                # wall
                if self.vision[i][k] == WALL_ID or self.vision[i][k] == HIDER_ID:

                    # vertical
                    if k == center[1]:
                        if i < center[0]:
                            if not (self.isValidInVision(i - 1, k)): continue
                            self.vision[i - 1][k] = COVERED
                            coverRate = 1
                            for e in range(2, i + 1):
                                if abs(center[0] - i) == 0 or e % (abs(center[0] - i)) == 0:
                                    coverRate += 1
                                if self.isValidInVision(i - e, k):
                                    self.vision[i - e][k] = COVERED
                                    for temp in range(1, coverRate):
                                        if self.isValidInVision(i - e, k + temp):
                                            self.vision[i - e][k + temp] = COVERED
                                        if self.isValidInVision(i - e, k - temp):
                                            self.vision[i - e][k - temp] = COVERED

                            if i + 1 == center[0]:
                                if self.isValidInVision(center[0] - 1, center[1] + 1):
                                    if self.vision[center[0] - 1][center[1] + 1] == WALL_ID or \
                                            self.vision[center[0] - 1][center[1] + 1] == HIDER_ID:
                                        if self.isValidInVision(center[0] - 2, center[1] + 1):
                                            self.vision[center[0] - 2][center[1] + 1] = COVERED
                                if self.isValidInVision(center[0] - 1, center[1] - 1):
                                    if self.vision[center[0] - 1][center[1] - 1] == WALL_ID or \
                                            self.vision[center[0] - 1][center[1] - 1] == HIDER_ID:
                                        if self.isValidInVision(center[0] - 2, center[1] - 1):
                                            self.vision[center[0] - 2][center[1] - 1] = COVERED

                        else:
                            if not (self.isValidInVision(i + 1, k)): continue
                            self.vision[i + 1][k] = COVERED
                            coverRate = 1
                            for e in range(2, len(self.vision) - i):
                                if abs(center[0] - i) == 0 or e % (abs(center[0] - i)) == 0:
                                    coverRate += 1
                                if self.isValidInVision(i + e, k):
                                    self.vision[i + e][k] = COVERED
                                    for temp in range(1, coverRate):
                                        if self.isValidInVision(i + e, k + temp):
                                            self.vision[i + e][k + temp] = COVERED
                                        if self.isValidInVision(i + e, k - temp):
                                            self.vision[i + e][k - temp] = COVERED

                            if i - 1 == center[0]:
                                if self.isValidInVision(center[0] + 1, center[1] + 1):
                                    if self.vision[center[0] + 1][center[1] + 1] == WALL_ID or \
                                            self.vision[center[0] + 1][center[1] + 1] == HIDER_ID:
                                        if self.isValidInVision(center[0] + 2, center[1] + 1):
                                            self.vision[center[0] + 2][center[1] + 1] = COVERED
                                if self.isValidInVision(center[0] + 1, center[1] - 1):
                                    if self.vision[center[0] + 1][center[1] - 1] == WALL_ID or \
                                            self.vision[center[0] + 1][center[1] - 1] == HIDER_ID:
                                        if self.isValidInVision(center[0] + 2, center[1] - 1):
                                            self.vision[center[0] + 2][center[1] - 1] = COVERED
                        # print("I was here vertical")

                    # horizontal
                    elif i == center[0]:
                        if k < center[1]:
                            if not (self.isValidInVision(i, k - 1)): continue
                            self.vision[i][k - 1] = COVERED
                            coverRate = 1
                            for e in range(2, k + 1):
                                if abs(center[1] - k) == 0 or e % (abs(center[1] - k)) == 0:
                                    coverRate += 1
                                if self.isValidInVision(i, k - e):
                                    self.vision[i][k - e] = COVERED
                                    for temp in range(1, coverRate):
                                        if self.isValidInVision(i + temp, k - e):
                                            self.vision[i + temp][k - e] = COVERED
                                        if self.isValidInVision(i - temp, k - e):
                                            self.vision[i - temp][k - e] = COVERED

                            if k + 1 == center[1]:
                                if self.isValidInVision(center[0] - 1, center[1] - 1):
                                    if self.vision[center[0] - 1][center[1] - 1] == WALL_ID or \
                                            self.vision[center[0] - 1][center[1] - 1] == HIDER_ID:
                                        if self.isValidInVision(center[0] - 1, center[1] - 2):
                                            self.vision[center[0] - 1][center[1] - 2] = COVERED
                                if self.isValidInVision(center[0] + 1, center[1] - 1):
                                    if self.vision[center[0] + 1][center[1] - 1] == WALL_ID or \
                                            self.vision[center[0] + 1][center[1] - 1] == HIDER_ID:
                                        if self.isValidInVision(center[0] + 1, center[1] - 2):
                                            self.vision[center[0] + 1][center[1] - 2] = COVERED
                        else:
                            if not (self.isValidInVision(i, k + 1)): continue
                            self.vision[i][k + 1] = COVERED
                            coverRate = 1
                            for e in range(2, len(self.vision[0]) - k):
                                if abs(center[1] - k) == 0 or e % (abs(center[1] - k)) == 0:
                                    coverRate += 1
                                if self.isValidInVision(i, k + e):
                                    self.vision[i][k + e] = COVERED
                                    for temp in range(1, coverRate):
                                        if self.isValidInVision(i + temp, k + e):
                                            self.vision[i + temp][k + e] = COVERED
                                        if self.isValidInVision(i - temp, k + e):
                                            self.vision[i - temp][k + e] = COVERED

                            if k - 1 == center[1]:
                                if self.isValidInVision(center[0] - 1, center[1] + 1):
                                    if self.vision[center[0] - 1][center[1] + 1] == WALL_ID or \
                                            self.vision[center[0] - 1][center[1] + 1] == HIDER_ID:
                                        if self.isValidInVision(center[0] - 1, center[1] + 2):
                                            self.vision[center[0] - 1][center[1] + 2] = COVERED
                                if self.isValidInVision(center[0] + 1, center[1] + 1):
                                    if self.vision[center[0] + 1][center[1] + 1] == WALL_ID or \
                                            self.vision[center[0] + 1][center[1] + 1] == HIDER_ID:
                                        if self.isValidInVision(center[0] + 1, center[1] + 2):
                                            self.vision[center[0] + 1][center[1] + 2] = COVERED
                        # print("I was here horizontal")

                    # diagonal quarter-2-4
                    elif i - k == center[0] - center[1]:
                        if i < center[0]:
                            if not (self.isValidInVision(i - 1, k - 1)): continue
                            naV = 2
                            subtop = 1
                            subleft = 1

                            while subtop > 0 or subleft > 0:
                                for temp in range(1, naV + 1):
                                    if self.isValidInVision(i - temp, 0):
                                        subtop = i - temp
                                    if self.isValidInVision(0, k - temp):
                                        subleft = k - temp

                                for eR in range(subtop, i - (int(naV / 2) - 1)):
                                    for eC in range(subleft, k - (int(naV / 2) - 1)):
                                        self.vision[eR][eC] = COVERED
                                naV += 2
                            '''
                            for eR in range(0, i):
                                for eC in range(0, k):
                                    self.vision[eR][eC] = COVERED
                            '''
                        else:
                            if not (self.isValidInVision(i + 1, k + 1)): continue
                            naV = 2
                            subbottom = 0
                            subright = 0

                            while subbottom < len(self.vision) - 1 or subright < len(self.vision[0]) - 1:
                                for temp in range(1, naV + 1):
                                    if self.isValidInVision(i + temp, 0):
                                        subbottom = i + temp
                                    if self.isValidInVision(0, k + temp):
                                        subright = k + temp

                                for eR in range(i + 1 + (int(naV / 2) - 1), subbottom + 1):
                                    for eC in range(k + 1 + int(naV / 2) - 1, subright + 1):
                                        self.vision[eR][eC] = COVERED
                                naV += 2
                            '''
                            for eR in range(i + 1, len(self.vision)):
                                for eC in range(k + 1, len(self.vision[0])):
                                    self.vision[eR][eC] = COVERED
                            '''
                        # print("I was here diagonal 2 4")

                    # diagonal quarter-1-3
                    elif i + k == center[0] + center[1]:
                        if i < center[0]:
                            if not (self.isValidInVision(i - 1, k + 1)): continue
                            naV = 2
                            subtop = 0
                            subright = 0

                            while subtop > 0 or subright < len(self.vision[0]) - 1:
                                for temp in range(1, naV + 1):
                                    if self.isValidInVision(i - temp, 0):
                                        subtop = i - temp
                                    if self.isValidInVision(0, k + temp):
                                        subright = k + temp

                                for eR in range(subtop, i - (int(naV / 2) - 1)):
                                    for eC in range(k + 1 + int(naV / 2) - 1, subright + 1):
                                        self.vision[eR][eC] = COVERED
                                naV += 2
                            '''
                            for eR in range(0, i):
                                for eC in range(k + 1, len(self.vision[0])):
                                    self.vision[eR][eC] = COVERED
                            '''
                        else:
                            if not (self.isValidInVision(i + 1, k - 1)): continue
                            naV = 2
                            subbottom = 0
                            subleft = 0

                            while subbottom < len(self.vision) - 1 or subleft > 0:
                                for temp in range(1, naV + 1):
                                    if self.isValidInVision(i + temp, 0):
                                        subbottom = i + temp
                                    if self.isValidInVision(0, k - temp):
                                        subleft = k - temp

                                for eR in range(i + 1 + (int(naV / 2) - 1), subbottom + 1):
                                    for eC in range(subleft, k - (int(naV / 2) - 1)):
                                        self.vision[eR][eC] = COVERED
                                naV += 2
                            '''
                            for eR in range(i + 1, len(self.vision)):
                                for eC in range(0, k):
                                    self.vision[eR][eC] = COVERED
                            '''
                        # print("I was here diagonal 1 3")

                    # other
                    else:
                        if i < center[0]:
                            # quarter 1
                            if k > center[1]:
                                if i + k < center[0] + center[1]:
                                    if not (self.isValidInVision(i - 1, k)): continue
                                    self.vision[i - 1][k] = COVERED
                                    exV = 1
                                    coverRate = 1
                                    conflict = 0
                                    for e in range(1, i + 1):
                                        for temp in range(coverRate):
                                            if self.isValidInVision(i - e, k + temp + exV):
                                                self.vision[i - e][k + temp + exV] = COVERED
                                        if (k - 1 != center[1] or self.vision[i][k - 1] != 1) and (
                                                (abs(i - center[0]) > 1 and abs(k - center[1]) > 1) or (
                                                abs(i - center[0]) <= 2 and abs(k - center[1]) == 1) or (
                                                        abs(i - center[0]) == 1 and abs(k - center[1]) <= 2)):
                                            if e % 5 == 0:
                                                exV += 1
                                                coverRate -= 1
                                        else:
                                            exV = 0
                                            if conflict < 1:
                                                coverRate += 1
                                                conflict += 1
                                        coverRate += 1
                                else:
                                    if not (self.isValidInVision(i, k + 1)): continue
                                    self.vision[i][k + 1] = COVERED
                                    exV = 1
                                    coverRate = 1
                                    conflict = 0
                                    for e in range(1, len(self.vision[0]) - k):
                                        for temp in range(coverRate):
                                            if self.isValidInVision(i - temp - exV, k + e):
                                                self.vision[i - temp - exV][k + e] = COVERED

                                        if (i + 1 != center[0] or self.vision[i + 1][k] != 1) and (
                                                (abs(i - center[0]) > 1 and abs(k - center[1]) > 1) or (
                                                abs(i - center[0]) <= 2 and abs(k - center[1]) == 1) or (
                                                        abs(i - center[0]) == 1 and abs(k - center[1]) <= 2)):
                                            if e % 5 == 0:
                                                exV += 1
                                                coverRate -= 1
                                        else:
                                            exV = 0
                                            if conflict < 1:
                                                coverRate += 1
                                                conflict += 1
                                        coverRate += 1
                                # print("I was here quarter 1")
                            # quater 2
                            else:
                                if k - i > center[1] - center[0]:
                                    if not (self.isValidInVision(i - 1, k)): continue
                                    self.vision[i - 1][k] = COVERED
                                    exV = 1
                                    coverRate = 1
                                    conflict = 0
                                    for e in range(1, i + 1):
                                        for temp in range(coverRate):
                                            if self.isValidInVision(i - e, k - temp - exV):
                                                self.vision[i - e][k - temp - exV] = COVERED
                                        if (k + 1 != center[1] or self.vision[i][k + 1] != 1) and (
                                                (abs(i - center[0]) > 1 and abs(k - center[1]) > 1) or (
                                                abs(i - center[0]) <= 2 and abs(k - center[1]) == 1) or (
                                                        abs(i - center[0]) == 1 and abs(k - center[1]) <= 2)):
                                            if e % 5 == 0:
                                                exV += 1
                                                coverRate -= 1
                                        else:
                                            exV = 0
                                            if conflict < 1:
                                                coverRate += 1
                                                conflict += 1
                                        coverRate += 1
                                else:
                                    if not (self.isValidInVision(i, k - 1)): continue
                                    self.vision[i][k - 1] = COVERED
                                    exV = 1
                                    coverRate = 1
                                    conflict = 0
                                    for e in range(1, k + 1):
                                        for temp in range(coverRate):
                                            if self.isValidInVision(i - temp - exV, k - e):
                                                self.vision[i - temp - exV][k - e] = COVERED
                                        if (i + 1 != center[0] or self.vision[i + 1][k] != 1) and (
                                                (abs(i - center[0]) > 1 and abs(k - center[1]) > 1) or (
                                                abs(i - center[0]) <= 2 and abs(k - center[1]) == 1) or (
                                                        abs(i - center[0]) == 1 and abs(k - center[1]) <= 2)):
                                            if e % 5 == 0:
                                                exV += 1
                                                coverRate -= 1
                                        else:
                                            exV = 0
                                            if conflict < 1:
                                                coverRate += 1
                                                conflict += 1
                                        coverRate += 1
                            # print("I was here quarter 2")
                        else:
                            # quater 3
                            if k < center[1]:
                                if i + k > center[0] + center[1]:
                                    if not (self.isValidInVision(i + 1, k)): continue

                                    self.vision[i + 1][k] = COVERED
                                    exV = 1
                                    coverRate = 1
                                    conflict = 0
                                    for e in range(1, len(self.vision) - i):
                                        for temp in range(coverRate):
                                            if self.isValidInVision(i + e, k - temp - exV):
                                                self.vision[i + e][k - temp - exV] = COVERED
                                        if (k + 1 != center[1] or self.vision[i][k + 1] != 1) and (
                                                (abs(i - center[0]) > 1 and abs(k - center[1]) > 1) or (
                                                abs(i - center[0]) <= 2 and abs(k - center[1]) == 1) or (
                                                        abs(i - center[0]) == 1 and abs(k - center[1]) <= 2)):
                                            if e % 5 == 0:
                                                exV += 1
                                                coverRate -= 1
                                        else:
                                            exV = 0
                                            if conflict < 1:
                                                coverRate += 1
                                                conflict += 1
                                        coverRate += 1
                                else:
                                    if not (self.isValidInVision(i, k - 1)): continue
                                    self.vision[i][k - 1] = COVERED
                                    exV = 1
                                    coverRate = 1
                                    conflict = 0
                                    for e in range(1, k + 1):
                                        for temp in range(coverRate):
                                            if self.isValidInVision(i + temp + exV, k - e):
                                                self.vision[i + temp + exV][k - e] = COVERED
                                        if (i - 1 != center[0] or self.vision[i - 1][k] != 1) and (
                                                (abs(i - center[0]) > 1 and abs(k - center[1]) > 1) or (
                                                abs(i - center[0]) <= 2 and abs(k - center[1]) == 1) or (
                                                        abs(i - center[0]) == 1 and abs(k - center[1]) <= 2)):
                                            if e % 5 == 0:
                                                exV += 1
                                                coverRate -= 1
                                        else:
                                            exV = 0
                                            if conflict < 1:
                                                coverRate += 1
                                                conflict += 1
                                        coverRate += 1
                                # print("I was here quarter 3")
                            # quater 4
                            else:
                                if k - i < center[1] - center[0]:
                                    if not (self.isValidInVision(i + 1, k)): continue
                                    self.vision[i + 1][k] = COVERED
                                    exV = 1
                                    coverRate = 1
                                    conflict = 0
                                    for e in range(1, len(self.vision) - i):
                                        for temp in range(coverRate):
                                            if self.isValidInVision(i + e, k + temp + exV):
                                                self.vision[i + e][k + temp + exV] = COVERED
                                        if (k - 1 != center[1] or self.vision[i][k - 1] != 1) and (
                                                (abs(i - center[0]) > 1 and abs(k - center[1]) > 1) or (
                                                abs(i - center[0]) <= 2 and abs(k - center[1]) == 1) or (
                                                        abs(i - center[0]) == 1 and abs(k - center[1]) <= 2)):
                                            if e % 5 == 0:
                                                exV += 1
                                                coverRate -= 1
                                        else:
                                            exV = 0
                                            if conflict < 1:
                                                coverRate += 1
                                                conflict += 1
                                        coverRate += 1
                                else:
                                    if not (self.isValidInVision(i, k + 1)): continue
                                    self.vision[i][k + 1] = COVERED
                                    exV = 1
                                    coverRate = 1
                                    conflict = 0
                                    for e in range(1, len(self.vision[0]) - k):
                                        for temp in range(coverRate):
                                            if self.isValidInVision(i + temp + exV, k + e):
                                                self.vision[i + temp + exV][k + e] = COVERED
                                        if (i - 1 != center[0] or self.vision[i - 1][k] != 1) and (
                                                (abs(i - center[0]) > 1 and abs(k - center[1]) > 1) or (
                                                abs(i - center[0]) <= 2 and abs(k - center[1]) == 1) or (
                                                        abs(i - center[0]) == 1 and abs(k - center[1]) <= 2)):
                                            if e % 5 == 0:
                                                exV += 1
                                                coverRate -= 1
                                        else:
                                            exV = 0
                                            if conflict < 1:
                                                coverRate += 1
                                                conflict += 1
                                        coverRate += 1
                                # print("I was here quarter 4")

        # print("I was here final")
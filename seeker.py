import pygame
from constants import *


class Seeker:

    icon = pygame.transform.scale(pygame.image.load('characterIcon/dog.png'), (SQUARE_SIZE - 1, SQUARE_SIZE - 1))

    def __init__(self):
        self.Sx = -1
        self.Sy = -1
        self.vision = []
        self.top, self.left, self.bottom, self.right = 0, 0, 0, 0
        self.radius = 3
        self.movement = 1
        self.visitMap = []
        self.currentTime = 0

    def build_visitMap(self, map):
        for i in map:
            self.visitMap.append(list(i))

    def mark_visitMap(self):
        #print(self.top, self.bottom, self.left, self.right)
        for row in range(self.top, self.bottom + 1):
            for col in range(self.left, self.right + 1):
                #print(row, col)
                #print(self.vision[row - self.top][col - self.left])
                if self.vision[row - self.top][col - self.left] == VISIBLE:
                    self.visitMap[row][col] = self.currentTime

    def update(self, newCor, map):
        if self.Sx != -1:
            map[self.Sx][self.Sy] = 0
        self.Sx = newCor[0]
        self.Sy = newCor[1]
        map[self.Sx][self.Sy] = 3

        self.visionScopeUpdate(map)
        self.visibleUpdate()
        self.currentTime += 1
        self.mark_visitMap()


    def drawSeeker(self, win):
        win.blit(Seeker.icon, (self.Sy * SQUARE_SIZE, self.Sx * SQUARE_SIZE))

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

        '''print('This is current map')
        for jk in map:
            print(jk)
        '''
        for i in range(self.top, self.bottom + 1):
            temp = list(map[i])
            self.vision.append(temp[self.left : self.right + 1])


    def getSeekerInVision(self):
        return [self.Sx - self.top, self.Sy - self.left]

    def isValidInVision(self, row, col):
        if 0 <= row < len(self.vision) and 0 <= col < len(self.vision[0]):
            return True
        return False

    def randomHeuristic(self, currentTime, visitMap):
        '''
        count = 0
        for row in self.vision:
            count += row.count(VISIBLE)
        '''

        count = 0
        for row in range(self.top, self.bottom + 1):
            for col in range(self.left, self.right + 1):
                if self.vision[row - self.top][col - self.left] != VISIBLE:
                    continue
                count += currentTime - visitMap[row][col]

        return count

    def drawVison(self, win, map):
        #self.visionScopeUpdate(map)
        #self.visibleUpdate()

        '''
        for i in self.vision:
            print(i)

        print('\n')
        '''

        vi = 0
        for i in range(self.top, self.bottom + 1):
            vj = 0
            for j in range(self.left, self.right + 1):
                if self.vision[vi][vj] == 0 or self.vision[vi][vj] == 2 or self.vision[vi][vj] == 3:
                    pygame.draw.rect(win, PINK,
                                     (j * SQUARE_SIZE, i * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))
                vj += 1
            vi += 1


    def valueInVision(self,row, col):
        return self.vision[row - self.top][col - self.left]

    def visited(self, visitedList, cor):
        for visit in visitedList:
            if cor == visit:
                return True
        return False

    def randomMove(self, oldMove, map):
        dummy = Seeker()
        max = -1
        nextMove = [self.Sx, self.Sy]

        for i in self.visitMap:
            print(i)
        #print('\n')
        print(self.Sx, self.Sy)
        #print(oldMove1[0], oldMove1[1])
        #print(oldMove2[0], oldMove2[1])
        for i in range(self.Sx - self.movement, self.Sx + self.movement + 1):
            for j in range(self.Sy - self.movement, self.Sy + self.movement + 1):
                if self.top <= i <= self.bottom \
                        and self.left <= j <= self.right \
                        and (i != self.Sx or j != self.Sy):

                    print('I consider a move', i, j)
                    #print(self.valueInVision(i, j), self.Sx - self.top, self.Sy - self.left, i - self.top, j- self.left)
                    if self.valueInVision(i, j) == VISIBLE:
                        #print(self.valueInVision(i, j), i, j)
                        dummy.Sx = i
                        dummy.Sy = j
                        dummy.visionScopeUpdate(map)
                        dummy.visibleUpdate()

                        heuristic = dummy.randomHeuristic(self.currentTime, self.visitMap)
                        print('H = ', heuristic)
                        if heuristic > max:
                            max = heuristic
                            #print('I got a move')
                            #print(i, j)
                            nextMove[0] = i
                            nextMove[1] = j


        ''' and not(self.visited(oldMove, [i, j]))'''
        print('i got move', nextMove[0], nextMove[1])
        print('current time :', self.currentTime)
        return nextMove



    def visibleUpdate(self):
        #(i, k): i row, k column
        center = self.getSeekerInVision()
        visibleTop = center[0]
        visibleBottom = center[0]
        visibleLeft = center[1]
        visibleRight = center[1]
        visibleNarrow = 1

        while visibleTop > 0 or visibleBottom < len(self.vision) - 1 or visibleLeft > 0 or visibleRight < len(self.vision[0]) - 1:
            if self.isValidInVision(center[0] - visibleNarrow, 0):
                visibleTop = center[0] - visibleNarrow
            if self.isValidInVision(center[0] + visibleNarrow, 0):
                visibleBottom = center[0] + visibleNarrow
            if self.isValidInVision(0, center[1] - visibleNarrow):
                visibleLeft = center[1] - visibleNarrow
            if self.isValidInVision(0, center[1] + visibleNarrow):
                visibleRight = center[1] + visibleNarrow

            #print("I was here befor checking")
            #print(center, visibleNarrow, visibleTop, visibleBottom, len(self.vision) - 1, visibleLeft, visibleRight, len(self.vision[0]) - 1)
            for i in range(visibleTop, visibleBottom + 1):
                for k in range(visibleLeft, visibleRight + 1):

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
                            #print("I was here vertical")

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
                            #print("I was here horizontal")

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
                            #print("I was here diagonal 2 4")

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
                            #print("I was here diagonal 1 3")

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
                                                    conflict +=1
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
                                                    conflict +=1
                                            coverRate += 1
                                    #print("I was here quarter 1")
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
                                                    conflict +=1
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
                                                    conflict +=1
                                            coverRate += 1
                                #print("I was here quarter 2")
                            else:
                                # quater 3
                                if k < center[1]:
                                    if i + k > center[0] + center[1]:
                                        if not(self.isValidInVision(i+1, k)): continue

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
                                                    conflict +=1
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
                                                    conflict +=1
                                            coverRate += 1
                                    #print("I was here quarter 3")
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
                                                    conflict +=1
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
                                    #print("I was here quarter 4")

                    #print('not stuck!')

            #print("I was here", visibleNarrow)
            visibleNarrow += 1

        #print("I was here final")
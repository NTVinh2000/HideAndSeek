import pygame
from constants import *


class Seeker:

    icon = pygame.transform.scale(pygame.image.load('characterIcon/dog.png'), (SQUARE_SIZE - 1, SQUARE_SIZE - 1))

    def __init__(self):
        self.Sx = 1
        self.Sy = 1
        self.vision = []
        self.top, self.left, self.bottom, self.right = 0, 0, 0, 0
        self.radius = 3
        self.movement = 1

    def update(self, newCor, map):
        map[self.Sx][self.Sy] = 0
        self.Sx = newCor[0]
        self.Sy = newCor[1]
        map[self.Sx][self.Sy] = 3

    def drawSeeker(self, win):
        win.blit(Seeker.icon, (self.Sy * SQUARE_SIZE, self.Sx * SQUARE_SIZE))

    '''
    def visionScope(self, map):
        explored = []
        frontier = []
        frontier.append([self.Sx, self.Sy])
        level = 0
        count = len(frontier)

        while level <= 3:
            explored.append(frontier[0])

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue

                    if frontier[0][0] + i in range(21) and frontier[0][1] + j in range(21):
                        if [frontier[0][0] + i, frontier[0][1] + j] in frontier or [frontier[0][0] + i, frontier[0][1] + j] in explored:
                            continue

                        if map[frontier[0][0] + i][frontier[0][1] + j] == 0:
                            frontier.append([frontier[0][0] + i, frontier[0][1] + j])

            #print(frontier)
            frontier.pop(0)
            count -= 1
            if count == 0:
                count = len(frontier)
                level += 1


        #for i in frontier:
            #explored.append([i[0], i[1]])


        return explored



    def drawVison(self, win, map):
        explored = self.visionScope(map)
        for i in explored:
            if i[0] == self.Sx and i[1] == self.Sy:
                continue

            #pygame.time.delay(300)
            pygame.draw.rect(win, PINK, (i[1] * SQUARE_SIZE, i[0] * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))
    '''

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
            self.vision.append(temp[self.left : self.right + 1])


    def getSeekerInVision(self):
        return [self.Sx - self.top, self.Sy - self.left]

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
                                    if e % (abs(center[0] - i) + 1) == 0:
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
                                    if e % (abs(center[0] - i) + 1) == 0:
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
                                    if e % (abs(center[1] - k) + 1) == 0:
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
                                    if e % (abs(center[1] - k) + 1) == 0:
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
                                            coverRate += 1
                                    else:
                                        if not (self.isValidInVision(i, k + 1)): continue
                                        self.vision[i][k + 1] = COVERED
                                        exV = 1
                                        coverRate = 1
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
                                            coverRate += 1
                                    #print("I was here quarter 1")
                                # quater 2
                                else:
                                    if k - i > center[1] - center[0]:
                                        if not (self.isValidInVision(i - 1, k)): continue
                                        self.vision[i - 1][k] = COVERED
                                        exV = 1
                                        coverRate = 1
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
                                            coverRate += 1
                                    else:
                                        if not (self.isValidInVision(i, k - 1)): continue
                                        self.vision[i][k - 1] = COVERED
                                        exV = 1
                                        coverRate = 1
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

                                            coverRate += 1
                                    else:
                                        if not (self.isValidInVision(i, k - 1)): continue
                                        self.vision[i][k - 1] = COVERED
                                        exV = 1
                                        coverRate = 1
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
                                            coverRate += 1
                                    #print("I was here quarter 3")
                                # quater 4
                                else:
                                    if k - i < center[1] - center[0]:
                                        if not (self.isValidInVision(i + 1, k)): continue
                                        self.vision[i + 1][k] = COVERED
                                        exV = 1
                                        coverRate = 1
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
                                            coverRate += 1
                                    else:
                                        if not (self.isValidInVision(i, k + 1)): continue
                                        self.vision[i][k + 1] = COVERED
                                        exV = 1
                                        coverRate = 1
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
                                            coverRate += 1
                                    #print("I was here quarter 4")

                    #print('not stuck!')

            #print("I was here", visibleNarrow)
            visibleNarrow += 1

        #print("I was here final")

        '''
        # check conflict 2 wall
        if self.vision[center[0] - 1][center[1]] == 1:
            if self.vision[center[0] - 1][center[1] + 1] == 1:
                if self.isValidInVision(center[0] - 2, center[1] + 1):
                    self.vision[center[0] - 2][center[1] + 1] = -1
            if self.vision[center[0] - 1][center[1] - 1] == 1:
                if self.isValidInVision(center[0] - 2, center[1] - 1):
                    self.vision[center[0] - 2][center[1] - 1] = -1
        if self.vision[center[0] + 1][center[1]] == 1:
            if self.vision[center[0] + 1][center[1] + 1] == 1:
                if self.isValidInVision(center[0] + 2, center[1] + 1):
                    self.vision[center[0] + 2][center[1] + 1] = -1
            if self.vision[center[0] + 1][center[1] - 1] == 1:
                if self.isValidInVision(center[0] + 2, center[1] - 1):
                    self.vision[center[0] + 2][center[1] - 1] = -1
        if self.vision[center[0]][center[1] - 1] == 1:
            if self.vision[center[0] - 1][center[1] - 1] == 1:
                if self.isValidInVision(center[0] - 1, center[1] - 2):
                    self.vision[center[0] - 1][center[1] - 2] = -1
            if self.vision[center[0] + 1][center[1] - 1] == 1:
                if self.isValidInVision(center[0] + 1, center[1] - 2):
                    self.vision[center[0] + 1][center[1] - 2] = -1
        if self.vision[center[0]][center[1] + 1] == 1:
            if self.vision[center[0] - 1][center[1] + 1] == 1:
                if self.isValidInVision(center[0] - 1, center[1] + 2):
                    self.vision[center[0] - 1][center[1] + 2] = -1
            if self.vision[center[0] + 1][center[1] + 1] == 1:
                if self.isValidInVision(center[0] + 1, center[1] + 2):
                    self.vision[center[0] + 1][center[1] + 2] = -1
        '''


    def isValidInVision(self, row, col):
        if 0 <= row < len(self.vision) and 0 <= col < len(self.vision[0]):
            return True
        return False

    def randomHeuristic(self):
        count = 0
        for row in self.vision:
            count += row.count(VISIBLE)
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
        return self.vision[row - self.top][col - self.right]

    def randomMove(self, oldMove, map):
        dummy = Seeker()
        max = -1
        nextMove = [self.Sx, self.Sy]

        for i in self.vision:
            print(i)
        #print('\n')
        print(oldMove[0], oldMove[1])
        for i in range(self.Sx - self.movement, self.Sx + self.movement + 1):
            for j in range(self.Sy - self.movement, self.Sy + self.movement + 1):
                print('I consider a move', i, j)
                if self.top <= i <= self.bottom \
                        and self.left <= j <= self.right \
                        and (i != oldMove[0] or j != oldMove[1]):

                    if self.valueInVision(i, j) == VISIBLE:
                        print(self.valueInVision(i, j), i, j)
                        dummy.Sx = i
                        dummy.Sy = j
                        dummy.visionScopeUpdate(map)
                        dummy.visibleUpdate()
                        heuristic = dummy.randomHeuristic()
                        print('I consider a move', i, j)
                        if heuristic > max:
                            print('I got a move')
                            nextMove[0] = i
                            nextMove[1] = j

        '''and i != self.Sx and j != self.Sy '''
        print(nextMove[0], nextMove[1])
        return nextMove
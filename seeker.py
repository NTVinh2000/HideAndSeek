import pygame
from constants import *
import numpy as np


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
        self.currentTime = 1
        #self.Shortest_path = np.zeros((ROW, COL, ROW, COL))
        self.hiderPositionList = []  # save list of hiders position have been found
        # print(self.Shortest_path.shape)
        # print('ROW {} COL {}'.format(ROW,COL))


    # Build a sub map to mark visited tile
    # This map will include values to calculate heuristic
    def build_visitMap(self, map):
        # for i in map:
        #    self.visitMap.append(list(i))
        self.visitMap = np.zeros((ROW, COL))
        self.visitMap[self.Sx][self.Sy] = self.currentTime

    # Mark seen titles by assigning current time value
    def mark_visitMap(self):
        for row in range(self.top, self.bottom + 1):
            for col in range(self.left, self.right + 1):
                if self.vision[row - self.top][col - self.left] == VISIBLE or self.vision[row - self.top][
                    col - self.left] == HIDER_ID:
                    self.visitMap[row][col] = self.currentTime

    def BreathFirstSearch(self, posNow, queue, prev, map):
        Ix = [-1, -1, -1, 0, 1, 1, 1, 0]
        Iy = [-1, 0, 1, 1, 1, 0, -1, -1]

        while queue.shape[0] != 0:
            queue = queue.reshape((-1, 3))
            cur = [0, 0]
            dis = 0
            # print(queue)
            (cur[0], cur[1], dis) = queue[0][:]
            queue = np.delete(queue, 0, 0)
            for i in range(8):
                newPosX = cur[0] + Ix[i]
                newPosY = cur[1] + Iy[i]
                if (newPosX < 1 or newPosX > ROW - 2 or newPosY < 1 or newPosY > COL - 2):
                    continue
                if (map[newPosX][newPosY] == 1):
                    continue
                if (prev[newPosX][newPosY][0] == 0 and prev[newPosX][newPosY][1] == 0):
                    prev[newPosX][newPosY][:] = [cur[0], cur[1]]
                    queue = np.append(queue, [(newPosX, newPosY, dis + 1)])
                    if (self.visitMap[newPosX][newPosY] == 0):
                        print('{} {} return'.format(newPosX, newPosY))
                        return (newPosX, newPosY)
        return None

    def getPathToUnvisited(self, map):
        # trả lại list các tuble các vị trí đi đến ô unvisited gần nhất
        # nếu không có trả lại None
        # code bug, please không sử dụng
        # print('{} {} ok ?'.format(ROW,COL))
        prev = np.zeros((ROW, COL, 2))
        prev[self.Sx][self.Sy][:] = [self.Sx, self.Sy]
        queue = np.array([(self.Sx, self.Sy, 0)])
        new_pos = self.BreathFirstSearch([self.Sx, self.Sy], queue, prev, map)
        if (new_pos is None):
            return None
        print(new_pos)
        result = []
        (curX, curY) = new_pos
        while (curX != self.Sx or curY != self.Sy):
            # print(curX,curY,prev[curX][curY])
            result.append((curX, curY))
            tmpX = int(prev[curX][curY][0])
            tmpY = int(prev[curX][curY][1])
            curX = tmpX
            curY = tmpY

        # result.append((curX, curY))
        # result.reverse()
        # print('{} {}'.format(self.Sx,self.Sy))
        # print(result[0])
        # print('ok')
        return result[-1]

    def BFS_for_shortest(self, begin, queue, map):
        Ix = [-1, -1, -1, 0, 1, 1, 1, 0]
        Iy = [-1, 0, 1, 1, 1, 0, -1, -1]

        while queue.shape[0] != 0:
            queue = queue.reshape((-1, 3))
            cur = [0, 0]
            dis = 0
            # print(queue)
            (cur[0], cur[1], dis) = queue[0][:]
            queue = np.delete(queue, 0, 0)
            for i in range(8):
                newPosX = cur[0] + Ix[i]
                newPosY = cur[1] + Iy[i]
                if (newPosX < 1 or newPosX > ROW - 2 or newPosY < 1 or newPosY > COL - 2):
                    continue
                if (map[newPosX][newPosY] == 1):
                    continue
                if (self.Shortest_path[begin[0]][begin[1]][newPosX][newPosY] == -1):
                    self.Shortest_path[begin[0]][begin[1]][newPosX][newPosY] = dis + 1
                    queue = np.append(queue, [(newPosX, newPosY, dis + 1)])

    #return path from begin to end
    def FromStartToEnd(self, begin, end, map):
        Ix = [-1, -1, -1, 0, 1, 1,  1,  0]
        Iy = [-1,  0,  1, 1, 1, 0, -1, -1]
        queue = np.array([(begin[0],begin[1],0)])
        prev = np.zeros((ROW,COL,2))
        prev[begin[0]][begin[1]][:] = [begin[0],begin[1]]
        while queue.shape[0] != 0:
            queue = queue.reshape((-1,3))
            cur = [0,0]
            dis = 0
            #print(queue)
            (cur[0],cur[1],dis) = queue[0][:]
            queue = np.delete(queue,0,0)
            #print(cur[0],cur[1])
            for i in range(8):
                newPosX = cur[0] + Ix[i]
                newPosY = cur[1] + Iy[i]
                if (newPosX < 1 or newPosX > ROW-2 or newPosY < 1 or newPosY > COL-2):
                    continue
                if (map[newPosX][newPosY] == 1):
                    continue
                if (prev[newPosX][newPosY][0]==0 and prev[newPosX][newPosY][1] == 0):
                    prev[newPosX][newPosY][:]= [cur[0],cur[1]]
                    queue = np.append(queue, [(newPosX, newPosY, dis+1)])
                    if (newPosX == end[0] and newPosY == end[1]):
                        curX = int(newPosX)
                        curY = int(newPosY)
                        res = []
                        while(curX != begin[0] or curY != begin[1]):
                            res.append((curX,curY))
                            tmpX = prev[curX][curY][0]
                            tmpY = prev[curX][curY][1]
                            curX = int(tmpX)
                            curY = int(tmpY)
                        res.append((curX,curY))
                        res.reverse()
                        res = np.array(res)

                        return res.tolist()
    # trả lại bảng shortest_path[Row][Col][Row][Col]

    def Create_Shortest_path_table(self, map):
        print('ROW {} COL {}'.format(ROW, COL))
        for i in range(ROW - 2):
            for j in range(COL - 2):
                queue = np.array([(i + 1, j + 1, 0)])
                self.Shortest_path[i + 1][j + 1][i + 1][j + 1] = 0
                self.BFS_for_shortest([i + 1, j + 1], queue, map)
                print('finish {} {}'.format(i + 1, j + 1))

    # update position of seeker in origin map
    # including update vision scope, update vision
    # this function increases current time by 1 and mark visitMap
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

    # take vision region of seeker
    # this function update vision scope
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

    # caculate heuristic
    def randomHeuristic(self, currentTime, visitMap):
        '''
        count = 0
        for row in self.vision:
            count += row.count(VISIBLE)
        '''
        zero_cnt = 0
        count = 0
        for row in range(self.top, self.bottom + 1):
            for col in range(self.left, self.right + 1):
                if self.vision[row - self.top][col - self.left] != VISIBLE:
                    continue
                count += currentTime - visitMap[row][col]
                if (visitMap[row][col] == 0):
                    zero_cnt += 1

        return (count, zero_cnt)

    # find next move
    def randomMove(self, map):
        # self.getPathToUnvisited(map)
        dummy = Seeker()
        max = -1
        max_zero = 0
        nextMove = [self.Sx, self.Sy]

        # for i in self.vision:
        #    print(i)
        # print(self.Sx, self.Sy)

        for i in range(self.Sx - self.movement, self.Sx + self.movement + 1):
            for j in range(self.Sy - self.movement, self.Sy + self.movement + 1):
                if self.top <= i <= self.bottom \
                        and self.left <= j <= self.right \
                        and (i != self.Sx or j != self.Sy):

                    # print('I consider a move', i, j)
                    # print(self.valueInVision(i, j), self.Sx - self.top, self.Sy - self.left, i - self.top, j- self.left)
                    if self.valueInVision(i, j) == VISIBLE:
                        dummy.Sx = i
                        dummy.Sy = j
                        dummy.visionScopeUpdate(map)
                        dummy.visibleUpdate()
                        (heuristic, zero_cnt) = dummy.randomHeuristic(self.currentTime, self.visitMap)

                        # print('H = ', heuristic)
                        if (zero_cnt > max_zero):
                            max_zero = zero_cnt

                        if heuristic > max:
                            max = heuristic
                            nextMove[0] = i
                            nextMove[1] = j
        if (max_zero == 0):
            nextMove = self.getPathToUnvisited(map)
        # print('i got move', nextMove[0], nextMove[1])
        # print('current time :', self.currentTime)
        return nextMove

    '''--------------------------------------------------------------------------------------------------------------'''

    # this function return position of seeker in its vision
    def getPositionInVision(self):
        return [self.Sx - self.top, self.Sy - self.left]

    # draw vision
    def drawVison(self, win, map):
        vi = 0
        for i in range(self.top, self.bottom + 1):
            vj = 0
            for j in range(self.left, self.right + 1):
                if self.vision[vi][vj] == 0 or self.vision[vi][vj] == 2 or self.vision[vi][vj] == 3:
                    pygame.draw.rect(win, PINK,
                                     (j * SQUARE_SIZE, i * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1))
                vj += 1
            vi += 1

    # draw seeker
    def drawSeeker(self, win):
        win.blit(Seeker.icon, (self.Sy * SQUARE_SIZE, self.Sx * SQUARE_SIZE))

    # check a given tile is in list visited or not
    def visited(self, visitedList, cor):
        for visit in visitedList:
            if cor == visit:
                return True
        return False

    # this function checks if a given tile belong to vision or not
    def isValidInVision(self, row, col):
        if 0 <= row < len(self.vision) and 0 <= col < len(self.vision[0]):
            return True
        return False

    # this function returns value in Vision: VISIBLE(0) or others
    def valueInVision(self, row, col):
        return self.vision[row - self.top][col - self.left]

    # check which tiles are VISIBLE(0) and mark COVERED(-1) tiles
    def visibleUpdate(self):
        # (i, k): i row, k column
        center = self.getPositionInVision()
        for i in range(0, len(self.vision) + 1):
            for k in range(0, len(self.vision[0]) + 1):

                if not (self.isValidInVision(i, k)): continue

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

    def findHider(self):
        vision_x = 0
        vision_y = 0
        for i in range(0, len(self.vision)):
            for j in range(0, len(self.vision[i])):
                if self.vision[i][j] == 3:
                    vision_x = i
                    vision_y = j
                    break
        for i in range(0, len(self.vision)):
            for j in range(0, len(self.vision[i])):
                if self.vision[i][j] == 2:
                    temp = []
                    #hider_x = self.Sx - (3 - i)
                    #hider_y = self.Sy - (3 - j)
                    hider_x = self.Sx + (i-vision_x)
                    hider_y = self.Sy + (j-vision_y)
                    temp.append(hider_x)
                    temp.append(hider_y)
                    flag = False
                    for k in self.hiderPositionList:
                        if k[0] == hider_x and k[1] == hider_y:
                            flag = True
                            break
                    if flag == False:
                        self.hiderPositionList.append(temp)

        return self.hiderPositionList


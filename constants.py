
WIDTH, HEIGHT = 600, 600
ROW, COL = 20, 20
SQUARE_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (252, 252, 252)
PINK = (255, 192, 203)
COVERED = -1
VISIBLE = 0
WALL_ID = 1
HIDER_ID = 2
SEEKER_ID = 3
OBSTACLE_ID = 4
ANNOUNCE_ID = 5

def load_map(path):
    fileMap = open(path, 'r')
    data = fileMap.readlines()
    fileMap.close()

    global ROW, COL, HEIGHT, WIDTH
    ROW, COL = data[0].strip('\n').split(' ')
    ROW = int(ROW)
    COL = int(COL)
    HEIGHT = ROW * SQUARE_SIZE
    WIDTH = COL * SQUARE_SIZE

    return take_map_info(data)


def take_map_info(data):
    map = []
    for i in range(ROW):
        map.append(data[i + 1].strip('\n').split(' '))

    for i in range(ROW):
        for j in range(COL):
            map[i][j] = int(map[i][j])

    seekerList = []
    hiderList = []
    for i in range(ROW):
        for j in range(COL):
            if map[i][j] == 2:
                hiderList.append([i, j])
            elif map[i][j] == 3:
                seekerList.append([i, j])

    obstacle = []

    if ROW + 1 < len(data):
        for i in range(ROW + 1, len(data)):
            obstacle.append(data[i].strip('\n').split(' '))


    info = []
    info.append(map)
    info.append(seekerList)
    info.append(hiderList)
    info.append(obstacle)

    return info
WALL = 1
import frontend as fe
from Agent import Agent

def is_inside(position, size):
    x, y = position
    return (0 <= x < size[0]) and (0 <= y < size[1])

def updateVision(pos, vision):
    listSeen = []
    for point in vision:
        listSeen.append((point[0] + pos[0], point[1] + pos[1]))
    return listSeen

def observe(position, grid, size):
    vision = set()  # Initialize the vision list

    x, y = position

    if (grid[x][y] == WALL):
        return list(vision)

    flatten = [
        [(-1,0), (-2,0), (-3,0)], # vertical
        [(0,1), (0,2), (0,3)], # horizontal
        [(-1,1), (-2,2), (-3,3)], # diagonal
        [(-2,1), (-3,1), (-3,2)], # VxD
        [(-1,2), (-1,3), (-2,3)] # HxD
    ]

    quarters = [
        (1,1),   # quarter 1
        (1,-1),  # quarter 2
        (-1,-1), # quarter 3
        (-1,1)   # quarter 4
    ]
    for quarter in quarters:
        # Make new flatten for each quarter
        new_flatten = []
        for sublist in flatten:
            new_sublist = []
            for point in sublist:
                new_point = (quarter[0] * point[0], quarter[1] * point[1])
                new_sublist.append(new_point)
            new_flatten.append(new_sublist)

        # check vertical
        flag_v = False
        for i in range(3):
            new_x, new_y = x + new_flatten[0][i][0], y + new_flatten[0][i][1]
            if not (is_inside((new_x, new_y), size)):
                break
            if (grid[new_x][new_y] == WALL):
                print(new_x, new_y)
                if (i == 0):
                    flag_v = True
                del new_flatten[0][i+1:]
                break

        # check horizontal
        flag_h = False
        for i in range(3):
            new_x, new_y = x + new_flatten[1][i][0], y + new_flatten[1][i][1]
            if not (is_inside((new_x, new_y), size)):
                break
            if (grid[new_x][new_y] == WALL):
                if (i == 0):
                    flag_h = True
                del new_flatten[1][i+1:]
                break

        # check diagonal
        flag_d = False
        for i in range(3):
            new_x, new_y = x + new_flatten[2][i][0], y + new_flatten[2][i][1]
            if not (is_inside((new_x, new_y), size)):
                break
            if (grid[new_x][new_y] == WALL):
                if (i == 0):
                    flag_d = True
                del new_flatten[2][i+1:]
                break

        if flag_d:
            del new_flatten[3][2]
            del new_flatten[4][2]

        if flag_v:
            del new_flatten[3][1]

        if flag_h:
            del new_flatten[4][1]

        if flag_d and flag_v:
            del new_flatten[3][:]

        if flag_d and flag_h:
            del new_flatten[4][:]

        # check VxD
        if (len(new_flatten[3]) > 0):
            new_x, new_y = x + new_flatten[3][0][0], y + new_flatten[3][0][1]
            if (is_inside((new_x, new_y), size)):
                if grid[new_x][new_y] == WALL:
                    del new_flatten[3][1:]
        # check HxD
        if (len(new_flatten[4]) > 0):
            new_x, new_y = x + new_flatten[4][0][0], y + new_flatten[4][0][1]
            if  (is_inside((new_x, new_y), size)):
                if grid[new_x][new_y] == WALL:
                    del new_flatten[4][1:]

        vision.add((x, y))

        for sublist in new_flatten:
            for point in sublist:
                new_x = point[0] + x
                new_y = point[1] + y
                if not is_inside((new_x, new_y), size) or grid[new_x][new_y] == WALL:
                    continue
                vision.add((new_x, new_y))

    return list(vision)

def cal_heuristic(pos, grid, size, listSeen):
    # find the cell with biggest vision
    h = 0
    listWillSee = observe(pos, grid, size)
    for point in listWillSee:
        x, y = point
        if grid[x][y] != WALL and point not in listSeen:
            h+=1
            print(x, y)
            print()
    return h


def AStar():
    pass

def updateBoard(grid, pos, listVision):
        newGrid = grid.copy()
        for point in listVision:
            newGrid[point[0]][point[1]] = 5
        return newGrid


def test1():
    size = 7, 7
    grid = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 3, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 0, 0, 0],
        ]

    seenGrid = grid.copy()

    obstacles = [((1, 0), (1, 0))] # fix later
    seekerPos = 3, 3
    vision = observe(seekerPos, grid, size)
    fe.createFrontEnd(grid, size, vision)

    # newSeekerPos = 4, 3
    # newVision = observe(newSeekerPos, grid, size)
    # grid[3][3], grid[4][3] = grid[4][3], grid[3][3]
    # a = cal_heuristic(newSeekerPos, grid, size, vision)
    # updateBoard(grid, newVision)
    # fe.createFrontEnd(grid, size)
    # print(a)

test1()
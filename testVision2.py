SEEKER = 3
WALL = 1

def is_inside(position, size):
    x, y = position
    return (0 <= x < size[0]) and (0 <= y < size[1])


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

        for sublist in new_flatten:
            for point in sublist:
                vision.add(point)

    return list(vision)


def printBroad(grid, size):
    for i in range(size[0]):
        for j in range(size[1]):
            if (j % size[1] == 0 and i != 0):
                print()
            print(grid[i][j], end=" ")

def redrawGrid(grid, size, seekerPos, listVision):
    newGrid = grid.copy()
    for k in range(len(listVision)):
        if not (is_inside((seekerPos[0] + listVision[k][0], seekerPos[1] + listVision[k][1]), size)):
            continue
        if newGrid[seekerPos[0] + listVision[k][0]][seekerPos[1] + listVision[k][1]] == 1:
            continue
        newGrid[seekerPos[0] + listVision[k][0]][seekerPos[1] + listVision[k][1]] = 5
    return newGrid

def findSeeker(grid, size):
    for i in range(size[0]):
        for j in range(size[1]):
            if grid[i][j] == SEEKER:
                return i, j

# data = [
#     [1, 0, 1, 0, 0, 0, 0],
#     [0, 1, 0, 1, 0, 0, 0],
#     [1, 0, 1, 0, 0, 0, 0],
#     [0, 1, 0, 9, 0, 0, 0],
#     [0, 0, 1, 0, 1, 0, 0],
#     [0, 0, 0, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
# ]
# size = 7, 7
# pos = 3, 3
# printBroad(data, size)

# print()

# vision = observe((3, 3), data)
# print(vision)
# redrawGrid(data, size, pos, vision)
# print()
# printBroad(data, size)
WALL = 1
import frontend as fe
from Agent import Agent
import heapq
from inputMap import readInputFile
import board as bd

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

def cal_new_vision(pos, grid, size, listSeen):
def cal_new_vision(pos, grid, size, listSeen):
    # find the cell with biggest vision
    new_vision  = 0
    new_vision  = 0
    listWillSee = observe(pos, grid, size)
    for point in listWillSee:
        x, y = point
        if grid[x][y] != WALL and point not in listSeen:
            new_vision+=1
    return new_vision

def cal_heuristic():
    pass


def neighbors8(node, rows, cols):
    row, col = node
    list_neighbor = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols:
                list_neighbor.append((new_row,new_col))
    return list_neighbor        
        

def Search(grid, start, size, has_seen):
    visited = set()
    
    heap = [(-len(has_seen), start, [start], set())] # value(vision), node, path, list_seen
    
    # visited.add(start)
    
    max_vision = -len(has_seen)
    max_vision_path = [start]

    while heap:
        print(max_vision)
        print(max_vision_path)
        value, node, path, list_seen = heapq.heappop(heap)

        if node in visited:
            continue

        visited.add(node)

        #update list_seen
        list_seen.update(observe(node, grid, size))
        
        if not path:
            max_vision = -value
            max_vision_path = path
        elif -value > max_vision:
            max_vision = -value
            max_vision_path = path
        
        for new_x, new_y in neighbors8(node, size[0], size[1]):
            if (new_x, new_y) not in visited and grid[new_x][new_y] != WALL:
                # visited.add((new_x, new_y))
                new_value = len(list_seen) + cal_new_vision((new_x, new_y), grid, size, list_seen)
                heapq.heappush(heap,( -new_value, (new_x, new_y), path + [(new_x, new_y)], list_seen))
        
    return max_vision, max_vision_path


def updateBoard(grid, pos, listVision):
        newGrid = grid.copy()
        for point in listVision:
            newGrid[point[0]][point[1]] = 5
        return newGrid

def Search_2(grid, start, size, has_seen, time_visited):
    visited = {}  # Use a dictionary instead of a set to keep track of the number of times each cell is visited
    max_vision = 0
    max_vision_path = []
    
    heap = [(-len(has_seen), start, [start], set())]  # value(vision), node, path, list_seen
    
    visited[start] = 1  # Initialize the starting cell with a visit count of 1
    
    while heap:
        value, node, path, list_seen = heapq.heappop(heap)
        if node not in visited:
            pass
        elif visited[node] >= time_visited:
            continue
            
        visited[node] = visited.get(node, 0) + 1
        # Update list_seen
        list_seen.update(observe(node, grid, size))
        
        if not path:
            max_vision = -value
            max_vision_path = path
        elif -value > max_vision:
            max_vision = -value
            max_vision_path = path
        
        for new_x, new_y in neighbors8(node, size[0], size[1]):
            if grid[new_x][new_y] == WALL:
                continue
            if (new_x, new_y) not in visited or visited[(new_x, new_y)] < time_visited :
                print(new_x, new_y)
                # visited[(new_x, new_y)] = visited.get((new_x, new_y), 0) + 1
                new_value = len(list_seen) + cal_new_vision((new_x, new_y), grid, size, list_seen)
                heapq.heappush(heap, (-new_value, (new_x, new_y), path + [(new_x, new_y)], list_seen))
        
    return max_vision, max_vision_path

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
    value, path = Search(grid, (3,3), (7,7), observe((3,3), grid, size))
    print(value)
    print(path)

def test2():
    N, M, board, obstacle = readInputFile("map1_1.txt")
    testBoard = bd.Board((N, M), board, obstacle)
    testBoard.printBroad()
    seekerVision = testBoard.seeker.vision(testBoard.grid)
    print(testBoard.seeker.position)
    value, path = Search_2(testBoard.grid, (testBoard.seeker.position[0], testBoard.seeker.position[1]), testBoard.size,
                        observe((testBoard.seeker.position[0], testBoard.seeker.position[1]), testBoard.grid, testBoard.size), 2)
    print(value)
    print(path)

    listAllVision = []
    for point in path:
        tmp = observe(point, board, (N, M))
        for i in tmp:
            listAllVision.append(i)

    cnt = 0
    # print(len(listAllVision))
    for x in range(N):
        for y in range(M):
            if board[x][y] == WALL:
                cnt+=1
    print(cnt)

    newGrid = testBoard.grid.copy()
    for point in path:
        newGrid[point[0]][point[1]] = 6
    fe.createFrontEnd(newGrid, (N, M), listAllVision)
    # fe.createFrontEnd(testBoard.grid, testBoard.size, seekerVision)

test2()
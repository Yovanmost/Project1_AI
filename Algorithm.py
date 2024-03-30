
import heapq

def is_inside(position, size):
    x, y = position
    rows, cols = size
    return (0 <= x < rows) and (0 <= y < cols)

WALL = 1
def observe(position, grid, size):
    vision = set()
    x, y = position
    if grid[x][y] == WALL:
        return list()
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
        
        flag = [False, False, False]
        for time in range(3):
            for i in range(3):
                new_x = x + new_flatten[time][i][0]
                new_y = y + new_flatten[time][i][1]
                if not is_inside((new_x, new_y), size):
                    break
                if grid[new_x][new_y] == WALL:
                    if i == 0:
                        flag[time] = True
                    del new_flatten[time][i:]
                    break
        if flag[2]:
            del new_flatten[3][2]
            del new_flatten[4][2]
            
        if flag[0]:
            del new_flatten[3][1]
            
        if flag[1]:
            del new_flatten[4][1]
            
        if flag[0] and flag[2]:
            del new_flatten[3][:]
            
        if flag[1] and flag[2]:
            del new_flatten[4][:]
        
        for time in [3,4]:
            if len(new_flatten[time]) <= 0:
                continue
            new_x = x + new_flatten[time][0][0]
            new_y = y + new_flatten[time][0][1]
            if not is_inside((new_x, new_y), size):
                continue
            if grid[new_x][new_y] == WALL:
                del new_flatten[time][:]
                
        vision.add((x,y))
        for sublist in new_flatten:
            for point in sublist:
                new_x = point[0] + x
                new_y = point[1] + y
                if not is_inside((new_x, new_y), size) or grid[new_x][new_y] == WALL:
                    continue
                vision.add((new_x, new_y))
    return list(vision)

def generate_neighbor(pos, size):
    x, y = pos
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and  dy == 0:
                continue
            new_x, new_y = x + dx, y + dy
            if not is_inside((new_x, new_y), size):
                continue
            yield new_x, new_y

# Hàm tính số tầm nhìn mới
def cal_new_vision(pos, grid, size, list_had_seen):
    new_vision = 0
    list_new_vision = observe(pos, grid, size)
    
    for cell in list_new_vision:
        x, y = cell
        if grid[x][y] != WALL and cell not in list_had_seen:
            new_vision += 1
    return new_vision

# Hàm tìm đường đi ngắn nhất với tầm nhìn lớn nhất, (1 ô có thể đi "visited_times" lần)
def Search(pos_start, grid, size, list_had_seen, visited_times):
    visited = {}
    max_vision = len(list_had_seen)
    max_vision_path = [pos_start]
    min_steps = float("inf")
    
    # heap: (vision, cost, position, path, list_seen)
    heap = [(-max_vision, 0, pos_start, max_vision_path, list_had_seen)]

    while heap:
        value, cost, node, path, list_seen = heapq.heappop(heap)
        
        # check visited times
        if node not in visited:
            pass
        elif visited[node] >= visited_times:
            continue
        # update visited
        visited[node] = visited.get(node, 0) + 1
        # update list_seen
        list_seen.update(observe(node, grid, size))
        # update max_value, path, min cost
        if not path:
            max_vision = -value
            max_vision_path = path
            min_steps = cost
        elif -value > max_vision:
            max_vision = -value
            max_vision_path = path
            min_steps = cost
        elif -value == max_vision and cost < min_steps:
            max_vision_path = path
            min_steps = cost
        
        # generate neighbor
        for new_pos in generate_neighbor(node, size):
            if grid[new_pos[0]][new_pos[1]] == WALL:
                continue
            if new_pos not in visited or visited[new_pos] < visited_times:
                # update new cost, path, value
                new_cost = cost + 1
                new_path = path + [new_pos]
                new_value = len(list_seen) + cal_new_vision(new_pos, grid, size, list_seen)
                
                heapq.heappush(heap,(-new_value, new_cost, new_pos, new_path, list_seen))

    return max_vision, max_vision_path

def Search_priority():
    pass

def test1():
    size = 7, 7
    grid = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]

    pos = 3,3 
    value, path = Search(pos, grid, size, set(), 1)
    print(value)
    print(path)

test1()
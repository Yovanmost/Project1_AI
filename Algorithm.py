import heapq
import copy
class Algorithm:    

    WALL = 1
    def is_inside(position, size):
        x, y = position
        rows, cols = size
        return (0 <= x < rows) and (0 <= y < cols)

    
    def observe(position, grid, size):
        vision = set()
        x, y = position
        if grid[x][y] == Algorithm.WALL:
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
                    if not Algorithm.is_inside((new_x, new_y), size):
                        break
                    if grid[new_x][new_y] == Algorithm.WALL:
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
                if not Algorithm.is_inside((new_x, new_y), size):
                    continue
                if grid[new_x][new_y] == Algorithm.WALL:
                    del new_flatten[time][:]
                    
            vision.add((x,y))
            for sublist in new_flatten:
                for point in sublist:
                    new_x = point[0] + x
                    new_y = point[1] + y
                    if not Algorithm.is_inside((new_x, new_y), size) or grid[new_x][new_y] == Algorithm.WALL:
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
                if not Algorithm.is_inside((new_x, new_y), size):
                    continue
                yield new_x, new_y

    # Hàm tính số tầm nhìn mới
    def cal_new_vision(pos, grid, size, list_had_seen):
        new_vision = 0
        list_new_vision = Algorithm.observe(pos, grid, size)
        
        for cell in list_new_vision:
            x, y = cell
            if grid[x][y] != Algorithm.WALL and cell not in list_had_seen:
                new_vision += 1
        return new_vision

    # Hàm tìm đường đi ngắn nhất với tầm nhìn lớn nhất, (1 ô có thể đi "visited_times" lần)
    def Search(start, grid, size, list_had_seen, visited_times):
        visited = {}
        max_vision = len(list_had_seen)
        max_vision_path = [start]
        min_steps = float("inf")
        
        # heap: (vision, cost, position, path, list_seen)
        heap = [(-max_vision, 0, start, max_vision_path, list_had_seen)]

        count = 0

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
            list_seen.update(Algorithm.observe(node, grid, size))
            # update max_value, path, min cost
            if not max_vision_path:
                max_vision = -value
                max_vision_path = path
                min_steps = cost
            elif -value > max_vision:
                max_vision = -value
                max_vision_path = path
                min_steps = cost
            elif -value == max_vision and cost < min_steps:
                max_vision = -value
                max_vision_path = path
                min_steps = cost
            
            # generate neighbor
            for new_pos in Algorithm.generate_neighbor(node, size):
                if grid[new_pos[0]][new_pos[1]] == Algorithm.WALL:
                    continue
                if new_pos not in visited or visited[new_pos] < visited_times:
                    # update new cost, path, value
                    
                    new_cost = cost + 1
                    new_path = path + [new_pos]
                    new_value = len(list_seen) + Algorithm.cal_new_vision(new_pos, grid, size, list_seen)
                    heapq.heappush(heap,(-new_value, new_cost, new_pos, new_path, copy.deepcopy(list_seen)))
        

        return max_vision_path

    def cal_heuristic(pos, grid, size, list_had_seen, list_priority):
        heuristic = 0
        list_new_vision = Algorithm.observe(pos, grid, size)
        
        for cell in list_new_vision:
            x, y = cell
            if grid[x][y] != Algorithm.WALL and cell not in list_had_seen and cell in list_priority:
                heuristic += 1
        return heuristic

    def Search_priority(start, grid, size, list_had_seen, visited_times, list_priority):
        visited = {}
        max_value = 0
        max_value_path = [start]
        min_steps = float("inf")
        
        # heap: (vision, cost, position, path, list_seen)
        heap = [(0, 0, start, max_value_path, list_had_seen)]

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
            list_seen.update(Algorithm.observe(node, grid, size))
            # update max_value, path, min cost
            if not path:
                max_value = -value
                max_value_path = path
                min_steps = cost
            elif -value > max_value:
                max_value = -value
                max_value_path = path
                min_steps = cost
            elif -value == max_value and cost < min_steps:
                max_value_path = path
                min_steps = cost
            
            # generate neighbor
            for new_pos in Algorithm.generate_neighbor(node, size):
                if grid[new_pos[0]][new_pos[1]] == Algorithm.WALL:
                    continue
                if new_pos not in visited or visited[new_pos] < visited_times:
                    # update new cost, path, value
                    new_cost = cost + 1
                    new_path = path + [new_pos]
                    new_value = -value + Algorithm.cal_heuristic(new_pos, grid, size, list_seen, list_priority)
                    heapq.heappush(heap,(-new_value, new_cost, new_pos, new_path, copy.deepcopy(list_seen)))

        return max_value_path

    def cal_heuristic_diagonal(current, goal):
        dx = abs(current[0] - goal[0])
        dy = abs(current[1] - goal[1])
        
        D =  1 # length of each node
        D2 = 1 # diagonal distance  
        h = D *(dx + dy) + (D2 - 2*D) * min(dx,dy)
        return h

        
    def Search_shorted_path(start, goal, grid, size):
        
        heap = [(0, 0, start,[start])] # (f = g + h, g, node, path)
        visited = set()
        
        while heap:
            _, cur_g, current, path = heapq.heappop(heap)
            
            if current in visited:
                continue
            visited.add(current)
            
            if current == goal:
                return path
            
            for new_cell in Algorithm.generate_neighbor(current, size):
                if not Algorithm.is_inside(new_cell, size) or new_cell in visited or grid[new_cell[0]][new_cell[1]] == Algorithm.WALL:
                    continue
                
                new_g = cur_g + 1
                new_h = Algorithm.cal_heuristic_diagonal(current, goal)
                new_f = new_g + new_h
                new_path = path + [new_cell]
                
                heapq.heappush(heap, (new_f, new_g, new_cell, new_path))
            
    def find_list_priority(announce_position, grid, size):
        list = []
        x, y = announce_position
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                new_x, new_y = x + dx, y + dy
                if not Algorithm.is_inside((new_x, new_y), size) or grid[new_x][new_y] == Algorithm.WALL:
                    continue
                list.append((new_x, new_y))
        return list
    
    def make_priority_grid(grid, size): 
        new_grid = grid
        rows, cols = size
        # clear map
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] != Algorithm.WALL:
                    grid[i][j] = 0;
        # make priority cell
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == Algorithm.WALL:
                    for new_x, new_y in Algorithm.generate_neighbor((i,j), size):
                        if not Algorithm.is_inside((new_x, new_y), size) or grid[new_x][new_y] == Algorithm.WALL:
                            continue
                        grid[new_x][new_y] -= 1
        return new_grid

    def predict_move_hider(hider_pos, seeker_pos, priority_grid, size, list_hider_pos):        
        current_dis = len(Algorithm.Search_shorted_path(hider_pos, seeker_pos, priority_grid, size))
        # dis, priority, node
        heap = [] 
        
        for new_hider_pos in Algorithm.generate_neighbor(hider_pos, size):
            if new_hider_pos in list_hider_pos:
                continue
            if priority_grid[new_hider_pos[0]][new_hider_pos[1]] == Algorithm.WALL:
                continue
            new_dis = len(Algorithm.Search_shorted_path(new_hider_pos, seeker_pos, priority_grid, size))
            if new_dis < current_dis:
                continue
            heapq.heappush(heap, (-new_dis, -priority_grid[new_hider_pos[0]][new_hider_pos[1]], new_hider_pos))

        result = []
        while heap:
            _, _, position = heapq.heappop(heap)
            result.append(position)
        return result
    
    def predict_move_hider_for_seeker(hider_pos, seeker_pos, priority_grid, size, list_hider_pos):        
        current_dis = len(Algorithm.Search_shorted_path(hider_pos, seeker_pos, priority_grid, size))
        # dis, priority, node
        heap = [] 
        
        for new_hider_pos in Algorithm.generate_neighbor(hider_pos, size):
            if new_hider_pos in list_hider_pos:
                continue
            if priority_grid[new_hider_pos[0]][new_hider_pos[1]] == Algorithm.WALL:
                continue
            new_dis = len(Algorithm.Search_shorted_path(new_hider_pos, seeker_pos, priority_grid, size))
            if new_dis <= current_dis:
                continue
            heapq.heappush(heap, (-new_dis, -priority_grid[new_hider_pos[0]][new_hider_pos[1]], new_hider_pos))

        result = []
        while heap:
            _, _, position = heapq.heappop(heap)
            result.append(position)
        return result

    def predict_move_seeker(seeker_pos, hider_pos, priority_grid, size, list_hider_pos):
        current_dis = len(Algorithm.Search_shorted_path(seeker_pos, hider_pos, priority_grid, size))
        
        heap = []
        for new_seeker_pos in Algorithm.generate_neighbor(seeker_pos, size):
            if priority_grid[new_seeker_pos[0]][new_seeker_pos[1]] == Algorithm.WALL:
                continue
            new_dis = len(Algorithm.Search_shorted_path(new_seeker_pos, hider_pos, priority_grid, size))
            if new_dis >= current_dis:
                continue
            priority = len(Algorithm.predict_move_hider_for_seeker(hider_pos, new_seeker_pos, priority_grid, size, list_hider_pos))
            heapq.heappush(heap, (new_dis, priority, new_seeker_pos))
        
        result = []
        while heap:
            _, _, position = heapq.heappop(heap)
            result.append(position)
        return result
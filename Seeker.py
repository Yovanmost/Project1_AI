from Agent import Agent

WALL = 1

class Seeker(Agent):
    def vision(self, grid):
        ls_vision = set()  # Initialize the vision list

        x, y = self.position
        size = (len(grid), len(grid[0]))

        if (grid[x][y] == Agent.WALL):
            return list(ls_vision)

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
                if not (Agent.is_inside((new_x, new_y), size)):
                    break
                if (grid[new_x][new_y] == Agent.WALL):
                    # print(new_x, new_y)
                    if (i == 0):
                        flag_v = True
                    del new_flatten[0][i+1:]
                    break

            # check horizontal
            flag_h = False
            for i in range(3):
                new_x, new_y = x + new_flatten[1][i][0], y + new_flatten[1][i][1]
                if not (Agent.is_inside((new_x, new_y), size)):
                    break
                if (grid[new_x][new_y] == Agent.WALL):
                    if (i == 0):
                        flag_h = True
                    del new_flatten[1][i+1:]
                    break

            # check diagonal
            flag_d = False
            for i in range(3):
                new_x, new_y = x + new_flatten[2][i][0], y + new_flatten[2][i][1]
                if not (Agent.is_inside((new_x, new_y), size)):
                    break
                if (grid[new_x][new_y] == Agent.WALL):
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
                if (Agent.is_inside((new_x, new_y), size)):
                    if grid[new_x][new_y] == Agent.WALL:
                        del new_flatten[3][1:]
            # check HxD
            if (len(new_flatten[4]) > 0):
                new_x, new_y = x + new_flatten[4][0][0], y + new_flatten[4][0][1]
                if (Agent.is_inside((new_x, new_y), size)):
                    if grid[new_x][new_y] == Agent.WALL:
                        del new_flatten[4][1:]

            ls_vision.add((x, y))

            for sublist in new_flatten:
                for point in sublist:
                    new_x = point[0] + x
                    new_y = point[1] + y
                    if not Agent.is_inside((new_x, new_y), size) or grid[new_x][new_y] == WALL:
                        continue
                    ls_vision.add((new_x, new_y))

        return list(ls_vision)
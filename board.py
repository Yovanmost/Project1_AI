from Agent import Agent
from Seeker import Seeker
from Hider import Hider

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0
VISION = 5

class Board:
    def __init__(self, size, grid, obstacles):
        self.size = size # size[0] = N, size[1] = M
        self.grid = grid # NxM matrix
        self.obstacles = obstacles # list of (upper left, bottom right) pos
        self.hider = self.findHider()
        self.seeker = self.findSeeker()
        self.fillObstacle()

    # init hider
    def findHider(self):
        hiderPos = 0,0
        listHider = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] == HIDER:
                    hiderPos = i, j
                    listHider.append(Hider(hiderPos))
        return listHider

    # init seeker
    def findSeeker(self):
        seekerPos = 0,0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] == SEEKER:
                    seekerPos = i, j
        seeker = Seeker(seekerPos)
        return seeker

    def fillObstacle(self):
        for obstacle in self.obstacles:
            for x in range(obstacle[0], obstacle[2]+1):
                for y in range(obstacle[1], obstacle[3]+1):
                    self.grid[x][y] = WALL

    def printBroad(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if (j % self.size[1] == 0 and i != 0):
                    print()
                print(self.grid[i][j], end=" ")

    
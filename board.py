from Agent import Agent
from Seeker import Seeker
from Hider import Hider

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0

class Cell:
    def __init__(self, pos, state, value):
        self.pos = pos
        self.state = state
        self.value = value

class Board:
    def __init__(self, size, grid, obstacles):
        self.size = size # size[0] = N, size[1] = M
        self.grid = grid # NxM matrix
        self.obstacles = obstacles # list of (upper left, bottom right) pos
        self.hider = self.findHider()
        self.seeker = self.findSeeker()

    # init hider
    def findHider(self):
        hiderPos = 0,0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] == HIDER:
                    hiderPos = i, j
        hider = Hider(hiderPos)
        return hider

    # init seeker
    def findSeeker(self):
        seekerPos = 0,0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] == SEEKER:
                    seekerPos = i, j
        seeker = Seeker(seekerPos)
        return seeker

    def isFound(self):
        # newest pos comparison
        return self.seeker.position == self.hider.position


    def printBroad(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if (j % self.size[1] == 0 and i != 0):
                    print()
                print(self.grid[i][j], end=" ")

    # update board based on seeker vison(?)
    def updateBoard(self, listVision):
        seekerPos = self.seeker.position
        print(seekerPos)
        newGrid = self.grid.copy()
        for k in range(len(listVision)):
            if not (Agent.is_inside((seekerPos[0] + listVision[k][0], seekerPos[1] + listVision[k][1]), self.size)):
                continue
            if newGrid[seekerPos[0] + listVision[k][0]][seekerPos[1] + listVision[k][1]] == 1:
                continue
            newGrid[seekerPos[0] + listVision[k][0]][seekerPos[1] + listVision[k][1]] = 5
        return newGrid
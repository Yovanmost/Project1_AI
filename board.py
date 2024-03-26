import random

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0

class Hider:
    def __init__(self, pos):
        self.pos = pos

    def announcePos(self):
        # scan the whole 3x3 surrounding
        # add all free space into a list for random
        # pick one and send a signal(?)
        pass

class Cell:
    def __init__(self, pos, state, value):
        self.pos = pos
        self.state = state
        self.value = value

class Board:
    def __init__(self, size, grid, obstacle):
        self.size = size # size[0] = N, size[1] = M
        self.grid = grid # NxM matrix
        self.obstacle = obstacle # list of (upper left, bottom right) pos

    # find pos hider
    def findHider(self):
        hiderPos = 0,0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] == HIDER:
                    hiderPos = i, j
        return hiderPos

    # find pos seeker
    def findSeeker(self):
        seekerPos = 0,0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.grid[i][j] == SEEKER:
                    seekerPos = i, j
        return seekerPos

    def printBroad(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if (j % self.size[1] == 0 and i != 0):
                    print()
                print(self.grid[i][j], end=" ")

testSize = 3, 3
testGrid = [[3, 0, 0],
            [0, 0, 1],
            [2, 0, 0]]
testObstacle = [((1, 0), (1, 0))]
testBoard = Board(testSize, testGrid, testObstacle)
testBoard.printBroad()
print()
print(testBoard.findHider())
print(testBoard.findSeeker())
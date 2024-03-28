# This will test all the functions
# How frontend interact with the backend

import frontend as fe
import board as bd

size = 7, 7
grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 0, 0, 0],
    ]
obstacles = [((1, 0), (1, 0))]
testBoard = bd.Board(size, grid, obstacles)

# # before update seeker vision
# fe.createFrontEnd(testBoard.grid, testBoard.size)

# # find seeker vision
# seekerVision = testBoard.seeker.vision(testBoard.grid)

# # update the vision
# testBoard.updateBoard(testBoard.seeker.position, seekerVision)

# # show the updated grid
# fe.createFrontEnd(testBoard.grid, testBoard.size)

# # find hider vision
# hiderVision = testBoard.hider.vision(testBoard.grid)

# # update hider vision
# testBoard.updateBoard(testBoard.hider.position, hiderVision)

# fe.createFrontEnd(testBoard.grid, testBoard.size)

testBoard.addAnnounce()
fe.createFrontEnd(testBoard.grid, testBoard.size)
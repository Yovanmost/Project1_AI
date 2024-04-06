# This will test all the functions
# How frontend interact with the backend

import frontend as fe
import board as bd
from inputMap import readInputFile
import Render as rd
import Solve

FILE_NAME = "mapVer7.txt"

def test1():
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
    obstacles = [((1, 0), (1, 0))] # fix later
    testBoard = bd.Board(size, grid, obstacles)

    # before update seeker vision
    fe.createFrontEnd(testBoard.grid, testBoard.size, [])

    # find seeker vision
    seekerVision = testBoard.seeker.vision(testBoard.grid)

    # update the vision

    # show the updated grid
    fe.createFrontEnd(testBoard.grid, testBoard.size, seekerVision)

    # # find hider vision
    # hiderVision = testBoard.hider.vision(testBoard.grid)

    # # update hider vision
    # testBoard.updateBoard(testBoard.hider.position, hiderVision)

    # fe.createFrontEnd(testBoard.grid, testBoard.size)

    testBoard.addAnnounce()
    fe.createFrontEnd(testBoard.grid, testBoard.size)

def test2():
    N, M, board, obstacle = readInputFile("map1_1.txt")
    testBoard = bd.Board((N, M), board, obstacle)
    testBoard.printBroad()
    print(testBoard.seeker.position)
    seekerVision = testBoard.seeker.vision(testBoard.grid)
    fe.createFrontEnd(testBoard.grid, testBoard.size, seekerVision)

def test3():
    N, M, board, obstacle = readInputFile("map1_1.txt")
    testBoard = bd.Board((N, M), board, obstacle)
    frontEnd = rd.Render(testBoard)
    frontEnd.render()

def testFinal():
    game = Solve.Solve(FILE_NAME)
    # game.playLevel1and2()
    game.playLevel3()

testFinal()
import board as bd
from Algorithm import Algorithm as algo
import inputMap as im
import Render as rd
import Render2 as rd2
from time import sleep
import copy
import Info

def createHidersPos(hiders):
    newList = []
    for hider in hiders:
        newList.append(hider.position)
    return newList


def test1():
    N, M, board, obstacle = im.readInputFile("map1_1.txt")
    testBoard = bd.Board((N, M), board, obstacle)
    time = 10000
    cntHider = len(testBoard.hider)
    listSeen = set()
    # while cntHider > 0:
    seeker = testBoard.seeker
    hiders = testBoard.hider.copy()
    grid = testBoard.grid.copy()
    testBoard.printBroad()
    print()
    size = (N, M)
    list = []
    i = 0
    listAnnounce = []
    path = []
    historyPath = []

    flagToHider = False
    flagAnnounce = False
    flagPath = False

    history = []

    while True:
        # if seeker is on the same position as hider => remove hider from list
        for index, hider in enumerate(hiders):
            if seeker.position == hider.position:
                del hiders[index]
                del listAnnounce[index]
                flagToHider = False

        # no more hider => end
        if len(hiders) == 0:
            break

        # the Seeker looks around
        current_vision = algo.observe(seeker.position, grid, size)
        listSeen.update(current_vision)

        # New announce every 5 steps
        if i % 5 == 0 and i != 0:
            tmpList = []
            for index, hider in enumerate(hiders):
                tmpList.append(hider.announce(grid))
                print("announce")
            listAnnounce = tmpList.copy()

        # if the seeker see the hider => find the shortest path to the hider
        for hider in hiders:
            if hider.position in listSeen and flagToHider == False:
                path = algo.Search_shorted_path(seeker.position, hider.position, grid, size)
                cnt = 1
                flagToHider = True
                flagPath = False
                flagAnnounce = False
                print("path hider")
                break

        # if the seeker see the announce => look around the announce
        for a in listAnnounce:
            if a in current_vision and flagToHider == False and flagAnnounce == False:
                path = algo.Search_priority(seeker.position, grid, size, listSeen, 2, algo.find_list_priority(a, grid, size))
                cnt = 1
                flagAnnounce = True
                flagPath = False
                print("path announce")
                break

        # initial path
        if flagPath == False and flagToHider == False and flagAnnounce == False:
            path = algo.Search(seeker.position, grid, size, listSeen, 1)
            cnt = 1
            flagPath = True

        # Move the seeker along the new path
        if cnt < len(path):
            seeker.position = path[cnt]
            cnt+=1
            historyPath.append(seeker.position)
            # print(seeker.position)
        if cnt >= len(path):
            flagPath = False
        i+=1
        print(seeker.position)     
    renderer = rd.Render(testBoard)
    renderer.renderPath(historyPath)	

def is_loop(listPathSeekerHider, currSeekerPos, currHiderPos):
    return (currSeekerPos, currHiderPos) in listPathSeekerHider

def test3():
    N, M, board, obstacle = im.readInputFile("map1_1.txt")
    testBoard = bd.Board((N, M), board, obstacle)
    time = 10000
    cntHider = len(testBoard.hider)
    listSeen = set()
    # while cntHider > 0:
    seeker = testBoard.seeker
    hiders = testBoard.hider.copy()
    grid = testBoard.grid.copy()
    testBoard.printBroad()
    print()
    size = (N, M)
    list = []
    i = 0
    listAnnounce = []
    path = []
    historyPath = []
    history = []

    flagAnnounce = False
    flagPath = False
    flagChase = False
    newGrid = algo.make_priority_grid(copy.deepcopy(grid), size)

    while True:
        history.append(Info.GameInfo(seeker.position, createHidersPos(hiders.copy()), listAnnounce.copy()))
        print("Seeker: ", seeker.position)
        print("Hiders list: ", createHidersPos(hiders))
        print("Announce list: ", listAnnounce)
        # if seeker is on the same position as hider => remove hider from list
        for index, hider in enumerate(hiders):
            if seeker.position == hider.position:
                print("Caught: ", hider.position)
                del hiders[index]
                del listAnnounce[index]
                flagChase = False

        # no more hider => end
        if len(hiders) == 0:
            break

        # the Seeker looks around
        current_vision = algo.observe(seeker.position, grid, size)
        listSeen.update(current_vision)

        # New announce every 5 steps
        if i % 5 == 0 and i != 0:
            tmpList = []
            for index, hider in enumerate(hiders):
                tmpList.append(hider.announce(grid))
                print("announce")
            listAnnounce = tmpList.copy()

        # if the hider see seeker and that hider is not being chased => move away from seeker
        for hider in hiders:
            # if hider.chased == True:
            #     continue
            if seeker.position in hider.vision(grid):
                hiderMove = algo.predict_move_hider(hider.position, seeker.position,
                                                    newGrid, size, createHidersPos(hiders))
                if hiderMove:
                    hider.position = hiderMove[0]

        # find the first hider to chase
        for hider in hiders:
            if flagChase == False and hider.chased == False and hider.position in seeker.vision(grid):
                flagChase = True
                flagPath = False
                flagAnnounce = False
                hider.chased = True
                chasedHider = hider
                listPathSeekerHider = []
                path = []

        # start chasing
        if flagChase == True:
            # hiderMove = algo.predict_move_hider(chasedHider.position, seeker.position,
            #                                      newGrid, size, createHidersPos(hiders))
            # if hiderMove:
            #     chasedHider.position = hiderMove[0]

            seekerMove = algo.predict_move_seeker(seeker.position, chasedHider.position,
                                                   newGrid, size, createHidersPos(hiders))
            if seekerMove:
                seeker.position = seekerMove[0]

            if is_loop(listPathSeekerHider, seeker.position, chasedHider.position):
                print("In loop: ")
                print(listPathSeekerHider)
                break
            print("Debug: List hider: ", createHidersPos(hiders))
            print("Debug: Seeker: ", seeker.position)
            print("Debug: Chased one: ", chasedHider.position)
            listPathSeekerHider.append((seeker.position, chasedHider.position))

        # if the seeker see the announce => look around the announce
        for a in listAnnounce:
            if a in current_vision and flagChase == False and flagAnnounce == False:
                path = algo.Search_priority(seeker.position, grid, size, listSeen, 2, algo.find_list_priority(a, grid, size))
                if len(path) == 1:
                    listSeen = set()
                    path = algo.Search_priority(seeker.position, grid, size, listSeen, 2, algo.find_list_priority(a, grid, size))
                cnt = 1
                flagAnnounce = True
                flagPath = False
                print("path announce")
                break

        # initial path
        if flagPath == False and flagChase == False and flagAnnounce == False:
            path = algo.Search(seeker.position, grid, size, listSeen, 1)
            if len(path) == 1:
                listSeen = set()
                path = algo.Search(seeker.position, grid, size, listSeen, 1)
            cnt = 1
            flagPath = True
            print("Debug: Path")

        # Move the seeker along the new path
        if cnt < len(path):
            seeker.position = path[cnt]
            cnt+=1
            historyPath.append(seeker.position)
            # print(seeker.position)
        if cnt >= len(path):
            flagPath = False
        i+=1

    renderer = rd2.Render(testBoard, history)
    renderer.render()
    # renderer.renderPath(historyPath)

test3()
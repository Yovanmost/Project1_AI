import board as bd
from Algorithm import Algorithm as algo
import inputMap as im
import Render as rd
from time import sleep
from Infor import*

def createHiderPos(hiders):
    list = []
    for hider in hiders:
        list.append(hider.position)
    return list

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
    
    # Danh sach lich su cac vi tri cua cac object
    list_history = []
    
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
            for hider in hiders:
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
        hidersPos = createHiderPos(hiders)
        # print("Seeker: ", seeker.position)
        # print("Hiders: ", hidersPos)
        # print("Announce: ", listAnnounce)
        list_history.append(GameInfo(seeker.position, hidersPos.copy(), listAnnounce.copy()))
        # print(seeker.position)     
    # renderer = rd.Render(testBoard)
    # renderer.renderPath(historyPath)	
    for x in list_history:
        x.printInfomationPos()

            

test1()

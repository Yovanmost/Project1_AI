import board as bd
from Algorithm import Algorithm as algo
import inputMap as im
import Render as rd

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
        listSeen.update(algo.observe(seeker.position, grid, size))

        # New announce every 5 steps
        if i % 5 == 0 and i != 0:
            tmpList = []
            for index, hider in enumerate(hiders):
                tmpList.append(hider.announce)
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
            if a in listSeen and flagToHider == False and flagAnnounce == False:
                path = algo.Search_priority(seeker.position, grid, size, listSeen, 2, algo.find_list_priority(listAnnounce[i], grid, size))
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

        i+=1
        
        print(seeker.position)

    renderer = rd.Render(testBoard)
    renderer.renderPath(historyPath)	

            
    
test1()
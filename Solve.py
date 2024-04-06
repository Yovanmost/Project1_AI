import board as bd
from Algorithm import Algorithm as algo
import inputMap as im
import Render as rd
import Render2 as rd2
from time import sleep
import copy
import Info

FILE_MAP = "mapVerSpecial.txt"

class Solve:
    def __init__(self, file_name) -> None:
        N, M, board, obstacle = im.readInputFile(file_name)
        self.testBoard = bd.Board((N, M), board, obstacle)
        time = 10000
        self.listSeen = set()
        # while cntHider > 0:
        self.seeker = self.testBoard.seeker
        self.hiders = self.testBoard.hider.copy()
        self.grid = self.testBoard.grid.copy()
        self.size = (N, M)
        self.newGrid = algo.make_priority_grid(copy.deepcopy(self.grid), self.size)
        self.step = 0
        self.listAnnounce = []
        self.path = []

        self.flagToHider = False
        self.flagAnnounce = False
        self.flagPath = False
        self.flagChase = False

        self.history = []


    def createHidersPos(self):
        newList = []
        for hider in self.hiders:
            newList.append(hider.position)
        return newList

    def is_loop(self, listPathSeekerHider, currSeekerPos, currHiderPos):
        return (currSeekerPos, currHiderPos) in listPathSeekerHider

    def removeCaught(self):
        for index, hider in enumerate(self.hiders):
            if self.seeker.position == hider.position:
                del self.hiders[index]
                del self.listAnnounce[index]
                self.flagToHider = False

    def announceHiders(self):
        if self.step % 5 == 0 and self.step != 0:
                tmpList = []
                for hider in self.hiders:
                    tmpList.append(hider.announce(self.grid))
                    # print("announce")
                self.listAnnounce = tmpList.copy()

    def findPathToHider(self, hider):
        if hider.position in self.listSeen and self.flagToHider == False:
            self.path = algo.Search_shorted_path(self.seeker.position, hider.position, self.grid, self.size)
            self.cnt = 1
            self.flagToHider = True
            self.flagPath = False
            self.flagAnnounce = False
            # print("path hider")
            return True
        return False

    def findPathToAnnounce(self, announce, current_vision):
        if announce in current_vision and self.flagToHider == False and self.flagAnnounce == False:
            self.path = algo.Search_priority(self.seeker.position, self.grid, self.size, self.listSeen, 2, algo.find_list_priority(announce, self.grid, self.size))
            if len(self.path) == 1:
                self.listSeen = set()
                self.path = algo.Search_priority(self.seeker.position, self.grid, self.size, self.listSeen, 2, algo.find_list_priority(announce, self.grid, self.size))
            self.cnt = 1
            self.flagAnnounce = True
            self.flagPath = False
            # print("path announce")
            return True
        return False

    def findPath(self):
        if self.flagPath == False and self.flagToHider == False and self.flagAnnounce == False:
            self.path = algo.Search(self.seeker.position, self.grid, self.size, self.listSeen, 2)
            if len(self.path) == 1:
                self.listSeen = set()
                self.path = algo.Search(self.seeker.position, self.grid, self.size, self.listSeen, 2)
            self.cnt = 1
            self.flagPath = True

    def moveSeeker(self):
        if self.cnt < len(self.path):
                self.seeker.position = self.path[self.cnt]
                self.cnt+=1

        if self.cnt >= len(self.path):
            self.flagPath = False
            self.flagAnnounce = False

    def debugRender(self):
        renderer = rd2.Render(self.testBoard, self.history)
        renderer.render()

    def playLevel1and2(self):
        print("Running...")
        while True:
            # Update history
            self.history.append(Info.GameInfo(self.seeker.position, self.createHidersPos(), self.listAnnounce.copy()))

            # if seeker is on the same position as hider => remove hider from list
            self.removeCaught()

            # no more hider => end
            if len(self.hiders) == 0:
                break

            # the Seeker looks around
            current_vision = algo.observe(self.seeker.position, self.grid, self.size)
            self.listSeen.update(current_vision)

            # New announce every 5 steps
            self.announceHiders()

            # if the seeker see the hider => find the shortest path to the hider
            for hider in self.hiders:
                if self.findPathToHider(hider):
                    break

            # if the seeker see the announce => look around the announce
            for announce in self.listAnnounce:
                if self.findPathToAnnounce(announce, current_vision):
                    break

            # initial path
            self.findPath()

            # Move the seeker along the new self.path
            self.moveSeeker()
            self.step+=1

        self.debugRender()

    def moveHider(self, hider):
        if self.seeker.position in hider.vision(self.grid):
            hiderMove = algo.predict_move_hider(hider.position, self.seeker.position,
                                                self.newGrid, self.size, self.createHidersPos())
            if hiderMove:
                hider.position = hiderMove[0]

    def playLevel3(self):
        while True:
            self.history.append(Info.GameInfo(self.seeker.position, self.createHidersPos(), self.listAnnounce.copy()))

            # if seeker is on the same position as hider => remove hider from list
            self.removeCaught()

            # no more hider => end
            if len(self.hiders) == 0:
                break

            # the Seeker looks around
            current_vision = algo.observe(self.seeker.position, self.grid, self.size)
            self.listSeen.update(current_vision)

            # New announce every 5 steps
            self.announceHiders()

            # if the hider see seeker => move away from seeker
            for hider in self.hiders:
                self.moveHider(hider)
            self.history.append(Info.GameInfo(self.seeker.position, self.createHidersPos(), self.listAnnounce.copy()))

            # find the first hider to chase
            for hider in self.hiders:
                if self.flagToHider == False and hider.chased == False and hider.position in self.seeker.vision(self.grid):
                    self.flagToHider = True
                    self.flagPath = False
                    self.flagAnnounce = False
                    hider.chased = True
                    chasedHider = hider
                    listPathSeekerHider = []
                    self.path = []

            # start chasing
            if self.flagToHider == True:
                seekerMove = algo.predict_move_seeker(self.seeker.position, chasedHider.position,
                                                self.newGrid, self.size, self.createHidersPos())
                if seekerMove:
                    self.seeker.position = seekerMove[0]

                if self.is_loop(listPathSeekerHider, self.seeker.position, chasedHider.position):
                    self.history.append(Info.GameInfo(self.seeker.position, self.createHidersPos(), self.listAnnounce.copy()))
                    break
                listPathSeekerHider.append((self.seeker.position, chasedHider.position))

            # if the seeker see the announce => look around the announce
            for announce in self.listAnnounce:
                if self.findPathToAnnounce(announce, current_vision):
                    break

            # initial path
            self.findPath()

            # Move the seeker along the new path
            self.moveSeeker()
            self.step += 1

        self.debugRender()
class GameInfo:
    def __init__(self, seekerPos, hidersPos, announcePos, score, step):
        self.seekerPos = seekerPos
        self.hidersPos = hidersPos
        self.announcePos = announcePos
        self.score = score
        self.step = step

    def printInfo(self):
        print ("Seeker Position:")
        print(self.seekerPos)
        print ("Hider Position:")
        print(self.hidersPos)
        print ("Announcement Position:")
        print(self.announcePos)
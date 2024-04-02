class GameInfo:
    def __init__(self, seeker_position, hider_position, announcement_positions):
        self.seeker_position = seeker_position
        self.hider_position = hider_position
        self.announcement_positions = announcement_positions

    def printInfomationPos(self):
        print ("Seeker Position:")
        print(self.seeker_position)
        print ("Hider Position:")
        print(self.hider_position)
        print ("Announcement Position:")
        print(self.announcement_positions)

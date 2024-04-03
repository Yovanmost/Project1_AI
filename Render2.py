import tkinter as tk

# Constants
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0
VISION = 5
ANNOUNCE = 6
OBSTACLE = 7

class Render:
    def __init__(self, board):
        self.board = board
        self.listAnnounce = []
        self.listHidersPos = []
        self.root = tk.Tk()
        self.root.title("Grid Example")

        # Get the size of the window
        window_width = self.root.winfo_screenwidth() // 2
        window_height = self.root.winfo_screenheight() // 2

        # Dimension
        self.rows, self.columns = self.board.size
        max_cell_width = window_width // self.columns
        max_cell_height = window_height // self.rows
        self.cell_size = min(max_cell_height, max_cell_width)

        # Create a canvas to hold the grid
        self.canvas = tk.Canvas(self.root, width=self.columns * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack(padx=10, pady=10)

    def findColor(self, value):
        if value == WALL:
            return "blue"
        if value == HIDER:
            return "red"
        if value == SEEKER:
            return "green"
        if value == PATH:
            return "white"
        if value == VISION:
            return "gray"
        if value == ANNOUNCE:
            return "purple"
        if value == OBSTACLE:
            return "yellow"

    def colorCell(self, row, column, color):
        x0 = column * self.cell_size
        y0 = row * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    def clearCanvas(self):
        self.canvas.delete("all")

    def setNewSeeker(self, seekerPos):
        self.board.seeker.position = seekerPos

    def setNewHiders(self, hiders):
        self.listHidersPos = hiders

    def setNewAnnounce(self, listAnnounce):
        self.listAnnounce = listAnnounce

    def renderBoard(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.board.grid[row][column] != PATH and self.board.grid[row][column] != WALL:
                    continue
                cell_color = self.findColor(self.board.grid[row][column])
                self.colorCell(row, column, cell_color)

    def renderObstacle(self):
        for obstacle in self.board.obstacles:
            for x in range(obstacle[0], obstacle[2]+1):
                for y in range(obstacle[1], obstacle[3]+1):
                    self.colorCell(x, y, self.findColor(OBSTACLE))

    def renderVision(self, listVision):
        for vision in listVision:
            row, column = vision
            if self.board.grid[row][column] == PATH:
                self.colorCell(row, column, self.findColor(VISION))

    def renderSeeker(self):
        seekerPos = self.board.seeker.position
        self.colorCell(seekerPos[0], seekerPos[1], self.findColor(SEEKER))

    def renderHider(self):
        # if self.board.hider.empty():
        #     pass
        for hider in self.listHidersPos:
            self.colorCell(hider[0], hider[1], self.findColor(HIDER))

    def renderAnnounce(self): # circle
        for announce in self.listAnnounce:
            self.colorCell(announce[0], announce[1], self.findColor(ANNOUNCE))

    def renderAll(self):
        self.clearCanvas()
        self.renderBoard()
        self.setNewSeeker((9,9))
        self.renderVision(self.board.seeker.vision(self.board.grid))
        self.renderSeeker()
        self.renderHider()
        self.renderObstacle()
        self.renderAnnounce()

    def render(self, history):
        create_button = tk.Button(self.root, text="End", command=self.root.destroy)
        create_button.pack()
        self.renderAll()
        # self.updateSeekerPosition(history)
        self.root.mainloop()

    # def updateSeekerPosition(self, history):
    #     self.clearCanvas()  # Clear canvas before rendering
    #     for h in history:
    #         self.setNewSeeker(h.seekerPos)
    #         self.setNewHiders(h.hidersPos)
    #         self.setNewAnnounce(h.announcePos)
    #         self.renderAll()
    #         self.root.after(10000, self.updateSeekerPosition)  # Schedule the update
    #         # self.root.mainloop()
    def updateSeekerPosition(self, history, index=0):
        if index < len(history):
            # Get the next state from history
            state = history[index]
            self.setNewSeeker(state.seekerPos)
            self.setNewHiders(state.hidersPos)
            self.setNewAnnounce(state.announcePos)
            self.renderAll()
            # self.renderSeeker()
            # self.renderVision(self.board.seeker.vision(self.board.grid))
            # self.renderHider()
            # Schedule the update for the next state
            self.root.after(1000, self.updateSeekerPosition, history, index + 1)

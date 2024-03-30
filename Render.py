import tkinter as tk
from board import Board

# CONSTANT
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

        # Create a frame to hold the grid
        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

    def findColor(self, value):
        if value == WALL:
            return "wall", "blue"
        if value == HIDER:
            return "hider", "red"
        if value == SEEKER:
            return "seeker", "green"
        if value == PATH:
            return "path", "white"
        if value == VISION:
            return "see", "gray"
        if value == ANNOUNCE:
            return "signal", "purple"
        if value == OBSTACLE:
            return "obstacle", "yellow"

    def colorCell(self, cell, row, column):
        tk.Label(self.frame, borderwidth=1, relief='solid',
                        width=self.cell_size // 10, height=self.cell_size // 15,
                        bg=cell[1]).grid(row=row, column=column)

    def renderBoard(self):
        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.findColor(self.board.grid[row][column])
                if self.board.grid[row][column] != WALL and self.board.grid[row][column] != PATH :
                    continue
                self.colorCell(cell, row, column)

    def renderObstacle(self):
        for obstacle in self.board.obstacles:
            for x in range(obstacle[0], obstacle[2]):
                for y in range(obstacle[1], obstacle[3]):
                    cell = self.findColor(OBSTACLE)
                    self.colorCell(cell, x, y)

    def renderVision(self, listVision):
        for vision in listVision:
            row, column = vision
            cell = self.findColor(VISION)
            if self.board.grid[row][column] != PATH:
                continue
            self.colorCell(cell, row, column)

    def renderSeeker(self):
        cell = self.findColor(SEEKER)
        seekerPos = (self.board.seeker.position[0], self.board.seeker.position[1])
        self.colorCell(cell, seekerPos[0], seekerPos[1])

    def renderHider(self):
        cell = self.findColor(HIDER)
        hiders = self.board.hider
        for hider in hiders:
            hiderPos = (hider.position[0], hider.position[1])
            self.colorCell(cell, hiderPos[0], hiderPos[1])

    def renderAnnounce(self): # circle
        cell = self.findColor(ANNOUNCE)
        hiders = self.board.hider
        for hider in hiders:
            announcePos = hider.announce(self.board.grid)
            self.colorCell(cell, announcePos[0], announcePos[1])

    def renderAll(self):
        self.renderBoard()
        self.renderSeeker()
        self.renderVision(self.board.seeker.vision(self.board.grid))
        self.renderHider()
        self.renderObstacle()
        self.renderAnnounce()

    def render(self):
        create_button = tk.Button(self.root, text="End", command=self.root.destroy)
        create_button.pack()
        self.renderAll()
        self.root.mainloop()
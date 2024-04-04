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
        center_x = (x0 + x1) // 2
        center_y = (y0 + y1) // 2
        self.canvas.create_text(center_x, center_y, text=f"({row}, {column})", fill="black")

    def clearCanvas(self):
        self.canvas.delete("all")

    def renderBoard(self):
        for row in range(self.rows):
            for column in range(self.columns):
                cell_color = self.findColor(self.board.grid[row][column])
                self.colorCell(row, column, cell_color)

    def renderObstacle(self):
        for obstacle in self.board.obstacles:
            for x in range(obstacle[0], obstacle[2]):
                for y in range(obstacle[1], obstacle[3]):
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
        for hider in self.board.hider:
            hiderPos = hider.position
            self.colorCell(hiderPos[0], hiderPos[1], self.findColor(HIDER))

    def renderAnnounce(self): # circle
        for hider in self.board.hider:
            announcePos = hider.announce(self.board.grid)
            self.colorCell(announcePos[0], announcePos[1], self.findColor(ANNOUNCE))

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
        self.updateSeekerPosition()
        self.root.mainloop()

    def updateSeekerPosition(self):
        self.clearCanvas()  # Clear canvas before rendering
        self.renderAll()
        self.root.after(1000, self.updateSeekerPosition)  # Schedule the update

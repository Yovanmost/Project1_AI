import tkinter as tk
# pip install Pillow
from PIL import Image, ImageTk
import time
import Hider

# Constants
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0
VISION = 5
ANNOUNCE = 6
OBSTACLE = 7
CAUGHT = 8
VISION_HIDER = 9
SAME_VISION = 10

class Render:
    def __init__(self, board, history):
        self.board = board
        self.history = history
        self.listAnnounce = []
        self.listHidersPos = []
        self.root = tk.Tk()
        self.root.title("Grid Example")

        

        # Get the size of the window
        window_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_screenheight()

        # Dimension
        self.rows, self.columns = self.board.size
        max_cell_width = window_width // self.columns - 5
        max_cell_height = window_height // self.rows - 5
        self.cell_size = min(max_cell_height, max_cell_width)


        # Create a canvas to hold the grid
        self.canvas = tk.Canvas(self.root, width=self.columns * self.cell_size + 20, height=self.rows * self.cell_size + 20)
        self.canvas.pack(padx=5, pady=5)

        # Button variables
        self.is_paused = False
        self.pause_button = None
        self.end_button = None
        self.update_index = 0
        #self.create_buttons()

        # Load image for wall
        self.wall_image = self.loadImage(r"Photo/wall.png")

        # Load image for Hiders
        self.hider_image = self.loadImage(r"Photo/hider.png") 

        # Load image for Seeker
        self.seeker_image = self.loadImage(r"Photo/Seeker.png") 

        # Load image for Path
        self.path_image = self.loadImage(r"Photo/path2.png") 

        # Load image for Vision 
        self.vision_image = self.loadImage(r"Photo/vision.png") 

        # Load image for Annoucements
        self.announce_image = self.loadImage(r"Photo/Annouce.png")

        # Load image for Obstacles
        self.obstacle_image = self.loadImage(r"Photo/object.png") 

        # Load image for caught event
        self.caught_image = self.loadImage(r"Photo/caught.png") 

    def loadImage(self, filePath):
        pil_image = Image.open(filePath) 
        image = pil_image.resize((self.cell_size, self.cell_size), Image.LANCZOS)
        return ImageTk.PhotoImage(image)


    def colorCell(self, row, column, value):
        x0 = column * self.cell_size
        y0 = row * self.cell_size
        x1 = x0 + self.cell_size
        y1 = y0 + self.cell_size

        # Xác định hình ảnh cho từng giá trị
        image = None
        if value == WALL:
            image = self.wall_image
        elif value == HIDER:
            image = self.hider_image
        elif value == SEEKER:
            image = self.seeker_image
        elif value == PATH:
            image = self.path_image
        elif value == VISION:
            image = 1
        elif value == VISION_HIDER:
            image = 2
        elif value == SAME_VISION:
            image = 3
        elif value == ANNOUNCE:
            image = self.announce_image
        elif value == OBSTACLE:
            image = self.obstacle_image
        elif value == CAUGHT:
            image = self.caught_image


        # Vẽ hình ảnh tại vị trí được chỉ định
        if image == 1 :
            self.drawObject(x0, y0, x1, y1, "gray")
        elif image == 2:
            self.drawObject(x0, y0, x1, y1, "orange")
        elif image == 3:
            self.drawObject(x0, y0, x1, y1, "yellow")
        else : self.canvas.create_image(x0, y0, image=image, anchor="nw")

    # Function draw vision graphic
    def drawObject(self, x0, y0, x1, y1, color):
        # Draw rectangle
        rectangle = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

        # Tạo màu trong suốt với alpha là 75%
        self.canvas.itemconfig(rectangle, fill=color, stipple="gray75")
    # Remove object after moving
    def clearCanvas(self):
        self.canvas.delete("all")

    def setNewSeeker(self, seekerPos):
        self.board.seeker.position = seekerPos

    def setNewHiders(self, hiders):
        self.listHidersPos = hiders

    def setNewAnnounce(self, listAnnounce):
        self.listAnnounce = listAnnounce

    def renderCaught(self):
        seekerPos = self.board.seeker.position
        for hider in self.listHidersPos:
            if seekerPos == hider:
                self.colorCell(seekerPos[0], seekerPos[1], CAUGHT)
                return True
        return False

    def renderBoard(self):
        for row in range(self.rows):
            for column in range(self.columns):
                self.colorCell(row, column, self.board.grid[row][column])
                if self.board.grid[row][column] != PATH and self.board.grid[row][column] != WALL:
                    self.colorCell(row, column, PATH)

    def renderObstacle(self):
        for obstacle in self.board.obstacles:
            for x in range(obstacle[0], obstacle[2]+1):
                for y in range(obstacle[1], obstacle[3]+1):
                    self.colorCell(x, y, OBSTACLE)            

    def renderVision(self, listVision):
        for vision in listVision:
            row, column = vision
            if self.board.grid[row][column] != WALL:
                self.colorCell(row, column, VISION)
    
    def renderHiderVision(self, listVision):
        for vision in listVision:
            row, column = vision
            if self.board.grid[row][column] != WALL:
                self.colorCell(row, column, VISION_HIDER)

    def renderSameVision(self, listSeekerVision, listHiderVision):
        listSamePos = []
        for hiderVision in listHiderVision:
            for seekerVision in listSeekerVision:
                if hiderVision == seekerVision:
                    listSamePos.append(hiderVision)
        for vision in listSamePos:
            self.colorCell(vision[0], vision[1], SAME_VISION)

    def renderSeeker(self):
        seekerPos = self.board.seeker.position
        self.colorCell(seekerPos[0], seekerPos[1], SEEKER)

    def renderHider(self):
        for hider in self.listHidersPos:
            self.colorCell(hider[0], hider[1], HIDER)

    def renderAnnounce(self): # circle
        for announce in self.listAnnounce:
            self.colorCell(announce[0], announce[1], ANNOUNCE)

    def renderAll(self):
        self.clearCanvas()
        self.renderBoard()
        self.renderVision(self.board.seeker.vision(self.board.grid))
        listHiderVision = []
        for hider in self.listHidersPos:
            tmp_hider = Hider.Hider(hider)
            hiderVision = tmp_hider.vision(self.board.grid)
            self.renderHiderVision(hiderVision)
            for vison in hiderVision:
                listHiderVision.append(vison)

        self.renderAnnounce()
        self.renderSameVision(self.board.seeker.vision(self.board.grid), listHiderVision)
        self.renderSeeker()
        self.renderHider()
        self.renderCaught()
        self.renderObstacle()

    def create_buttons(self):
        self.pause_button = tk.Button(self.root, text="Pause", command=self.handle_pause)
        self.pause_button.place(x = (self.cell_size * self.columns) // 2, y = (self.cell_size * self.rows) // 2)
        self.end_button = tk.Button(self.root, text="End", command=self.root.destroy)
        self.end_button.place(x = self.cell_size + 5, y = self.cell_size * (self.columns - 2))

        
        self.pause_button.pack()
        self.end_button.pack()

    def handle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")
            self.update(index=self.update_index)

    def update(self, index=0):
        if not self.is_paused and index < len(self.history):
            state = self.history[index]
            self.setNewSeeker(state.seekerPos)
            self.setNewHiders(state.hidersPos)
            self.setNewAnnounce(state.announcePos)
            self.renderAll()
            Time = 250
            if self.renderCaught():
               Time = 500

            self.canvas.create_text(10, self.rows * self.cell_size - 10, anchor="sw", text="Time: " + str(state.step), fill="black")
            self.canvas.create_text(10, self.rows * self.cell_size - 30, anchor="sw", text="Score: " + str(state.score), fill="black")
            self.create_buttons()
            self.root.after(Time, self.update, index + 1)
            self.update_index = index


            

    def render(self):
        self.renderAll()
        self.update()
        self.root.mainloop()

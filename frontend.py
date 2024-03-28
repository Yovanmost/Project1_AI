import tkinter as tk
import testVision2 as tv2

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0
VISION = 5
ANNOUNCE = 6

def colorCell(value):
    if value == WALL:
        return "wall", "blue"
    if value == HIDER:
        return "Hider", "red"
    if value == SEEKER:
        return "seeker", "green"
    if value == PATH:
        return "path", "white"
    if value == VISION:
        return "see", "gray"
    if value == ANNOUNCE:
        return "signal", "purple"

def createGrid(frame, grid, size):
    rows = size[0]
    columns = size[1]
    # Clear previous grid
    for widget in frame.winfo_children():
        widget.destroy()

    # Create new grid
    for row in range(rows):
        for column in range(columns):
            # Calculate color based on position
            cell = colorCell(grid[row][column])
            tk.Label(frame, text=cell[0].format(row+1, column+1), borderwidth=1, relief='solid', width=9, height=4, bg=cell[1]).grid(row=row, column=column)

def createFrontEnd(grid, size):
    root = tk.Tk()
    root.title("Grid Example")

    # Create a frame to hold the grid
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Button to create grid
    create_button = tk.Button(root, text="End", command=root.destroy)
    create_button.pack()
    createGrid(frame, grid, size)

    root.mainloop()
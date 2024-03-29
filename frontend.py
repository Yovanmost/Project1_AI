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

def createGrid(frame, grid, size, listVision, window_size):
    rows = size[0]
    columns = size[1]
    window_width, window_height = window_size

    # Clear previous grid
    for widget in frame.winfo_children():
        widget.destroy()

    # Calculate the maximum width and height of a cell
    max_cell_width = window_width // columns
    max_cell_height = window_height // rows

    # Take the minimum of the two as the size for each cell
    cell_size = min(max_cell_width, max_cell_height)

    # Create new grid: color seeker, hider, wall
    for row in range(rows):
        for column in range(columns):
            cell = colorCell(grid[row][column])
            tk.Label(frame, borderwidth=1, relief='solid', width=cell_size // 10, height=cell_size // 15, bg=cell[1]).grid(row=row, column=column)

    # color vision(list)
    for point in listVision:
        row = point[0]
        column = point[1]
        if grid[row][column] != PATH:
            continue
        cell = colorCell(VISION)
        tk.Label(frame, borderwidth=1, relief='solid', width=cell_size // 10, height=cell_size // 15, bg=cell[1]).grid(row=row, column=column)

def createFrontEnd(grid, size, vision):
    root = tk.Tk()
    root.title("Grid Example")

    # Get the size of the window
    window_width = root.winfo_screenwidth() // 2
    window_height = root.winfo_screenheight() // 2

    # Create a frame to hold the grid
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Button to create grid
    create_button = tk.Button(root, text="End", command=root.destroy)
    create_button.pack()
    createGrid(frame, grid, size, vision, (window_width, window_height))

    root.mainloop()
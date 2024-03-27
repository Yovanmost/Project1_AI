import tkinter as tk
import testVision2 as tv2

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0
VISION = 5

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

class Board:
    def __init__(self):
        pass


def create_grid(grid, size):
    # global rows, columns
    # try:
    #     rows = int(row_entry.get())
    #     columns = int(column_entry.get())
    # except ValueError:
    #     return

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

root = tk.Tk()
root.title("Grid Example")

# Create a frame to hold the grid
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# # Label and entry for row count
# row_label = tk.Label(root, text="Rows:")
# row_label.pack()
# row_entry = tk.Entry(root)
# row_entry.pack()

# # Label and entry for column count
# column_label = tk.Label(root, text="Columns:")
# column_label.pack()
# column_entry = tk.Entry(root)
# column_entry.pack()

data = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
size = 7, 7
pos = tv2.findSeeker(data, size)

vision = tv2.observe(pos, data, size)

newData = tv2.redrawGrid(data, size, pos, vision)


# Button to create grid
# create_button = tk.Button(root, text="Create Grid", command=create_grid(testGrid, testSize))
# create_button.pack()
create_grid(newData, size)

root.mainloop()

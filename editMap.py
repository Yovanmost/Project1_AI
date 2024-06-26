import tkinter as tk
from tkinter import messagebox

# Define
PATH = 0
WALL = 1
HIDER = 2
SEEKER = 3
OBS = 4 # obstacle

# Color
PATH_COLOR = 'white'
WALL_COLOR = 'black'
HIDER_COLOR = 'green'
SEEKER_COLOR = 'blue'
OBS_COLOR = 'yellow'

# Button
BUTTON_HEIGHT = 2
BUTTON_WIDTH = 4

# Render Map Editor App
class MapEditorApp:
    def __init__(self, root, map_data, map_size_n, map_size_m, filename):
        self.root = root
        self.map_data = map_data
        self.map_size_n = map_size_n
        self.map_size_m = map_size_m
        self.filename = filename

        self.create_widgets()

    def create_widgets(self):
        self.buttons = []
        for i in range(self.map_size_n):
            row_buttons = []
            for j in range(self.map_size_m):
                button = tk.Button(self.root, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                   command=lambda i=i, j=j: self.toggle_cell(i, j))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        ok_button = tk.Button(self.root, text="OK", command=self.save_map)
        ok_button.grid(row=self.map_size_n, columnspan=self.map_size_m)

        self.render_map()

    def toggle_cell(self, i, j):
        if self.map_data[i][j] == PATH:
            self.map_data[i][j] = WALL
        else:
            self.map_data[i][j] = PATH
        self.render_map()

    def render_map(self):
        for i in range(self.map_size_n):
            for j in range(self.map_size_m):
                cell_value = self.map_data[i][j]
                cell_text = f"{i},{j}"
                if cell_value == PATH:
                    bg_color = PATH_COLOR
                else:
                    bg_color = WALL_COLOR

                self.buttons[i][j].configure(text=cell_text, bg=bg_color)

    def save_map(self):
        try:
            with open(self.filename, 'w') as file:
                file.write(f"{self.map_size_n} {self.map_size_m}\n")
                for row in self.map_data:
                    file.write(' '.join(str(cell) for cell in row) + '\n')
            messagebox.showinfo("Saved", "Map saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the map: {str(e)}")

def read_map_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        map_size_n, map_size_m = map(int, lines[0].split())
        map_data = [[int(cell) for cell in line.split()] for line in lines[1:]]

    return map_data, map_size_n, map_size_m

def main():
    filename = "mapVer11.txt" # FILE_NAME
    map_data, map_size_n, map_size_m = read_map_from_file(filename)

    root = tk.Tk()
    root.title("Map Editor") 
    app = MapEditorApp(root, map_data, map_size_n, map_size_m, filename)
    root.mainloop()

main()

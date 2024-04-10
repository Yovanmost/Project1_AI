import tkinter as tk

class MenuInterface:
    def __init__(self, master):
        self.master = master
        master.title("HIDER & SEEKER")

        # Window size
        window_width = 1280
        window_height = 720

        # Menu size
        menu_width = 800
        menu_height = 400

        # Menu position
        menu_x = (window_width - menu_width) / 2
        menu_y = (window_height - menu_height) / 2

        master.geometry(f"{window_width}x{window_height}+{0}+{0}")

        self.menu_frame = tk.Frame(master, bg="lightblue")
        self.menu_frame.place(relx=0.5, rely=0.5, anchor="center", width=menu_width, height=menu_height)

        self.level = tk.StringVar()
        self.map = tk.StringVar()

        self.canvas = tk.Canvas(self.menu_frame, width=menu_width, height=100, bg="lightblue")
        self.canvas.grid(row=0, column=0, columnspan=2, pady=20)
        self.canvas.create_text(menu_width / 2, 50, text="HIDER & SEEKER", font=("Arial", 40, "bold"), fill="black", anchor="center")

        self.level_label = tk.Label(self.menu_frame, text="LEVEL:", font=("Arial", 24), bg="lightblue")
        self.level_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.level_options = tk.OptionMenu(self.menu_frame, self.level, "1", "2", "3")
        self.level_options.config(font=("Arial", 24), width=15)  
        self.level_options.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.map_label = tk.Label(self.menu_frame, text="MAP:", font=("Arial", 24), bg="lightblue")
        self.map_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.map_options = tk.OptionMenu(self.menu_frame, self.map, "")
        self.map_options.config(font=("Arial", 24), width=15)  
        self.map_options.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.start_button = tk.Button(self.menu_frame, text="START", font=("Arial", 28, "bold"), command=self.start_program)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.exit_button = tk.Button(self.menu_frame, text="EXIT ", font=("Arial", 28, "bold"), command=self.exit_program)
        self.exit_button.grid(row=3, column=1, columnspan=2, pady=20)
        
        self.level.trace('w', self.update_map_options)

        self.selected_level = None
        self.selected_map = None

    def update_map_options(self, *args):
        level = self.level.get()
        maps = self.get_maps_for_level(level)
        menu = self.map_options["menu"]
        menu.delete(0, "end")
        for map in maps:
            menu.add_command(label=map, command=lambda value=map: self.map.set(value))
        self.map.set("")

    def get_maps_for_level(self, level):
        if level == "1":
            return ["SingleHiderVer1", "SingleHiderVer2"]
        else:
            return ["SingleHiderVer1", "SingleHiderVer2", "MultiHidersVer0", "MultiHidersVer1", "MultiHidersVer2", "MultiHidersVer3", "MultiHidersVer4", "MultiHidersVer5", "MultiHidersVer6", "MultiHidersVer7", "MultiHidersVerSpecial"]

    def start_program(self):
        selected_level = self.level.get()
        selected_map = self.map.get()
        if selected_level and selected_map:
            self.selected_level = selected_level
            self.selected_map = "Map/" + selected_map + ".txt"
            self.master.quit()

    def exit_program(self):
        self.master.destroy()

def start_game():
    root = tk.Tk()

    menu_interface = MenuInterface(root)
    root.mainloop()
    root.destroy()
    return menu_interface.selected_level, menu_interface.selected_map


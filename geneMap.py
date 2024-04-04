
import tkinter as tk
from tkinter import ttk

import random

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0

def tao_map(n):
  """
  Hàm tạo bản đồ trò chơi trốn tìm

  Tham số:
    n: Kích thước ma trận (n x n)

  Trả về:
    map: Ma trận 2 chiều chứa bản đồ trò chơi
  """
  # Khởi tạo map
  map = [[WALL for _ in range(n)] for _ in range(n)]

  # Tạo đường đi
  for i in range(1, n - 1):
    for j in range(1, n - 1):
      if random.random() < 0.85:
        map[i][j] = PATH



  # Xử lý trường hợp 2 ô WALL liền kề
  for i in range(1, n - 1):
    for j in range(1, n - 1):
      if map[i][j] == WALL and map[i - 1][j - 1] == WALL and map[i][j - 1] == PATH and map[i - 1][j] == PATH:
        # Xóa 2 ô WALL
        map[i][j] = PATH
        map[i - 1][j - 1] = PATH
      if map[i][j] == WALL and map[i + 1][j + 1] == WALL and map[i][j + 1] == PATH and map[i + 1][j + 1] == PATH:
        # Xóa 2 ô WALL
        map[i][j] = PATH
        map[i + 1][j + 1] = PATH
      if map[i][j] == WALL and map[i + 1][j - 1] == WALL and map[i][j - 1] == PATH and map[i + 1][j] == PATH:
        # Xóa 2 ô WALL
        map[i][j] = PATH
        map[i + 1][j - 1] = PATH

  return map

def xuat_file_txt(map, n):
  with open("map.txt", "w") as f:
    f.write(str(n))
    f.write("\n")
    for i in range(n):
      for j in range(n):
        f.write(str(map[i][j]))
      f.write("\n")


def hien_thi_map(map, n):
  """
  Hàm hiển thị bản đồ trò chơi trốn tìm

  Tham số:
    map: Ma trận 2 chiều chứa bản đồ trò chơi
    n: Kích thước ma trận (n x n)
  """
  # Tạo cửa sổ
  root = tk.Tk()
  root.title("Bản đồ trò chơi trốn tìm")

  # Tạo canvas
  canvas = tk.Canvas(root, width=n * 20, height=n * 20)
  canvas.pack()

  # Vẽ các ô
  for i in range(n):
    for j in range(n):
      if map[i][j] == WALL:
        canvas.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="black")
      elif map[i][j] == PATH:
        canvas.create_rectangle(i * 20, j * 20, (i + 1) * 20, (j + 1) * 20, fill="white")

  # Khởi động vòng lặp chính
  root.mainloop()



class HiderAndSeekerMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Hider and Seeker Menu")

        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.create_menu()

    def create_menu(self):
        label = tk.Label(self.canvas, text="Hider and Seeker Game Menu", font=('Helvetica', 18))
        label.pack(pady=10)

        # Chọn kích thước bản đồ
        size_label = tk.Label(self.canvas, text="Select board size:")
        size_label.pack()
        self.size_entry = tk.Entry(self.canvas)
        self.size_entry.pack()

        # Chỉnh sửa bản đồ thủ công
        edit_button = tk.Button(self.canvas, text="Edit Map", command=self.edit_map)
        edit_button.pack(pady=10)

        # Chọn level để bắt đầu trò chơi
        level_label = tk.Label(self.canvas, text="Select game level:")
        level_label.pack()
        self.level_combo = ttk.Combobox(self.canvas, values=["Level 1", "Level 2", "Level 3", "Level 4"])
        self.level_combo.pack()

        # Nhập số Hider và Seeker
        hider_label = tk.Label(self.canvas, text="Enter number of Hiders:")
        hider_label.pack()
        self.hider_entry = tk.Entry(self.canvas)
        self.hider_entry.pack()

        seeker_label = tk.Label(self.canvas, text="Enter number of Seekers:")
        seeker_label.pack()
        self.seeker_entry = tk.Entry(self.canvas)
        self.seeker_entry.pack()

        # Nhập vị trí của từng agent
        agent_pos_button = tk.Button(self.canvas, text="Enter Agent Positions", command=self.enter_agent_positions)
        agent_pos_button.pack(pady=10)

        # Nhập thời gian của trò chơi (nếu có)
        time_label = tk.Label(self.canvas, text="Enter game time (optional):")
        time_label.pack()
        self.time_entry = tk.Entry(self.canvas)
        self.time_entry.pack()

        # Nút bắt đầu trò chơi
        start_button = tk.Button(self.canvas, text="Start Game", command=self.start_game)
        start_button.pack(pady=20)

    def edit_map(self):
        # Hàm chỉnh sửa bản đồ thủ công
        pass

    def enter_agent_positions(self):
        # Hàm nhập vị trí của từng agent
        pass

    def start_game(self):
        # Hàm bắt đầu trò chơi
        pass

def main():
    root = tk.Tk()
    menu = HiderAndSeekerMenu(root)
    root.mainloop()


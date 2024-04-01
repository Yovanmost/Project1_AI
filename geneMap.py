import tkinter as tk
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





# Kích thước bản đồ
n = 50

# Tạo bản đồ
map = tao_map(n)
# Xuất file txt
xuat_file_txt(map, n)

# Hiển thị bản đồ
hien_thi_map(map, n)


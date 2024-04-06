import tkinter as tk
import random
import heapq

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0

RADIUS = 3  # Bán kính tầm nhìn của Seeker

def create_map(n, m):
    """
    Hàm tạo bản đồ trò chơi trốn tìm

    Tham số:
        n: Số hàng của bản đồ
        m: Số cột của bản đồ

    Trả về:
        map: Ma trận 2 chiều chứa bản đồ trò chơi
    """
    # Khởi tạo map
    map = [[WALL for _ in range(m)] for _ in range(n)]

    # Tạo đường đi
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if random.random() < 0.70:
                map[i][j] = PATH

    # Xử lý trường hợp 2 ô WALL liền kề
    for i in range(1, n - 1):
        for j in range(1, m - 1):
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


def save_map_to_file(map, map_size_n, map_size_m, filename):
    """
    Hàm lưu thông tin map và kích thước vào file

    Tham số:
        map: Ma trận 2 chiều chứa bản đồ trò chơi
        map_size_n: Số hàng của bản đồ
        map_size_m: Số cột của bản đồ
        filename: Tên của file để lưu

    Trả về:
        Không có
    """
    with open(filename, 'w') as file:
        file.write(f"{map_size_n} {map_size_m}\n")  # Ghi kích thước của map
        for row in map:
            file.write(' '.join(str(cell) for cell in row) + '\n')

def main():
    map_size_n = 40  # Số hàng mặc định
    map_size_m = 30  # Số cột mặc định
    map = create_map(map_size_n, map_size_m)
    save_map_to_file(map, map_size_n, map_size_m, "map.txt")

if __name__ == "__main__":
    main()

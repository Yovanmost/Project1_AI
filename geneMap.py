import tkinter as tk
import random
import heapq

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0
OB = 4
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
    for i in range(1, n):
        for j in range(1, m):
            if random.random() < 0.60:
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

def spiral_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    num = 1
    left, right, top, bottom = 0, n - 1, 0, n - 1

    while num <= n * n:
        # Traverse from left to right
        for i in range(left, right + 1):
            matrix[top][i] = num
            num += 1
        top += 1

        # Traverse from top to bottom
        for i in range(top, bottom + 1):
            matrix[i][right] = num
            num += 1
        right -= 1

        # Traverse from right to left
        for i in range(right, left - 1, -1):
            matrix[bottom][i] = num
            num += 1
        bottom -= 1

        # Traverse from bottom to top
        for i in range(bottom, top - 1, -1):
            matrix[i][left] = num
            num += 1
        left += 1

    # Convert values to 0s and 1s
    for i in range(n):
        for j in range(n):
            matrix[i][j] %= 2

    return matrix

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
    map_size_n = 20  # Số hàng mặc định
    map_size_m = 60  # Số cột mặc định
    map = create_map(map_size_n, map_size_m)
    save_map_to_file(map, map_size_n, map_size_m, "mapVer7.txt")

if __name__ == "__main__":
    main()
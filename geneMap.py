import tkinter as tk
import random
import heapq

# CONSTANT
WALL = 1
HIDER = 2
SEEKER = 3
PATH = 0
OB = 4

def create_map(n, m):

    # Init map
    map = [[WALL for _ in range(m)] for _ in range(n)]

    # Gene path
    for i in range(1, n):
        for j in range(1, m):
            if random.random() < 0.60:
                map[i][j] = PATH

    # Delete unvalid walls
    for i in range(1, n - 1):
        for j in range(1, m - 1):
            if map[i][j] == WALL and map[i - 1][j - 1] == WALL and map[i][j - 1] == PATH and map[i - 1][j] == PATH:
                map[i][j] = PATH
                map[i - 1][j - 1] = PATH
            if map[i][j] == WALL and map[i + 1][j + 1] == WALL and map[i][j + 1] == PATH and map[i + 1][j + 1] == PATH:
                map[i][j] = PATH
                map[i + 1][j + 1] = PATH
            if map[i][j] == WALL and map[i + 1][j - 1] == WALL and map[i][j - 1] == PATH and map[i + 1][j] == PATH:
                map[i][j] = PATH
                map[i + 1][j - 1] = PATH
            if map[i][j] == WALL and map[i + 1][j + 1] == WALL and map[i][j + 1] == PATH and map[i + 1][j] == PATH:
                if random.random() < 0.5:
                    map[i][j + 1] = WALL
                else:
                    map[i + 1][j] = WALL
    return map

def save_map_to_file(map, map_size_n, map_size_m, filename):
    with open(filename, 'w') as file:
        file.write(f"{map_size_n} {map_size_m}\n")  
        for row in map:
            file.write(' '.join(str(cell) for cell in row) + '\n')

def main():
    map_size_n = 10 
    map_size_m = 10
    map = create_map(map_size_n, map_size_m)
    save_map_to_file(map, map_size_n, map_size_m, "mapVer11.txt")

main()
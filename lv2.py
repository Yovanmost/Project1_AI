import tkinter as tk
import random
import queue
import math

class HiderAndSeekerGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hider and Seeker Game")
        
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg='white')
        self.canvas.pack()

        self.board_size = 10
        self.wall_density = 0.1
        self.seeker_position = (0, 0)
        self.hider_position = (0, 0)

        self.generate_board()
        self.place_characters()

        self.start_button = tk.Button(self.master, text="Start", command=self.start_game)
        self.start_button.pack()

    def generate_board(self):
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        for i in range(self.board_size):
            for j in range(self.board_size):
                if random.random() < self.wall_density:
                    self.board[i][j] = 1
                    self.canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, fill='black')

    def place_characters(self):
        self.seeker_position = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
        self.hider_position = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
        while self.seeker_position == self.hider_position:
            self.hider_position = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))

        self.seeker = self.canvas.create_rectangle(self.seeker_position[1] * 40, self.seeker_position[0] * 40,
                                                   (self.seeker_position[1] + 1) * 40, (self.seeker_position[0] + 1) * 40,
                                                   fill='blue')
        self.hider = self.canvas.create_rectangle(self.hider_position[1] * 40, self.hider_position[0] * 40,
                                                  (self.hider_position[1] + 1) * 40, (self.hider_position[0] + 1) * 40,
                                                  fill='red')

    def start_game(self):
        self.move_seekers()

    def move_seekers(self):
        self.master.update()
        self.move_seeker()
        self.move_hider()
        if self.seeker_position == self.hider_position:
            self.canvas.create_text(200, 200, text="You caught the hider!", font=('Helvetica', 24))
        else:
            self.master.after(1000, self.move_seekers)

    def move_seeker(self):
        path = self.find_path_astar(self.seeker_position, self.hider_position)
        if path:
            next_position = path[1]
            self.canvas.move(self.seeker, (next_position[1] - self.seeker_position[1]) * 40, (next_position[0] - self.seeker_position[0]) * 40)
            self.seeker_position = next_position

    def move_hider(self):
        path = self.find_path_bfs(self.hider_position, self.seeker_position)
        if path:
            next_position = path[1]
            self.canvas.move(self.hider, (next_position[1] - self.hider_position[1]) * 40, (next_position[0] - self.hider_position[0]) * 40)
            self.hider_position = next_position

    def find_path_astar(self, start, goal):
        open_list = queue.PriorityQueue()
        open_list.put((0, start))
        came_from = {}
        g_score = {start: 0}

        while not open_list.empty():
            current_cost, current = open_list.get()

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, goal)
                    open_list.put((f_score, neighbor))
                    came_from[neighbor] = current

        return None

    def find_path_bfs(self, start, goal):
        visited = set()
        q = queue.Queue()
        q.put(start)
        came_from = {}

        while not q.empty():
            current = q.get()

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    q.put(neighbor)
                    visited.add(neighbor)
                    came_from[neighbor] = current

        return None

    def get_neighbors(self, position):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_x = position[0] + dx
                new_y = position[1] + dy
                if 0 <= new_x < self.board_size and 0 <= new_y < self.board_size and (dx != 0 or dy != 0) and self.board[new_x][new_y] == 0:
                    neighbors.append((new_x, new_y))
        return neighbors

    def heuristic(self, a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def main():
    root = tk.Tk()
    game = HiderAndSeekerGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()

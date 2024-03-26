class Agent:
    def __init__(self, grid, size, pos):
        self.grid = grid
        self.rows = size[0]
        self.cols = size[1]
        self.pos = pos

    def get_surrounding_cells(self, row, col):
        surrounding_cells = []

        for i in range(max(0, row - 1), min(row + 2, self.rows)):
            for j in range(max(0, col - 1), min(col + 2, self.cols)):
                if (i, j) != (row, col):
                    surrounding_cells.append(self.grid[i][j])

        return surrounding_cells

    def getSurrounding(self):
        surrounding = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1,), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_i = self.pos[0] + dir[0]
            new_j = self.pos[1] + dir[1]
            if 0 <= new_i < self.rows and 0 <= new_j < self.cols and :
                pass
        return

    def check_surroundings(self, row, col):
        return self.get_surrounding_cells(row, col)

# Example usage:
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

agent = Agent(grid)
row = 1
col = 0
surrounding_cells = agent.check_surroundings(row, col)
print("Surrounding cells of ({}, {}):".format(row, col), surrounding_cells)

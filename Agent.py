
class Agent:
    
    # WALL
    WALL = 1
    
    # Direction
    UP = 1
    UP_RIGHT = 2
    RIGHT = 3
    DOWN_RIGHT = 4
    DOWN = 5
    DOWN_LEFT = 6
    LEFT = 7
    UP_LEFT = 8
    
    def __init__(self, position):
        self.position = list(position)
        
    def move(self, direction):
        directions = [
            [0,0],    # no move
            [-1,0],   # up
            [-1,1],   # up_right
            [0,1],    # right
            [1,1],    # down_right
            [1,0],    # down
            [1,-1],   # down_left
            [0,-1],   # left
            [-1,-1]   # up_left
        ]
        dx, dy = directions[direction]
        self.position[0] += dx
        self.position[1] += dy
    
    def vision(self, grid):
        pass
    
    def is_inside(position, size):
        x, y = position
        width, height = size
        return (0 <= x < width) and (0 <= y < height)
        

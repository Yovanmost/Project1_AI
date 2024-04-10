# This will test all the functions
# How frontend interact with the backend

import board as bd
from inputMap import readInputFile
import Gui as rd2
import Solve
import menu as Menu
FILE_NAME = "mapVer5.txt"


def main():
    running = True
    while running:
        level, FILE_NAME = Menu.start_game()
        game = Solve.Solve(FILE_NAME)
        if level == '1' or level == '2':
            game.playLevel1and2()
        else:
            game.playLevel3()
        
        render = rd2.Render(game.Board, game.history)
        render.render()
    
if __name__ == "__main__":
    main()
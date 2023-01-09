# import the module
from SudokuBlockGenerator import SudokuGridGenerator
import random
import copy
import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (171, 215, 235)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700

class PuzzleByDifficultyGenerator():
    def __init__(self):
        pygame.font.init()
        self.grid = SudokuGridGenerator()
        self.numbers = []
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.SCREEN.fill(WHITE)
        self.myfont = pygame.font.SysFont('Times New Roman', 30)
        self.loadingText = "Generating Puzzle..."
        self.initialX = 240



    def gridGenerator(self):
        for row in self.grid.rows:
            for number in row:
                self.numbers.append(number)
        test = 0
        print("Generating Full Grid", end="")

        while 0 in self.numbers:
            self.SCREEN.fill(WHITE)
            textSurface = self.myfont.render(self.loadingText, False, (0, 0, 0))
            self.SCREEN.blit(textSurface, (self.initialX, 240))
            self.initialX -= 5
            self.loadingText = self.loadingText + "."
            pygame.display.update()


            self.numbers = []
            print(".", end = "")
            if test == 10:
                print("ERROR")
                break

            del(self.grid)
            self.grid = SudokuGridGenerator()
            self.grid.genThreeBlocks()
            self.grid.nextTwoBlocks()
            self.grid.upAndDown()
            self.grid.leftAndRight()
            for row in self.grid.rows:
                for number in row:
                    self.numbers.append(number)
            test += 1

        print("\n")
        for row in self.grid.rows:
            print(row)

        # self.difficulty_selector(self.grid)

    def __repr__(self):
        final_grid  = []
        for row in self.grid:
            final_grid.append(row)
        return final_grid

    def difficulty_selector_terminal(self, grid):
        chosen = False
        print("Select your difficulty. (E = Easy, M = Medium, H = Hard, X = Expert)\n")
        self.copy_grid = copy.deepcopy(grid)
        while chosen == False:
            chosenDifficulty = input()
            if chosenDifficulty.upper() == "E":
                chosen = True
                self.easyMode(grid)

            elif chosenDifficulty.upper() == "M":
                chosen = True
                self.mediumMode(grid)

            elif chosenDifficulty.upper() == "H":
                chosen = True
                self.hardMode(grid)

            elif chosenDifficulty.upper() == "X":
                chosen = True
                self.expertMode(grid)

            else:
                print("Not a valid option.")

        print("\n")
        for row in grid.rows:
            print(row)
        # print("\n")
        # for row in copy_grid.rows:
        #     print(row)



    def easyMode(self, grid):
        print("Easy Selected")
        i = 0
        while i < 30:
            row = random.randint(0, 8)
            column = random.randint(0,8)
            if grid.rows[row][column] != 0:
                grid.rows[row][column] = 0
                i += 1
        return

    def mediumMode(self, grid):
        print("Medium Selected")
        i = 0
        while i < 40:
            row = random.randint(0, 8)
            column = random.randint(0,8)
            if grid.rows[row][column] != 0:
                grid.rows[row][column] = 0
                i += 1
        return

    def hardMode(self, grid):
        print("Hard Selected")
        i = 0
        while i < 50:
            row = random.randint(0, 8)
            column = random.randint(0,8)
            if grid.rows[row][column] != 0:
                grid.rows[row][column] = 0
                i += 1
        return

    def expertMode(self, grid):
        print("Expert Selected")
        i = 0
        while i < 64:
            row = random.randint(0, 8)
            column = random.randint(0,8)
            if grid.rows[row][column] != 0:
                grid.rows[row][column] = 0
                i += 1
        return

# puzzle = PuzzleByDifficultyGenerator()

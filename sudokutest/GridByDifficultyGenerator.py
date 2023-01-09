"""
Filename: GridByDifficultyGenerator.py
Author: Fernando Perez
Created: July 31, 2021
"""

# import necessary libraries for game.
from SudokuBlockGenerator import SudokuGridGenerator
from SudokuPresets import SudokuPresets
import random
import copy
import pygame

# Set constants for color and dimensions.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (171, 215, 235)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700


class PuzzleByDifficultyGenerator():
    """
    Class that generates a Sudoku puzzle and replaces numbers with 0 depending on difficulty chosen.
    """
    def __init__(self):
        """
        Initialize sudoku grid object with constants for screen and fonts.
        """
        # Initialize pygame
        pygame.font.init()

        # Initialize object of SudokuGridGenerator. This will be the grid: A list of 9 lists with 9 integers each.
        self.grid = SudokuGridGenerator()

        # Initialize list that will store every integer in grid. This is to make checking values easier, rather than
        # checking in each individual list.
        self.numbers = []

        # Setup and color screen
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.SCREEN.fill(WHITE)

        # Setup text font, size and text that will be displayed in loading screen.
        self.myfont = pygame.font.SysFont('Times New Roman', 30)
        self.loadingText = "Generating Puzzle..."

        # Initial coordinate of loading text.
        self.initialX = 240

    def gridGenerator(self):
        """
        Method that attempts to generate a random Sudoku board multiple times for a certain amount of attempts by
        initializing SudokuGridGenerator objects
        :return: None
        """
        # Fills the numbers list with every integer in the grid. This is to make checking for empty spaces easier
        for row in self.grid.rows:
            for number in row:
                self.numbers.append(number)
        # Initialize variable to track how much attempts have been made to create a grid.
        attempts = 0
        print("Generating Full Grid", end="")

        # Loop until a proper random Sudoku Puzzle is created with no empty spaces or until 10 attempts have been made.
        # If the condition evaluates to True, the grid is incorrect and we must try again.
        while 0 in self.numbers:
            # Display loading screen to user while generating board.
            self.SCREEN.fill(WHITE)
            textSurface = self.myfont.render(self.loadingText, False, (0, 0, 0))
            self.SCREEN.blit(textSurface, (self.initialX, 240))
            self.initialX -= 5
            self.loadingText = self.loadingText + "."
            pygame.display.update()
            print(".", end="")

            # Reset the list to be able to fill it with the next attempt's numbers.
            self.numbers = []

            # If 10 attempts have been made, use a preset board from SudokuPresets.py to avoid taking too long.
            if attempts == 10:
                # Initialize SudokuPresets object
                presetGen = SudokuPresets()

                # Store the board (list of lists) that self.grid will copy
                preset_puzzle = presetGen.presets(presetGen.preset_no)

                # Generate board of 0's
                self.grid = SudokuGridGenerator()

                # Iterate through every row and make each one copy the preset list row
                for row_number in range(0, 9):
                    self.grid.rows[row_number] = preset_puzzle[row_number]
                # Board is finished, exit loop
                break

            # The previous grid was incorrect so delete it and try it all again.
            del(self.grid)
            self.grid = SudokuGridGenerator()
            self.grid.genThreeBlocks()
            self.grid.nextTwoBlocks()
            self.grid.upAndDown()
            self.grid.leftAndRight()

            # With the new board, refill the list to check again for 0
            for row in self.grid.rows:
                for number in row:
                    self.numbers.append(number)
            attempts += 1

        # Display the finished grid.
        print("\n")
        for row in self.grid.rows:
            print(row)

    def easyMode(self):
        """
        When called, takes the created board and replaces 30 random numbers on the board with 0, which will be
        considered empty spaces in the game.
        :return: None
        """
        print("Easy Selected")
        i = 0
        while i < 5:
            row = random.randint(0, 8)
            column = random.randint(0,8)
            if self.grid.rows[row][column] != 0:
                self.grid.rows[row][column] = 0
                i += 1
        return

    def mediumMode(self):
        """
        When called, takes the created board and replaces 45 random numbers on the board with 0, which will be
        considered empty spaces in the game.
        :return: None
        """
        print("Medium Selected")
        i = 0
        while i < 45:
            row = random.randint(0, 8)
            column = random.randint(0,8)
            if self.grid.rows[row][column] != 0:
                self.grid.rows[row][column] = 0
                i += 1
        return

    def hardMode(self):
        """
        When called, takes the created board and replaces 59 random numbers on the board with 0, which will be
        considered empty spaces in the game.
        :return: None
        """
        print("Hard Selected")
        i = 0
        while i < 59:
            row = random.randint(0, 8)
            column = random.randint(0,8)
            if self.grid.rows[row][column] != 0:
                self.grid.rows[row][column] = 0
                i += 1
        return

    def expertMode(self):
        """
        When called, takes the created board and replaces 64 random numbers on the board with 0, which will be
        considered empty spaces in the game.
        :return: None
        """
        print("Expert Selected")
        i = 0
        while i < 64:
            row = random.randint(0, 8)
            column = random.randint(0,8)
            if self.grid.rows[row][column] != 0:
                self.grid.rows[row][column] = 0
                i += 1
        return


    # def difficulty_selector_terminal(self, grid):
    #     """
    #
    #     :param grid:
    #     :return:
    #     """
    #     chosen = False
    #     print("Select your difficulty. (E = Easy, M = Medium, H = Hard, X = Expert)\n")
    #     self.copy_grid = copy.deepcopy(grid)
    #     while chosen == False:
    #         chosenDifficulty = input()
    #         if chosenDifficulty.upper() == "E":
    #             chosen = True
    #             self.easyMode(grid)
    #
    #         elif chosenDifficulty.upper() == "M":
    #             chosen = True
    #             self.mediumMode(grid)
    #
    #         elif chosenDifficulty.upper() == "H":
    #             chosen = True
    #             self.hardMode(grid)
    #
    #         elif chosenDifficulty.upper() == "X":
    #             chosen = True
    #             self.expertMode(grid)
    #
    #         else:
    #             print("Not a valid option.")
    #
    #     print("\n")
    #     for row in grid.rows:
    #         print(row)
    #     # print("\n")
    #     # for row in copy_grid.rows:
    #     #     print(row)

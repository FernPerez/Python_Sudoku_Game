"""
Filename: SudokuGameTitle.py
Author: Fernando
Created: July 31, 2021
"""

# Import necessary libraries
import pygame
import sys
import time
import copy

# Import GridByDifficultyGenerator to
from GridByDifficultyGenerator import PuzzleByDifficultyGenerator


# Set constants for colors and dimensions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (171, 215, 235)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700

class TitleScreen():
    """
    Class that creates and displays the title screen for Sudoku game.
    """
    def __init__(self):
        """
        Sets constants for screen and fonts
        """
        # Initialize pygame and font
        pygame.init()
        pygame.font.init()

        # Set screen display and clock
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.CLOCK = pygame.time.Clock()

        # Fill screen white
        self.SCREEN.fill(WHITE)

        # Set different fonts for use in the title screen
        self.FONT = pygame.font.SysFont('Times New Roman', 30)
        self.TITLEFONT = pygame.font.SysFont('Times New Roman', 80)
        self.SUBTITLEFONT = pygame.font.SysFont('Times New Roman', 20)

        # Booleans that serve as flags to move on to the game.
        self.running = True
        self.start = False
        self.difficultyChosen = False

    def genScreen(self):
        """
        Generate and display the screen. Begins with a title and start button. After the button is clicked, displays
        difficulty options for the player
        :return: Integer corresponding to difficulty: 0 = Easy, 1 = Medium, 2 = Hard, 3 = Expert. This number is then
        used in SudokuGameCleaned to generate the appropriate puzzle.
        """
        # Maintain the title screen displayed until the player exits or selects a difficulty.
        while self.running:
            # Loop until the player presses the start button
            while self.start == False:
                # Create and display the start button and title
                self.startButton()
                self.title()

                # Wait for an input from player
                event = pygame.event.wait()

                # Player exits window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Player left-clicks on start button
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # Get position of mouse click. If pos overlaps with button, set start to True to move on to next
                        # screen.
                        pos = pygame.mouse.get_pos()
                        if self.button.collidepoint(pos):
                            print("finished")
                            self.start = True
                # Update display
                pygame.display.update()

            # Player has clicked start button, reset the screen to display the difficulty options
            self.SCREEN.fill(WHITE)
            pygame.event.clear()
            # Wait a bit so transition isn't so abrupt
            time.sleep(0.2)

            # Loop until player has selected difficulty.
            while self.difficultyChosen == False:
                # Display options, title, and button text
                self.difficultyButtons()
                self.difficultyText()
                self.title()
                pygame.display.update()

                # Wait for user input
                event = pygame.event.wait()

                # Player exits window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Player left clicks on one of the options
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        # Depending on the button pressed, returns the corresponding number
                        for button in self.difficulty_button_list:
                            if button.collidepoint(pos):
                                # Set booleans to True to exit loop
                                self.start = True
                                self.difficultyNumber = self.difficulty_button_list.index(button)
                                self.difficultyChosen = True

            # Exit loop
            self.running = False
        # Return the number of the chosen difficulty.
        return self.difficultyNumber

    def startButton(self):
        """
        Creates and draws start button on title screen.
        :return: None
        """
        # Set coordinates and dimensions of button
        width = 300
        length = 100
        x = 200
        y = 400

        # Initialize and draw rectanges
        rect = pygame.Rect(x, y, width, length)
        inner_rect = pygame.Rect(x + 3, y + 3, width-5, length-5)
        pygame.draw.rect(self.SCREEN, BLACK, rect, 5)
        pygame.draw.rect(self.SCREEN, BLUE, inner_rect)

        # Initialize variable for the button to check its collision later.
        self.button = rect

        # Display text on button
        self.startText()


    def difficultyButtons(self):
        """
        Creates and draws buttons for difficulty options.
        :return: None
        """
        # Set dimensions and coordinates for buttons
        width = 150
        length = 50
        x = 260
        y = 300

        # Initialize a list that will store the buttons. This to make checking clicks easier.
        self.difficulty_button_list = []

        # Creates and draws all necessary triangles
        for i in range(0,4):
            button = pygame.Rect(x, y, width, length)
            inner_button = pygame.Rect(x + 2, y + 2, width-3, length-3)
            pygame.draw.rect(self.SCREEN, BLACK, button, 2)
            pygame.draw.rect(self.SCREEN, BLUE, inner_button)
            self.difficulty_button_list.append(button)

            # Move down to do next button
            y += 75

    def startText(self):
        """
        Creates and draws text on the start button.
        :return: None
        """
        textSurface = self.FONT.render('START', False, (0, 0, 0))
        self.SCREEN.blit(textSurface, (300, 425))

    def difficultyText(self):
        """
        Creates and draws text on the difficulty buttons.
        :return: None
        """
        # List of strings to display.
        difficulty_text_lst = ['Easy', 'Medium', 'Hard', 'Expert']
        # Initial coordinates.
        x = 275
        y = 315

        # Draw all the strings on the buttons
        for i in range(4):
            textSurface = self.FONT.render(difficulty_text_lst[i], False, (0, 0, 0))
            self.SCREEN.blit(textSurface, (x, y))

            # Move to next button.
            y += 75


    def title(self):
        """
        Creates and draws Title Screen text.
        :return: None
        """
        # Title
        textSurface = self.TITLEFONT.render('SUDOKU', False, (0, 0, 0))
        self.SCREEN.blit(textSurface, (185, 150))

        # Author
        textSurface = self.SUBTITLEFONT.render('by Fernando Perez', False, (0,0,0))
        self.SCREEN.blit(textSurface, (260, 240))

    # def genPuzzle(self, difficulty):
    #     #self.SCREEN.fill(WHITE)
    #     # textSurface = self.FONT.render('Generating Puzzle...', False, (0, 0, 0))
    #     # self.SCREEN.blit(textSurface, (240, 240))
    #     # pygame.display.update()
    #     print("start")
    #     puzzle = PuzzleByDifficultyGenerator()
    #     puzzle.gridGenerator()
    #     self.original_grid = copy.deepcopy(puzzle.grid.rows)
    #     if difficulty == 0:
    #         puzzle.easyMode()
    #     elif difficulty == 1:
    #         puzzle.mediumMode()
    #     elif difficulty == 2:
    #         puzzle.hardMode()
    #     else:
    #         puzzle.expertMode()
    #     self.adjusted_grid = puzzle.grid.rows





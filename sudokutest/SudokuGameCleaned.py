"""
Filename: SudokuGameCleaned.py
Author: Fernando Perez
Created: August 13, 2021
"""

# import necessary libraries for game.
import pygame
import sys
import time
import copy

# import title screen
from SudokuGameTitle import TitleScreen

from GridByDifficultyGenerator import PuzzleByDifficultyGenerator

class SudokuGame():
    """
    Class that generates and displays a fully playable Sudoku Game by using different methods and classes from other
    modules.
    Input: None
    :returns: sudoku game object
    """
    def __init__(self):
        """
        instatiates sudoku game with necessary constants and class variables.
        """
        # Color constants:
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (171, 215, 235)
        self.GREY = (220, 220, 220)
        self.RED = (255, 105, 97)

        # Window Dimensions:
        self.WINDOW_HEIGHT = 700
        self.WINDOW_WIDTH = 700

        # Initialize dict variable that will later store the coordinates of the numbers not removed from the board when
        # starting the game
        # keys: integer representing row
        # values: list of integers corresponding to columns
        self.greyed_out_squares = {}

        # Initialize dict variable that will later store the coordinates of the numbers the user inputs that are
        # incorrect. This is to keep track of them and remove them if the player corrects them.
        # keys: integer representing row
        # values: list of integers corresponding to columns
        self.red_squares = {}

        # Initialize font use in pygame and select font
        pygame.font.init()
        self.FONT = pygame.font.SysFont('Times New Roman', 30)
        self.smallFont = pygame.font.SysFont('Times New Roman', 15)

        # Initialize clock
        self.CLOCK = pygame.time.Clock()

    def gameTitle(self):
        """
        Uses imported TitleScreen() class to generate and display the title screen for the player to start and choose
        a difficulty.
        :return: None
        """
        # Create title object
        self.title = TitleScreen()

        # Generate title screen and display it to the user. After the player chooses a difficulty, the method will
        # return a number based on the selection to generate the puzzle accordingly.
        self.difficultyNumber = self.title.genScreen()

        self.genPuzzle(self.difficultyNumber)

    def genPuzzle(self, difficulty):
        """
        Uses imported GridByDifficultyGenerator to create a random Sudoku Puzzle and remove numbers from it based on
        difficulty.
        :param difficulty: integer between 0 and 3 corresponding to difficulty
        :return: None
        """
        print("start")

        # Initialize object self.puzzle as an instance of PuzzleByDifficultyGenerator()
        self.puzzle = PuzzleByDifficultyGenerator()

        # Transform the object into a list of 9 lists with 9 int elements each, representing the rows in the Sudoku
        # board. The numbers will be randomized while following Sudoku rules.
        self.puzzle.gridGenerator()

        # Copy the grid before making changes to it in case its original state is needed later.
        self.original_grid = copy.deepcopy(self.puzzle.grid.rows)

        # Depending on chosen difficulty remove the call corresponding PuzzleByDifficultyGenerator() method to remove
        # numbers from the board.
        if difficulty == 0:
            self.puzzle.easyMode()
        elif difficulty == 1:
            self.puzzle.mediumMode()
        elif difficulty == 2:
            self.puzzle.hardMode()
        else:
            self.puzzle.expertMode()

        # Initialize variable that stores the rows(lists) of the puzzle object. This is to make referencing the grid
        # much easier.
        self.puzzleGrid = self.puzzle.grid.rows


        # Loop that fills in the greyed_out_squares dictionary by iterating through every row and finding the coordi-
        # nates of every number not removed, the rows being keys and the lists of corresponding columns being values.
        for row in self.puzzleGrid:
            row_index = self.puzzleGrid.index(row)
            self.greyed_out_squares[row_index] = []
            for number in row:
                # Number not 0, meaning it wasn't removed.
                if number != 0:
                    index = row.index(number)
                    self.greyed_out_squares[row_index].append(index)

    def mainGameLoop(self):
        """
        Contains the main loop of the game that will cycle and update the display until the player exits the game.
        :return: None
        """
        # Before beginning loop, let the game transition from the title screen in a natural non-abrupt form by waiting
        # and preventing inputs.
        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
        time.sleep(0.1)

        # Keep track of when the game started so as to show the player their completion time.
        self.startTime = time.time()

        # Initizalize the game
        pygame.init()

        # Display window and fill it white
        self.SCREEN = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.SCREEN.fill(self.WHITE)

        # Variable used to check if the game is still running
        running = True

        # Dictionary that keeps track of all the pygame rectangles created when creating the grid that is displayed to
        # the user. This to know what squares are clicked on and associate them to the Sudoku Board.
        # Keys: row number integer
        # Values: lists of pygame rectangle objects, each with their respective dimensions and coordinates.
        self.row_rects_dict = {}

        # boolean variable to know if the program is on its first loop. This is because the first loop displays grey
        # squares behind the existing numbers, so this is used to make sure that only those are considered grey squares
        # and not the ones the player adds afterwards.
        firstloop = True

        # variable that keeps track of the loop number. This is used during the loop to determine if the game should
        # wait for the user's input of use an already registered input.
        loop_number = 1

        # allow player inputs that were previously blocked
        pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

        # Display number counts to user.
        self.numCountDisplay()

        # Main Loop:
        while running:
            # variable that is used to determine if the player clicked on a square. Is reset to false every loop.
            clickedSquare = False

            # displays the full grid with lines, pre-existing numbers, grey squares, and text.
            self.puzzleDisplayer(firstloop) #True the first loop, False every other time.
            self.drawGrid()
            self.drawText(self.difficultyNumber)
            self.drawThickLines()

            # If it is the first loop, or the user clicked on something that was not selectable, wait for another input.
            if loop_number == 1:
                event = pygame.event.wait()
            # otherwise if the player clicks on something selectable while selecting an object, go with an already
            # stored event.
            else:
                event = self.newEvent

            # player closes window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # player clicks on something
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # increase loop_number for the event conditional above
                loop_number += 1
                if event.button == 1:  # left mouse button
                    # get position of where the player clicked
                    pos = pygame.mouse.get_pos()

                    # loop that iterates through every item in row_rects_dict. For every rectangle, if the respective
                    # position collides with where the player clicked and the square was not greyed out, the
                    # corresponding square will be selected.
                    for row, columns in self.row_rects_dict.items():
                        for rect in columns:
                            if rect.collidepoint(pos) and columns.index(rect) not in self.greyed_out_squares[row]:
                                print("clicked on ", row, "x", columns.index(rect))

                                # call method that deals with selecting squares
                                self.squareSelect(rect, row, columns.index(rect))

                                # tell the program that the user clicked on a square, then break as no further
                                # comparisons are necessary.
                                clickedSquare = True
                                break

                    # If the player did not select a valid square or the player inputted a number, loop_number's value
                    # is reset to 0 so as to await a new event from the user.
                    if clickedSquare == False or self.placedNumber == True:
                        print("no")
                        loop_number = 1

            # Update the display of the game
            pygame.display.update()
            # set firstloop to False at the end of the first loop.
            firstloop = False

    def drawGrid(self):
        """
        creates the basic 9x9 Sudoku grid that will be displayed to the player
        :return: None
        """
        # size of each square
        blocksize = 50
        # starting coordinates and row
        x = 125
        y = 30
        row = 0

        # Loop that creates the 81 rectangles that will be displayed to the player. It goes left to right, top to bottom
        while y < 460:
            # adds key corresponding to the row number
            self.row_rects_dict[row] = []
            while x < 575:
                # create rectangle and appends it to the list value that corresponds to the row.
                rect = pygame.Rect(x, y, blocksize, blocksize)
                self.row_rects_dict[row].append(rect)

                # draw the rect on the screen
                pygame.draw.rect(self.SCREEN, self.BLACK, rect, 1)

                # move to next square to the right
                x += 50
            # reset the x coordinate and shift the y coordinate before moving to next row
            row += 1
            y += 50
            x = 125

    def puzzleDisplayer(self, firstloop):
        """
        displays the board of numbers based off the generated Sudoku Puzzle, also displays grey squares for the numbers
        the board starts on
        :param firstloop: boolean that determines if grey squares should be displayed under the numbers
        :return: None
        """
        # square size and initial coordinates
        blocksize = 50
        x = 140
        y = 40

        # Loop that iterates through every integer in ever list of puzzleGrid, displaying them on the board at the
        # specified coordinates. If called on the first loop, places grey squares behind them as well.
        for row in self.puzzleGrid:
            for number in row:
                if number != 0: # not an empty space
                    if firstloop == True:
                        # grey square creation and drawing
                        grey_rect = pygame.Rect(x - 15, y - 10, blocksize, blocksize)
                        pygame.draw.rect(self.SCREEN, self.GREY, grey_rect)

                    # creates number text and draws on screen at coordinates
                    numSurface = self.FONT.render(str(number), False, (0, 0, 0))
                    self.SCREEN.blit(numSurface, (x, y))

                # move to the right
                x += 50

            # reset x coordinate and shift y coordinate
            y += 50
            x = 140

    def drawThickLines(self):
        """
        Creates and draws the thick lines that separate every 3x3 square on the grid
        :return: None
        """
        # dictionary that stores every line and their respective coordinates, size, and thickness.
        line_dict = {
            'leftline': pygame.Rect(125, 30, 3, 450),
            'vline1': pygame.Rect(275, 30, 3, 450),
            'vline2': pygame.Rect(425, 30, 3, 450),
            'rightline': pygame.Rect(575, 30, 3, 450),
            'topline': pygame.Rect(125, 30, 450, 3),
            'hline1': pygame.Rect(125, 180, 450, 3),
            'hline2': pygame.Rect(125, 330, 450, 3),
            'bottomline': pygame.Rect(125, 480, 450, 3)
        }
        # Draw each line on the screen.
        for line in line_dict:
            pygame.draw.rect(self.SCREEN, self.BLACK, line_dict[line])

    def drawText(self, difficulty):
        """
        Display text on top of the board depending on difficulty
        :return:
        """
        # Check difficulty number
        if difficulty == 0:
            textSurface = self.FONT.render('Easy', False, (0, 0, 0))
            self.SCREEN.blit(textSurface, (320, 0))
        elif difficulty == 1:
            textSurface = self.FONT.render('Medium', False, (0, 0, 0))
            self.SCREEN.blit(textSurface, (300, 0))
        elif difficulty == 2:
            textSurface = self.FONT.render('Hard', False, (0, 0, 0))
            self.SCREEN.blit(textSurface, (320, 0))
        else:
            textSurface = self.FONT.render('Expert', False, (0, 0, 0))
            self.SCREEN.blit(textSurface, (300, 0))


    def squareSelect(self, rect, row, column):
        """
        Method that deals with the square selection process. When called after the user clicks on a square on the board,
        highlights the square and waits for an input. Performs different actions depending on whether a number key was
        pressed or the user clicks on another square.
        :param rect: rectangle object from list value in row_rects_dict corresponding to position clicked on by user
        :param row: integer key in row_rects_dict corresponding to row the rectangle is in.
        :param column: integer value corresponding to the index of rect in the row's list value
        :return: None
        """
        print("changing")

        # Allow the user to press a key to do something
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(pygame.KEYUP)

        # Resets placedNumber to False when called in case the user does not input a number
        self.placedNumber = False
        # The player selected a valid square
        selected = True

        # Create a blue rectangle to draw on the board on top of the square the player clicked on.
        inner_rect = pygame.Rect(rect.x + 1, rect.y + 1, 48, 48)
        pygame.draw.rect(self.SCREEN, self.BLUE, inner_rect)

        # Redraw the thick lines and board numbers so they show up above the blue square.
        self.drawThickLines()
        self.puzzleDisplayer(firstloop=False)

        # Clear the event queue of all events before checking for new ones
        pygame.event.clear()

        # Loop that continues as long as the player is highlighting a square and has not performed a valid action such
        # as placing a number, quitting, or clicking somewhere else.
        while selected:
            pygame.display.update()

            # Wait for the player to input something
            event = pygame.event.wait()

            # Initialize a variable that will store whatever input the player made. This is used when the player selects
            # a square, but then selects another square without filling the previous one in. The program keeps track of
            # where the player clicked on so it knows what block to highlight in the next game loop
            self.newEvent = event

            # player closes window
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Player clicks on something. The loop ends and the square will no longer be selected or highlighted.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    selected = False
            # Player presses a key.
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                # If the key is a number or numberpad key, places the number on the board and calls inputChecker() to
                # see if the number does not conflict with the board given Sudoku rules. This will let us know if the
                # number is wrong and should be highlighted red for the player.

                # Player presses 1
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    redSquare = self.inputChecker(1, row, column)
                    self.puzzleGrid[row][column] = 1
                    self.placedNumber = True # used in main loop to to reset the loop number
                    selected = False # square no longer selected

                # Player presses 2
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    redSquare = self.inputChecker(2, row, column)
                    self.puzzleGrid[row][column] = 2
                    self.placedNumber = True
                    selected = False

                # Player presses 3
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    redSquare = self.inputChecker(3, row, column)
                    self.puzzleGrid[row][column] = 3
                    self.placedNumber = True
                    selected = False

                # Player presses 4
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    redSquare = self.inputChecker(4, row, column)
                    self.puzzleGrid[row][column] = 4
                    self.placedNumber = True
                    selected = False

                # Player presses 5
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    redSquare = self.inputChecker(5, row, column)
                    self.puzzleGrid[row][column] = 5
                    self.placedNumber = True
                    selected = False

                # Player presses 6
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    redSquare = self.inputChecker(6, row, column)
                    self.puzzleGrid[row][column] = 6
                    self.placedNumber = True
                    selected = False

                # Player presses 7
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    redSquare = self.inputChecker(7, row, column)
                    self.puzzleGrid[row][column] = 7
                    self.placedNumber = True
                    selected = False

                # Player presses 8
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    redSquare = self.inputChecker(8, row, column)
                    self.puzzleGrid[row][column] = 8
                    self.placedNumber = True
                    selected = False

                # Player presses 9
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    redSquare = self.inputChecker(9, row, column)
                    self.puzzleGrid[row][column] = 9
                    self.placedNumber = True
                    selected = False

                # Player presses backspace or delete key. This will change the number back into a 0, which will not
                # be displayed on the board.
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.puzzleGrid[row][column] = 0
                    self.placedNumber = True
                    selected = False

        # Call redSquareRemover() to remove any unnecessary red squares from red_squares_dict if the player made
        # corrections
        self.redSquareRemover()

        # If squares are in the red_squares_dict, creates a red highlight over them. If not, creates a white square.
        inner_rect = pygame.Rect(rect.x + 1, rect.y + 1, 48, 48)
        if row not in self.red_squares or column not in self.red_squares[row]:
            pygame.draw.rect(self.SCREEN, self.WHITE, inner_rect)
        else:
            pygame.draw.rect(self.SCREEN, self.RED, inner_rect)

        # redraws thickines on top of squares and updates the entire display.
        self.drawThickLines()
        pygame.display.update()

        # call numCountDisplay to update user on number counts.
        self.numCountDisplay()

        # call fullChecker in case the game has been completed.
        self.fullChecker()


    def inputChecker(self, number, row, column):
        """
        Method that, when called, evaluates the inputted number by comparing it to the numbers in its row, column, and
        3x3 square to ensure it is valid given Sudoku Rules. Also adds incorrect number coordinates to red_squares
        to keep track of red squares
        :param number: integer that it is evaluating
        :param row: integer representing row number
        :param column: integer representing column number
        :return: boolean; True if number conflicts, False if it is valid
        """
        # Create a list of every number in each row that shares its index with 'number'. This is the column.
        column_lst = []
        for rowIterator in self.puzzleGrid:
            for num in rowIterator:
                if rowIterator.index(num) == column:
                    column_lst.append(num)

        # Create a list of every number in the 3x3 square by calling threeByThreeUpdater()
        threeByThreeLst = self.threeByThreeUpdater(row, column)

        # Check to see if the number does not conflict with the row, column, or 3x3. If it does, add its position to
        # red_squares. The key is the row and the value is a list of respective columns.
        if number in self.puzzleGrid[row] or number in column_lst or number in threeByThreeLst:
            if row in self.red_squares:
                self.red_squares[row].append(column)
            else:
                self.red_squares[row] = [column]
            return True

        else:
            return False

    def threeByThreeUpdater(self, row, column):
        """
        returns a list of all the numbers in the 3x3 that the square is a part of for evaluating.
        :param row: integer corresponding to row number
        :param column: integer corresponding to row column
        :return: list of all integers in the 3x3
        """
        # Initialize list
        threeByThreeList = []

        # Given the row and column, iterate through the corresponding lists to fill threeByThreeList
        if row < 3:
            if column < 3:
                for rowIterator in self.puzzleGrid[0:3]:
                    for number in rowIterator[0:3]:
                        threeByThreeList.append(number)
            elif column < 6:
                for rowIterator in self.puzzleGrid[0:3]:
                    for number in rowIterator[3:6]:
                        threeByThreeList.append(number)
            else:
                for rowIterator in self.puzzleGrid[0:3]:
                    for number in rowIterator[6:9]:
                        threeByThreeList.append(number)

        elif row < 6:
            if column < 3:
                for rowIterator in self.puzzleGrid[3:6]:
                    for number in rowIterator[0:3]:
                        threeByThreeList.append(number)
            elif column < 6:
                for rowIterator in self.puzzleGrid[3:6]:
                    for number in rowIterator[3:6]:
                        threeByThreeList.append(number)
            else:
                for rowIterator in self.puzzleGrid[3:6]:
                    for number in rowIterator[6:9]:
                        threeByThreeList.append(number)

        else:
            if column < 3:
                for rowIterator in self.puzzleGrid[6:9]:
                    for number in rowIterator[0:3]:
                        threeByThreeList.append(number)
            elif column < 6:
                for rowIterator in self.puzzleGrid[6:9]:
                    for number in rowIterator[3:6]:
                        threeByThreeList.append(number)
            else:
                for rowIterator in self.puzzleGrid[6:9]:
                    for number in rowIterator[6:9]:
                        threeByThreeList.append(number)

        return threeByThreeList

    def redSquareRemover(self):
        """
        When called, removes red squares on board if they have been corrected.
        :return: None
        """
        # Check to see if there are squares in red_squares dict. If so, check to see if they can be removed.
        if len(self.red_squares) > 0:
            # Create a dictionary to keep track of coordinates of squares that can be removed. Keys will be integers
            # corresponding to rows, values will be lists of integers corresponding to columns.
            removable_red_squares = {}

            # Given the number located in the coordinates, compare it to its row, column and 3x3 to see if it is no
            # longer incorrect.
            for key, value in self.red_squares.items():
                for column in value:
                    number = self.puzzleGrid[key][column]
                    column_list = []  # create list of numbers in column
                    for row in self.puzzleGrid:
                        column_list.append(row[column])

                    # Create list of numbers in 3x3
                    three_by_three = self.threeByThreeUpdater(key, column)

                    # Boolean checks used to determine if no conflicts exist. False means there are conflicts
                    row_check = False
                    column_check = False
                    three_by_three_check = False

                    # No conflict in row
                    if self.puzzleGrid[key].count(number) < 2 or number == 0:
                        row_check = True

                    # No conflict i column
                    if column_list.count(number) < 2 or number == 0:
                        column_check = True

                    # No conflict in 3x3
                    if three_by_three.count(number) < 2 or number == 0:
                        three_by_three_check = True

                    # If all checks are are True
                    if row_check == True and column_check == True and three_by_three_check == True:
                        # Create a white rectangle and draw it over the red one.
                        rect = self.row_rects_dict[key][column]
                        inner_rect = pygame.Rect(rect.x + 1, rect.y + 1, 48, 48)
                        pygame.draw.rect(self.SCREEN, self.WHITE, inner_rect)

                        # Add the row column pair to the dict of removable ones.
                        if key not in removable_red_squares:
                            removable_red_squares[key] = [column]
                        else:
                            removable_red_squares[key].append(column)

            # For every removable row column pair, remove them from red_squares dict.
            for key, value in removable_red_squares.items():
                for column in value:
                    if key in self.red_squares and column in self.red_squares[key]:
                        self.red_squares[key].remove(column)

                    # row key's list is empty, so remove it from the dict.
                    if len(self.red_squares[key]) < 1:
                        del self.red_squares[key]

            return

    def fullChecker(self):
        """
        Called every time a number is inputted to see if the board is complete and the player has won.
        :return: None
        """
        # Boolean checks to see if there are no conflicts on the board
        rowCheck = False
        columnCheck = False
        threeByThreeCheck = False
        zeroCheck = False

        # Create two dictionaries corresponding to columns and 3x3 squares. The keys will be the number of the
        # group, while the values will be lists of integers that belong to them.
        # Columns dictionary
        column_dict = {}
        for i in range(9):
            column_dict[i] = []
            for row in self.puzzleGrid:
                column_dict[i].append(row[i])

        # 3x3's dictionary; x is the row and y is the column. The 3x3's are counted left to right, top to bottom.
        three_by_three_dict = {}
        x = 0
        y = 0
        for i in range(9):
            three_by_three_to_add = self.threeByThreeUpdater(x, y)
            three_by_three_dict[i] = three_by_three_to_add
            x += 3
            if x == 9:
                x = 0
                y += 3

        # Check to see if every value in each row is unique
        for row in self.puzzleGrid:
            if len(set(row)) == len(row):
                rowCheck = True
            else:
                rowCheck = False  # break as soon as one mistake is found
                break

        # Do the same for the values in columns_dict
        for key, value in column_dict.items():
            if len(set(value)) == len(value):
                columnCheck = True
            else:
                columnCheck = False
                break

        # Do the same for the values in three_by_three_dict
        for key, value in three_by_three_dict.items():
            if len(set(value)) == len(value):
                threeByThreeCheck = True
            else:
                threeByThreeCheck = False
                break

        # Make sure there are no empty spaces
        for row in self.puzzleGrid:
            if 0 not in row:
                zeroCheck = True
            else:
                zeroCheck = False
                break

        # All checks are green, player has filled the board correctly, move to victory screen.
        if rowCheck == True and columnCheck == True and threeByThreeCheck == True:
            if zeroCheck == True:
                print("yay!")
                self.winScreen()

    def winScreen(self):
        """
        Show the player a brief victory screen upon completing the game before closing
        :return: None
        """
        # Update the puzzle display
        self.puzzleDisplayer(firstloop=False)

        # Properties of Victory text box
        width = 300
        length = 100
        x = 200
        y = 400

        # Draw the text box
        rect = pygame.Rect(x, y, width, length)
        inner_rect = pygame.Rect(x + 3, y + 3, width - 5, length - 5)
        pygame.draw.rect(self.SCREEN, self.BLACK, rect, 5)
        pygame.draw.rect(self.SCREEN, self.GREEN, inner_rect)

        # Draw text on screen
        textSurface = self.FONT.render('YOU WIN', False, (0, 0, 0))
        self.SCREEN.blit(textSurface, (285, 425))

        # Update display so the player sees.
        pygame.display.update()

        # Wait 5 seconds before closing the game.
        time.sleep(5)
        pygame.quit()
        sys.exit()

    def numberCount(self):
        """
        Scrolls through the in game board and returns a dictionary with every number and how many times they appear
        :return: Dictionary
            :keys: Integers representing numbers from the board
            :values: Integers representing the amount of times the corresponding key appears on the board.
        """
        # dictionary of numbers and their starting counters
        number_count_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}

        # Update how many of each are on the board
        for row in self.puzzleGrid:
            for number in row:
                if number != 0:
                    number_count_dict[number] += 1

        return number_count_dict

    def numCountDisplay(self):
        """
        When called, displays each number from the board along with the amount of times it is on the board.
        :return: None
        """
        # Call numberCount to create dictionary
        num_count_dict = self.numberCount()

        # initial x and y coordinates
        x = 150
        y = 500

        # Create and draw a white rectangle that erases the previous numCountDisplay before displaying the new one
        eraser_rect = pygame.Rect(x - 50, y - 10, 550, 100)
        pygame.draw.rect(self.SCREEN, self.WHITE, eraser_rect)

        # loop through the keys in the dictionary to display each of them, while updating x and y coordinates
        for int_key in num_count_dict.keys():
            # Create text surface for the number
            textSurface = self.FONT.render(str(int_key), False, (0, 0, 0))
            # Draw it on screen and update
            self.SCREEN.blit(textSurface, (x, y))
            pygame.display.update()
            # Move to next x coordinate
            x += 50

        # update x and y for smaller number counters
        x = 170
        y = 490

        # loop through every value in the dict to display each, while updating x and y coordinates
        for int_val in num_count_dict.values():
            # Create text surface for the number (smaller than previous)
            textSurface = self.smallFont.render(str(int_val), False, (0, 0, 0))
            # Draw on screen and update
            self.SCREEN.blit(textSurface, (x, y))
            pygame.display.update()
            # Move to next x coordinate
            x += 50



    def loadFullGame(self):
        """
        Creates title screen and starts game loop so the user need not call both methods to play the game
        :return: None
        """
        self.gameTitle()
        self.mainGameLoop()




game = SudokuGame()
game.loadFullGame()






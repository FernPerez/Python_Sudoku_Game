"""
Filename: SudokuBlockGenerator.py
Author: Fernando Perez
Date: July 29, 2021
"""

# import time and random libraries to use for time management and randomization
import random
import time

# Class that generates the complete Sudoku Grid when instantiated as an object.
class SudokuGridGenerator():

    def __init__(self):
        # Initialize variables that will store the data of the rows and columns
        self.rows = [[], [], [], [], [], [], [], [], []]
        # self.columns = [[], [], [], [], [], [], [], [], []]

        # fills every empty space on the grid with a 0.
        for row in self.rows:
            for i in range(0,9):
                row.append(0)

        # initialize variables for each respective 3x3 grid
        self.threeByThree0 = []
        self.threeByThree1 = []
        self.threeByThree2 = []

        # initialize variable for keeping track of time. This is to make sure the program doesn't end up looping
        # for too long
        self.startTime = time.time()

    def genThreeBlocks(self):
        """
        Method that randomly generates the top-left, middle, and bottom-right 3x3 squares. This is done to simplify the
        process, as these three blocks do not need to be compared to anything and are completely independent of each other
        The method goes through the appropriate columns of the appropriate row, left to right - top to bottom, selecting
        a random int value from a premade list of 1-9 and removing it from the list afterwards.
        Input: self
        Output: 2d array with 9 lists, each with 9 int elements. Elements 0-2 of lists 0-2, 3-5 of lists 3-5, and
            6-8 of lists 6-8 will be random integers that correspond with the rules of sudoku. Every other element is
            a 0.
        """

        # keep track of the column number. This will serve as the index.
        column_no = 0

        # initialize list variable with digits 1-9 by calling resetValues() method.
        pos_values = self.resetValues()

        # For the first three rows, the loop fills out the first three columns and then moves on to the next row.
        for row in self.rows[0:3]:
            # # print("row is ", row)
            while column_no < 3:
                # # print("column is ", column_no)
                # Choose a random number
                number = random.choice(pos_values)

                # Place the number in the space
                row[column_no] = number

                # Remove it from the list so it cannot be chosen again.
                pos_values.remove(number)

                # Move on to the next column
                column_no += 1
            # Reset the column index
            column_no = 0

        # Restore the values for the next 3x3
        pos_values = self.resetValues()

        # Does the same process as the previous loop, but fills in the middle columns of the next three rows
        for row in self.rows[3:6]:
            column_no = 3
            while column_no < 6:
                # # print("column is ", column_no)
                number = random.choice(pos_values)
                row[column_no] = number
                pos_values.remove(number)
                column_no += 1

        # Reset the values for the next 3x3
        pos_values = self.resetValues()

        # Same as last two loops, but for the last three columns of the last three rows.
        for row in self.rows[6:9]:
            column_no = 6
            while column_no < 9:
                # # print("column is ", column_no)
                number = random.choice(pos_values)
                row[column_no] = number
                pos_values.remove(number)
                column_no += 1

    def nextTwoBlocks(self):
        """
        Warning: Must be used after genThreeBlocks(), but before upAndDown() and leftAndRight
        Method that generates the top-right and bottom-left 3x3 squares. This will be a similar process to the previous
        method, but the process will need to compare each space to its corresponding row and column before filling in
        a number so as to avoid repeats and maintain Sudoku rules.
        Input: self
        :return: Same list that the genThreeBlocks() method returned, but elements 6-8 of lists 0-2 and elements 0-2 of
            lists 6-8  will now be random integers corresponding with the rules of sudoku.
        """

        # Keep track of column number for indexing
        column_no = 0

        # Have a fresh set of values to choose from
        pos_values = self.resetValues()

        # Start with first row
        row_no = 0

        # In this loop, the method will iterate through the first three rows in the grid and fill in the last three
        # columns. At every empty space, it will select a random number, compare it within the row (list) and column
        # (elements of other lists it shares its index with) to see if it is unique. If so, then add it and remove it
        # from the list. If not, keep looping until it gets one that is. If the program loops a certain amount of times,
        # it will assume that an appropriate solution for the space cannot be reached and will reset the entire 3x3 to
        # try again. Lastly, if the method takes too long to produce a result, it will return so as not to loop for too
        # long.
        while row_no < 3:
            # Make sure that the program is good on time. If not, exit.
            if self.toomuchTime():
                return
            # # print("Row number: ", row_no)
            # Variable that will be used to know if the loop had to reset the 3x3. This is so it can reset the
            # appropriate variables
            reset = False

            # select the column and row to start on.
            column_no = 6
            row = self.rows[row_no]

            # Loop through the last three columns of the chosen row and fill them in
            while 0 in row[6:9]:
                # # print("Column_no is ", column_no)
                # List variable that stores every element from the other rows that shares its index with the space we
                # are filling. This will be the column we compare to.
                column = []
                for rowCounter in self.rows:
                    column.append(rowCounter[column_no])
                # # print("Column is ", column)

                # variable to ensure we have a valid number and break from the loop if we do.
                valid = False
                # Keeps track of how many loops have been done.
                loopCount = 0

                # No valid number yet
                while valid == False:
                    # Choose a random number from the list
                    number = random.choice(pos_values)
                    # # print("Number is ", number)
                    # # print("Possible values: ", pos_values)
                    # Number is unique in its row and column
                    if number not in row and number not in column:
                        # Add the number and remove it from the list
                        row[column_no] = number
                        pos_values.remove(number)
                        # Move to next column and exit the loop.
                        column_no += 1
                        valid = True


                    # Looped too many times
                    if loopCount >= 50:
                        # # print("oops... Resetting block")
                        # Reset the whole 3x3 square and try again from the start.
                        self.backTracker(3, 1)
                        reset = True
                        break

                    # increase the amount of times the program has looped.
                    loopCount += 1

                # Tell the program that a reset has happened so as to restart fresh and correctly
                if reset == True:
                    # # print("returning to start...")
                    pos_values = self.resetValues()
                    row_no = -1 # -1 as this will be 0 when increased upon breaking the loop.
                    break

            # move to next row
            row_no += 1

        # finished with top-right, moving to bottom-left.
        # get a fresh set of values to choose from.
        pos_values = self.resetValues()
        # move to row 6
        row_no = 6

        # This loop does the same as the previous big loop, but with the first three elements of the last three lists.
        while row_no < 9:
            # print("Row number: ", row_no)
            reset = False

            # select the column and row to start on.
            column_no = 0
            row = self.rows[row_no]

            # Loop through the first three columns of the chosen row and fill them in
            while 0 in row[0:3]:
                # print("Column_no is ", column_no)
                # This will be the column we compare to.
                column = []
                for rowCounter in self.rows:
                    column.append(rowCounter[column_no])
                # print("Column is ", column)
                # variable to ensure we have a valid number and break from the loop if we do.
                valid = False
                # Keeps track of how many loops have been done.
                loopCount = 0

                # No valid number yet
                while valid == False:
                    # Choose a random number from the list
                    number = random.choice(pos_values)
                    # print("Number is ", number)
                    # print("Possible values: ", pos_values)
                    # Number is unique in its row and column
                    if number not in row and number not in column:
                        # Add the number and remove it from the list
                        row[column_no] = number
                        pos_values.remove(number)
                        # Move to next column and exit the loop.
                        column_no += 1
                        valid = True

                    # Looped too many times
                    if loopCount >= 50:
                        # print("oops... Resetting block")
                        # Reset the whole 3x3 square and try again from the start.
                        self.backTracker(1, 3)
                        reset = True
                        break

                    # increase the amount of times the program has looped.
                    loopCount += 1

                # Tell the program that a reset has happened so as to restart fresh and correctly
                if reset == True:
                    # print("returning to start...")
                    pos_values = self.resetValues()
                    row_no = 5 # 5 as this will be 6 when increased upon breaking the loop.
                    break

            # move to next row
            row_no += 1

    def upAndDown(self):
        """
        Warning: Must be used after nextTwoBlocks().
        Fills in the middle-top and middle-bottom 3x3 squares with random numbers following the rules of Sudoku.
        Input: self
        :return: same grid object that was returned from nextTwoBlocks(), but with top and bottom 3x3's filled in.
        """
        # keep track of column number for indexing.
        column_no = 3
        # Refresh list of values.
        pos_values = self.resetValues()
        # Keep track of row number
        row_no = 0

        # This loop works similarly to the ones in nextTwoBlocks(), but fills continuously loops until both the top
        # and bottom 3x3's are filled in correctly. The main difference is that if the loop gets stuck, it resets both
        # 3x3's from scratch, instead of the one it's on. This is because, as the grid gets more and more filled in,
        # the program is more likely to run out of options and not be able to find a solution that works. By resetting
        # both squares, it decreases that likelihood.
        while row_no < 9:
            # Boolean to determine if both squares will be reset.
            bigReset = False

            # Fill in the columns 3-5 (first column is 0) on the first three rows.
            while row_no < 3:
                # Took too long, exit.
                if self.toomuchTime():
                    return
                # print("Row number: ", row_no)
                # Boolean to determine if only the top square was reset.
                reset = False
                # Select apropriate column and row
                column_no = 3
                row = self.rows[row_no]

                # loop until the three spaces in the row are filled in
                while 0 in row[3:6]:
                    # print("Column_no is ", column_no)
                    # store the values of the column for comparison
                    column = []
                    for rowCounter in self.rows:
                        column.append(rowCounter[column_no])

                    # print("Column is ", column)
                    # variable to ensure we have a valid number and break from the loop if we do.
                    valid = False
                    # Keep track of how many loops.
                    loopCount = 0

                    # Loop until a valid number is found
                    while valid == False:
                        # Select a random number from the list
                        number = random.choice(pos_values)
                        # print("Number is ", number)
                        # print("Possible values: ", pos_values)

                        # If the number is unique to the row and column
                        if number not in row and number not in column:
                            # Place it in the row and remove it from the list.
                            row[column_no] = number
                            pos_values.remove(number)
                            # Move to the next column and exit the loop.
                            column_no += 1
                            valid = True

                        # Looped too many times
                        if loopCount >= 50:
                            # print("oops... Resetting block")
                            # Reset both 3x3 squares and exit the loop to start over
                            self.upDownBacktracker()
                            reset = True
                            break

                        # Increase the loop amount
                        loopCount += 1

                    # Squares were reset, refresh variables to start correctly again.
                    if reset == True:
                        # print("returning to start...")
                        pos_values = self.resetValues()
                        row_no = -1
                        break

                # Move to the next row after the previous is filled in.
                row_no += 1

            # Refresh the list of values for the next 3x3 square and move on to the 6th row
            pos_values = self.resetValues()
            row_no = 6
            # Same as before, loop until the bottom 3x3 is filled in
            while row_no < 9:
                # Took too long, exit.
                if self.toomuchTime():
                    return
                # print("Row number: ", row_no)
                # reset is used here to know when to break out of the loop and restart from the previous 3x3.
                reset = False

                # select the appropriate column and row to start with.
                column_no = 3
                row = self.rows[row_no]

                # Loop until values 3-5 of the row are filled in.
                while 0 in row[3:6]:
                    # print("Column_no is ", column_no)
                    # Store the values of the column
                    column = []
                    for rowCounter in self.rows:
                        column.append(rowCounter[column_no])

                    # print("Column is ", column)
                    # For checking if number was valid
                    valid = False
                    # Keep track of loops.
                    loopCount = 0

                    # Loop until a correct number is found.
                    while valid == False:
                        # Select a random number from the list.
                        number = random.choice(pos_values)
                        # print("Number is ", number)
                        # print("Possible values: ", pos_values)
                        # Number fits in the row and column
                        if number not in row and number not in column:
                            # Place it in the row and remove it from the list.
                            row[column_no] = number
                            pos_values.remove(number)

                            # Move to the next column and exit the loop.
                            column_no += 1
                            valid = True

                        # Looped for too long; reset both squares.
                        if loopCount >= 50:
                            # print("oops... Resetting block")
                            self.upDownBacktracker()
                            reset = True
                            bigReset = True
                            break

                        # Keep track of loops
                        loopCount += 1
                    # Exit the loop if a reset happened. This skips over to line 401.
                    if reset == True:
                        break
                # Move to the next row
                row_no += 1

                # Both squares were reset; start both from scratch.
                if bigReset == True:
                    # print("returning to THE VERY start...")
                    pos_values = self.resetValues()
                    row_no = 0
                    break

    def leftAndRight(self):
        """
        Warning: Must be used after nextTwoBlocks().
        Fills in the middle-left and middle-right 3x3 squares with random numbers following the rules of Sudoku.
        Input: self
        :return: same grid object that was returned from nextTwoBlocks(), but with left and right 3x3's filled in.
        """
        # keep track of column number for indexing.
        column_no = 0
        # Refresh list of values.
        pos_values = self.resetValues()
        row_no = 3

        # This loop works similarly to the ones in nextTwoBlocks(), but fills continuously loops until both the left
        # and right 3x3's are filled in correctly. The main difference is that if the loop gets stuck, it resets both
        # 3x3's from scratch, instead of the one it's on. This is because, as the grid gets more and more filled in,
        # the program is more likely to run out of options and not be able to find a solution that works. By resetting
        # both squares, it decreases that likelihood.
        while row_no < 6:
            # Boolean to determine if both squares will be reset.
            bigReset = False

            # Fill in the first three columns in rows 3-5 (first row is 0)
            while row_no < 6:
                # Took too long, exit.
                if self.toomuchTime():
                    return
                # print("Row number: ", row_no)
                # Boolean to determine if only the left square was reset.
                reset = False
                column_no = 0
                row = self.rows[row_no]
                while 0 in row[0:3]:
                    # print("Column_no is ", column_no)
                    # Store the values of the column
                    column = []
                    for rowCounter in self.rows:
                        column.append(rowCounter[column_no])

                    # print("Column is ", column)
                    # variable to ensure we have a valid number and break from the loop if we do.
                    valid = False
                    # Keep track of loops.
                    loopCount = 0

                    # Loop until a correct number is found.
                    while valid == False:
                        number = random.choice(pos_values)
                        # print("Number is ", number)
                        # print("Possible values: ", pos_values)
                        if number not in row and number not in column:
                            row[column_no] = number
                            pos_values.remove(number)
                            column_no += 1
                            valid = True

                        # Looped for too long; reset both squares.
                        if loopCount >= 50:
                            # print("oops... Resetting block")
                            self.leftRightBacktracker()
                            reset = True
                            break

                        loopCount += 1
                    # squares were reset, refresh variables to start from scratch
                    if reset == True:
                        # print("returning to start...")
                        pos_values = self.resetValues()
                        row_no = 2
                        break
                # Move to next row
                row_no += 1

            # Refresh values from list and move back to row 3 for the remainig squares
            pos_values = self.resetValues()
            row_no = 3

            # Same as before, loop until the bottom 3x3 is filled in
            while row_no < 6:
                # Took too long, exit.
                if self.toomuchTime():
                    return
                # print("Row number: ", row_no)
                reset = False

                # select the appropriate column and row to start with.
                column_no = 6
                row = self.rows[row_no]

                # Until the row is filled in
                while 0 in row[6:9]:
                    # print("Column_no is ", column_no)
                    # Store the values of the column
                    column = []
                    for rowCounter in self.rows:
                        column.append(rowCounter[column_no])
                    # print("Column is ", column)
                    valid = False
                    loopCount = 0

                    # Until a correct value is found
                    while valid == False:
                        # Choose a random number from the list
                        number = random.choice(pos_values)
                        # print("Number is ", number)
                        # print("Possible values: ", pos_values)
                        # Unique to row and column
                        if number not in row and number not in column:
                            # place it in the row and remove it from the list.
                            row[column_no] = number
                            pos_values.remove(number)
                            # Move to next column and exit the loop.
                            column_no += 1
                            valid = True

                        # Too many loops, reset both squares.
                        if loopCount >= 50:
                            # print("oops... Resetting block")
                            self.leftRightBacktracker()
                            reset = True
                            bigReset = True
                            break

                        loopCount += 1

                    if reset == True:
                        break

                row_no += 1

                # Start everything from scratch if reset happened.
                if bigReset == True:
                    # print("returning to THE VERY start...")
                    pos_values = self.resetValues()
                    row_no = 3
                    break

    def backTracker(self, x, y):
        """
        Method that resets every value in either the top-right or bottom-left 3x3 to 0 when called. Used to prevent
        getting stuck. x = 3 & y = 1 resets top-right. x = 1 & y = 3 resets bottom-left
        :param x: horizontal coordinate
        :param y: vertical coordinate
        :return: N/A
        """
        # print("previous grid:")
        # for row in self.rows:
            # print(row)
        # Reset top_right
        if x == 3 and y == 1:
            for row in self.rows[0:3]:
                column_no = 6
                for column in row[6:9]:
                    row[column_no] = 0
                    column_no += 1

        # Reset bottom-left
        elif x == 1 and y == 3:
            for row in self.rows[6:9]:
                column_no = 0
                for column in row[0:3]:
                    row[column_no] = 0
                    column_no += 1

    def upDownBacktracker(self):
        """
        Method that resets every value in the top-middle and bottom-middle 3x3's to 0 when called. Used to prevent
        getting stuck
        :return: N/A
        """
        # print("UPDOWNERROR")
        # print("previous grid:")
        # for row in self.rows:
            # print(row)
        # Reset top 3x3
        for row in self.rows[0:3]:
            column_no = 3
            for column in row[3:6]:
                row[column_no] = 0
                column_no += 1
        # Reset bottom 3x3
        for row in self.rows[6:9]:
            column_no = 3
            for column in row[3:6]:
                row[column_no] = 0
                column_no += 1

    def leftRightBacktracker(self):
        """
        Method that resets every value in the left-middle and right-middle 3x3's to 0 when called. Used to prevent
        getting stuck
        :return: N/A
        """
        # print("LEFTRIGHT")
        # print("previous grid:")
        # for row in self.rows:
            # print(row)
        # Reset left and right 3x3
        for row in self.rows[3:6]:
            column_no = 0
            for column in row[0:3]:
                row[column_no] = 0
                column_no += 1
            column_no = 6
            for column in row[6:9]:
                row[column_no] = 0
                column_no += 1

    def resetValues(self):
        """
        When called, refreshes the list of possible values to a shuffled list of integers from 1-9.
        :return: shuffled list of integers 1-9
        """
        pos_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        random.shuffle(pos_values)
        return pos_values

    def toomuchTime(self):
        """
        When called, evaluates if more than a second has passed since the object was created. This is to prevent
        the program from taking too long and will simply exit out if it does.
        :return: boolean to evaluate outside call.
        """
        currTime = time.time()
        if currTime - self.startTime > 1:
            return True











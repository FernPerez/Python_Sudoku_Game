# import random library for radnomization
import random

# define a class that will be used to create our grid and have methods to do so
class SudokuGrid():
    def __init__(self):
        # Initialize variables that will store the data of the rows and columns
        self.rows = [[], [], [], [], [], [], [], [], []]
        self.columns = [[], [], [], [], [], [], [], [], []]

        # initialize variables for each respective 3x3 grid
        self.threeByThree0 = []
        self.threeByThree1 = []
        self.threeByThree2 = []

        self.found = False

    # first method will create the first row of the grid
    def sudokuRow1(self):
        # keep track of the column number to be able to store the number in the appropriate column.
        column_no = 0

        # create a list of possible values that the program can select from
        pos_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # loop that will keep iterating until the row has been filled out with 9 numbers correctly
        while len(self.rows[0]) < 9:
            # pick a random number between 1 and 9 from the list
            number_to_add = random.choice(pos_values)

            # append it to the appropriate row and column
            self.rows[0].append(number_to_add)
            self.columns[column_no].append(number_to_add)

            # delete the value from the list and move to the next column
            pos_values.remove(number_to_add)
            column_no += 1

        # store the values from the rows in groups of three to know what numbers are in which 3x3 grid
        self.threeByThree0 = [number for number in self.rows[0][0:3]]
        self.threeByThree1 = [number for number in self.rows[0][3:6]]
        self.threeByThree2 = [number for number in self.rows[0][6:9]]
        print(self.threeByThree0)
        print(self.threeByThree1)
        print(self.threeByThree2)
        print("\n")


    # method that creates every other row in the grid
    def sudokuOtherRows(self):
        print("test")
        # keep track of what row in the 9x3 grid we are working with currently. This is to help us know whether we
        # need to check previous rows in the 3x3. It will start at 2 since it is the second row.
        rowInSquare = 2

        # iterate through and complete every row besides the first
        for row in self.rows[1:9]:
            # keep track of column number
            column_no = 0
            # keep list of possible values
            pos_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            # intialize/reset the loop count to 0. This in case the loop gets stuck.
            loopCount = 0

            # while loop that iterates through every space in the row to fill them in
            while len(row) < 9:
                # take note of the column by its number
                column = self.columns[column_no]
                loopCount += 1

                # select a random value from the list
                number_to_add = random.choice(pos_values)

                # boolean to see if the number fits later on
                fits = False

                # check to see if the number is not already in the row or column
                if number_to_add not in row and number_to_add not in column:
                    # if in the first row, no need to check 3x3 grid
                    if rowInSquare == 1:
                        fits = True

                    # if in the second or third row, make sure it isn't in the 3x3 grid
                    else:
                        # check what 3x3 it is on
                        # first 3x3
                        if column_no // 3 == 0 and number_to_add not in self.threeByThree0:
                            print(number_to_add, " fits in ", self.threeByThree0)
                            fits = True

                        # second 3x3
                        elif column_no // 3 == 1 and number_to_add not in self.threeByThree1:
                            print(number_to_add, " fits in ", self.threeByThree1)
                            fits = True

                        # third 3x3
                        elif column_no // 3 == 2 and number_to_add not in self.threeByThree2:
                            print(number_to_add, " fits in ", self.threeByThree2)
                            fits = True
                        else:
                            print("number ", number_to_add, " already in\n", loopCount)


                # no number fits, try to swap for another number in the row
                if loopCount >= 1000:
                    prev_number = number_to_add
                    print("no number works! ", number_to_add, "\n")
                    # call swap helper method
                    print("row ", row)
                    number_to_add = self.sudokuSwapper(number_to_add, row, column, column_no)

                    # make sure a good number was found, otherwise break
                    if self.found == False:
                        break

                    # otherwise, change fits to True and move on
                    else:
                        fits = True

                # check to see if the number works
                if fits == True:
                    # append number_to_add to both the respective row and column

                    row.append(number_to_add)
                    column.append(number_to_add)
                    print(self.rows.index(row))

                    print("After")
                    for row2 in self.rows:
                        print(row2)

                    # update column number and reset loop count
                    column_no += 1
                    loopCount = 0

                    if self.found == True:
                        pos_values.remove(prev_number)
                        self.found = False
                    else:
                        pos_values.remove(number_to_add)



            if fits == False:
                break

            # after the row is finished, add every 3 numbers to their respective 3x3 block
            for number in row[0:3]:
                self.threeByThree0.append(number)
            for number in row[3:6]:
                self.threeByThree1.append(number)
            for number in row[6:9]:
                self.threeByThree2.append(number)
            print("threeByThree0 = ", self.threeByThree0)
            print("threeByThree1 = ", self.threeByThree1)
            print("threeByThree2 = ", self.threeByThree2)
            print("\n")

            # if rowInSquare is 1 or 2, increase its value
            if rowInSquare < 3:
                rowInSquare += 1

            # otherwise, reset its value to 1 and reset every 3x3 grid for the next three rows
            else:
                rowInSquare = 1
                self.threeByThree0 = []
                self.threeByThree1 = []
                self.threeByThree2 = []


    # helper method that is used to swap numbers in a row to solve a conflict
    def sudokuSwapper(self, number_to_add, row, column, og_column_no):
        print("Before: ")
        for rowthing in self.rows:
            print(rowthing)
        print("swapping...\n")

        # create a variable for the column of the potential number to swap with
        column_no = 0
        # create a variable that will temporarily store the value to be swapped for
        temp_num = 0
        # boolean to let us know if a good number was swapped
        self.found = False

        og3x3 = self.threeByThreeFinder(og_column_no)

        print("row ", row)
        # loop through every number in the row to try swapping
        for swapNumber in row:
            print("SwapNumber is ", swapNumber)
            # know what column the number is in
            swapColumn = self.columns[column_no]
            print("swapcol", swapColumn)

            row_idx = row.index(swapNumber)
            col_idx = swapColumn.index(swapNumber)

            new3x3 = self.threeByThreeFinder(column_no)

            # check to make sure that the swapNumber is in the current column and that
            # the current number to be added isn't in the swapColumn
            if swapNumber not in column and number_to_add not in swapColumn:
                if swapNumber not in og3x3 and number_to_add not in new3x3:

                    print("\n\n CHANGED!!!! \n\n")
                    # swap the values
                    temp_num = swapNumber
                    print("temp", temp_num)

                    row[row_idx] = number_to_add
                    swapColumn[col_idx] = number_to_add
                    number_to_add = temp_num
                    print("num to add ", number_to_add)

                    self.found = True
                    break


            # otherwise, move to the next column
            else:
                column_no += 1

        return number_to_add

    def threeByThreeFinder(self, column):
        if column // 3 == 0:
            return self.threeByThree0
        elif column // 3 == 1:
            return self.threeByThree1
        else:
            return self.threeByThree2










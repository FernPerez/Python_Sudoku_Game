import random

# Row1 = []
# Row2 = []
# Row3 = []
# Row4 = []
# Row5 = []
# Row6 = []
# Row7 = []
# Row8 = []
# Row9 = []
rows = [[], [], [], [], [], [], [], [], []]
columns = [[], [], [], [], [], [], [], [], []]


def sudokuRow1(rows):
    column_no = 0
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    while len(rows[0]) < 9:
        number_to_add = random.choice(values)
        rows[0].append(number_to_add)
        columns[column_no].append(number_to_add)
        column_no += 1
        values.remove(number_to_add)
    # test()

def sudokuOtherRows(rows):
    row_number_in_square = 2
    for row in rows[1:9]:
        threeBlock = 0
        col_no = 0
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        loop = 0


        while len(row) < 9:
            loop += 1
            column = columns[col_no]
            number_to_add = random.choice(values)
            threeBlock = rows.index(row) // 3
            fits = False

            if number_to_add not in row and number_to_add not in column:
                fits = True

            #     elif row_number_in_square == 2:
            #         prev_row_idx = rows.index(row) - 1
            #         prev_row = rows
            #         if threeBlock == 0:
            #             if number_to_add not in rows[prev_row[0:3]]:
            #                 fits = True
            #         elif threeBlock == 1:
            #             if number_to_add not in rows[prev_row[3:6]]:
            #                 fits = True
            #         else:
            #             if number_to_add not in rows[prev_row[6:9]]:
            #                 fits = True
            #
            #     else:
            #         prev_row = rows[row - 1]
            #         prev2_row = rows[row - 2]
            #         if threeBlock == 0:
            #             if number_to_add not in rows[prev_row[0:3]] and number_to_add not in rows[prev2_row[0:3]]:
            #                 fits = True
            #         elif threeBlock == 1:
            #             if number_to_add not in rows[prev_row[3:6]] and number_to_add not in rows[prev2_row[3:6]]:
            #                 fits = True
            #         else:
            #             if number_to_add not in rows[prev_row[6:9]] and number_to_add not in rows[prev2_row[6:9]]:
            #                 fits = True
            #
            #
            elif loop > 10:
                print("test")
                number_to_add = sudokuIssueResolver(row, column, number_to_add)
                row.append(number_to_add)
                column.append(number_to_add)
                col_no += 1
                loop = 0

            if fits == True:
                row.append(number_to_add)
                column.append(number_to_add)
                col_no += 1
                values.remove(number_to_add)
                loop = 0


            test()

def sudokuIssueResolver(row, column, number_to_add):
    print("test")
    column_no = 0
    temp_num = 0
    for number in row:
        number_col = columns[column_no]
        idx = row.index(number)
        col_idx = number_col.index(number)
        if number not in column and number_to_add not in number_col:
            print("\n\n CHANGED!!!!!! \n\n")
            temp_num = number
            row[idx] = number_to_add
            number_col[col_idx] = number_to_add
            number_to_add = temp_num
            break
        else:
            column_no += 1
    return number_to_add

def test():
    print("rows:")
    for row in rows:
        print(row)
    print("columns:")
    for column in columns:
        print(column)


def main():
    sudokuRow1(rows)
    sudokuOtherRows(rows)
    print("\n Final result: \n")
    for row in rows:
        print(row)


main()
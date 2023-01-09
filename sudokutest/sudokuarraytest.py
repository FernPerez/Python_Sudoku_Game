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

def sudokuOtherRows(rows):
    for row in rows[1:9]:
        column_no = 0
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        while len(row) < 9:
            number_to_add = random.choice(values)
            # print("no: " , number_to_add)
            # print("Values: " , values)
            if number_to_add not in columns[column_no]:
                row.append(number_to_add)
                columns[column_no].append(number_to_add)
                # print(columns[column_no])
                column_no += 1
                values.remove(number_to_add)
            while len(values) == 1:
                sudokuResolver(row, number_to_add, columns[column_no])

def sudokuResolver(row, value, val_col):
    print("row is " , row)
    print("value is ", value)
    print("val_col", val_col)
    for number in row:
        column_no = row.index(number)
        if number not in val_col and value not in columns[column_no]:
            print("test")
            temp_num = value
            value = number
            row[number] = temp_num
            break
    return value



def main():
    sudokuRow1(rows)
    # print(columns)
    sudokuOtherRows(rows)
    for column in columns:
        print(column)


main()
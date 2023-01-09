# import the module
from SudokuBlockGenerator import SudokuGridGenerator

def main():
    grid = SudokuGridGenerator()
    numbers = []
    for row in grid.rows:
        for number in row:
            numbers.append(number)
    test = 0
    print("Generating Full Grid", end="")

    while 0 in numbers:
        numbers = []
        print(".", end = "")
        if test == 10:
            print("ERROR")
            break

        del(grid)
        grid = SudokuGridGenerator()
        grid.genThreeBlocks()
        grid.nextTwoBlocks()
        grid.upAndDown()
        grid.leftAndRight()
        for row in grid.rows:
            for number in row:
                numbers.append(number)
        test += 1

    print("\n")
    for row in grid.rows:
        print(row)


main()
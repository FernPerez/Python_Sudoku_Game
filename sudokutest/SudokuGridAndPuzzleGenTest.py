from GridByDifficultyGenerator import PuzzleByDifficultyGenerator

def main():
    puzzle = PuzzleByDifficultyGenerator()
    puzzle.gridGenerator()
    puzzle.difficulty_selector(puzzle.grid)
    while True:
        print("\n\n")
        for rowline in puzzle.grid.rows:
            print(rowline)
        row = int(input("Select row\n"))
        column = int(input("Select column\n"))
        spot = puzzle.grid.rows[row-1][column-1]
        if spot == 0:
            print("Change space ", row,  "x", column, " to?")
            answer = input()
            puzzle.grid.rows[row-1][column-1] = int(answer)
        else:
            print("Spot cannot be changed.")


main()

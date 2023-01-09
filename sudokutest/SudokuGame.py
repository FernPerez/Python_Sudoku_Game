"""
Filename: SudokuGame.py
Author: Fernando
Created: July 31, 2021
"""

import pygame
import sys
import time
import copy
from GridByDifficultyGenerator import PuzzleByDifficultyGenerator
from SudokuSquare import SudokuSquare
from SudokuGameTitle import TitleScreen

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (171, 215, 235)
GREY = (220, 220, 220)
RED = (255, 105, 97)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700
all_sprites = pygame.sprite.Group()

title = TitleScreen()
title.genScreen()
puzzleGrid = title.adjusted_grid
originalGrid = title.original_grid
greyed_out_squares = {}
for row in puzzleGrid:
    row_index = puzzleGrid.index(row)
    greyed_out_squares[row_index] = []
    for number in row:
        if number != 0:
            index = row.index(number)
            greyed_out_squares[row_index].append(index)

red_squares = {}


pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
time.sleep(0.1)
# pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
startTime = time.time()




def main():
    print('moved')
    global SCREEN, CLOCK, FONT, row_dict
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(WHITE)
    FONT = pygame.font.SysFont('Times New Roman', 30)
    running = True
    row_dict = {}
    loop = 1
    firstLoop = True
    event = 0

    pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    while running:
        clickedSquare = False
        puzzleDisplayer(firstLoop)
        drawGrid()
        drawText()
        drawThickLines()


        if loop == 1:
            event = pygame.event.wait()
        else:
            event = newEvent

        # for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN: # or event.type == pygame.MOUSEBUTTONUP:
            loop += 1
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                for row, columns in row_dict.items():
                    for rect in columns:
                        if rect.collidepoint(pos) and columns.index(rect) not in greyed_out_squares[row]:
                            print("clicked on ", row, "x", columns.index(rect))
                            squareSelect(rect, row, columns.index(rect))
                            clickedSquare = True
                            break
                if clickedSquare == False or placedNumber == True:
                    print("no")
                    loop = 1



        pygame.display.update()
        firstLoop = False



    for entity in all_sprites:
        SCREEN.blit(entity.surf, entity.rect)


def drawGrid():
    blocksize = 50
    x = 125
    y = 30
    row = 0
    while y < 460:
        row_dict[row] = []
        while x < 575:
            rect = pygame.Rect(x, y, blocksize, blocksize)


            row_dict[row].append(rect)

            pygame.draw.rect(SCREEN, BLACK, rect, 1)
            x += 50
        row += 1
        y += 50
        x = 125


def puzzleDisplayer(firstLoop):
    blocksize = 50
    x = 140
    y = 40
    for row in puzzleGrid:
        for number in row:
            if number != 0:
                if firstLoop == True:
                    grey_rect = pygame.Rect(x-15, y-10, blocksize, blocksize)
                    pygame.draw.rect(SCREEN, GREY, grey_rect)
                numSurface = FONT.render(str(number), False, (0, 0, 0))
                SCREEN.blit(numSurface, (x, y))

            x += 50
        y += 50
        x = 140


def drawThickLines():
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
    for line in line_dict:
        pygame.draw.rect(SCREEN, BLACK, line_dict[line])

    # print(row_dict)

def drawText():
    textSurface = FONT.render('Sudoku', False, (0,0,0))
    SCREEN.blit(textSurface, (300, 0))

def squareSelect(rect, row, column):
    global newEvent, placedNumber, startTime
    print("changing")

    pygame.event.set_allowed(pygame.KEYDOWN)
    pygame.event.set_allowed(pygame.KEYUP)
    placedNumber = False
    selected = True
    redSquare = False

    inner_rect = pygame.Rect(rect.x + 1, rect.y + 1, 48, 48)
    pygame.draw.rect(SCREEN, BLUE, inner_rect)
    drawThickLines()
    puzzleDisplayer(firstLoop=False)
    pygame.event.clear()

    while selected == True:
        pygame.display.update()
        event = pygame.event.wait()
        newEvent = event
        # for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN: # or event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selected = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    redSquare = inputChecker(1, row, column)
                    puzzleGrid[row][column] = 1
                    placedNumber = True
                    selected = False
                elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    redSquare = inputChecker(2, row, column)
                    puzzleGrid[row][column] = 2
                    placedNumber = True
                    selected = False
                elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    redSquare = inputChecker(3, row, column)
                    puzzleGrid[row][column] = 3
                    placedNumber = True
                    selected = False
                elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    redSquare = inputChecker(4, row, column)
                    puzzleGrid[row][column] = 4
                    placedNumber = True
                    selected = False
                elif event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    redSquare = inputChecker(5, row, column)
                    puzzleGrid[row][column] = 5
                    placedNumber = True
                    selected = False
                elif event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    redSquare = inputChecker(6, row, column)
                    puzzleGrid[row][column] = 6
                    placedNumber = True
                    selected = False
                elif event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    redSquare = inputChecker(7, row, column)
                    puzzleGrid[row][column] = 7
                    placedNumber = True
                    selected = False
                elif event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    redSquare = inputChecker(8, row, column)
                    puzzleGrid[row][column] = 8
                    placedNumber = True
                    selected = False
                elif event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    redSquare = inputChecker(9, row, column)
                    puzzleGrid[row][column] = 9
                    placedNumber = True
                    selected = False
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:

                    puzzleGrid[row][column] = 0
                    placedNumber = True
                    selected = False


    # print('Original: ')
    # for row in originalGrid:
    #     print(row)
    # print('\nAdjusted: ')
    # for row in puzzleGrid:
    #     print(row)
    redSquareRemover()
    inner_rect = pygame.Rect(rect.x + 1, rect.y + 1, 48, 48)

    if row not in red_squares or column not in red_squares[row]:
        pygame.draw.rect(SCREEN, WHITE, inner_rect)
    else:
        pygame.draw.rect(SCREEN, RED, inner_rect)

    # if redSquare == True:
    #     pygame.draw.rect(SCREEN, RED, inner_rect)

    drawThickLines()
    pygame.display.update()
    fullChecker()

def inputChecker(number, row, column):
    column_lst = []
    for rowIterator in puzzleGrid:
        for num in rowIterator:
            if rowIterator.index(num) == column:
                column_lst.append(num)
    print('column is: ', column_lst)

    threeByThreeLst = threeByThreeUpdater(row, column)
    print('Three by three is: ', threeByThreeLst)

    if number in puzzleGrid[row] or number in column_lst or number in threeByThreeLst:
        if row in red_squares:
            red_squares[row].append(column)
        else:
            red_squares[row] = [column]
        print('NUMBER WRONG')
        return True
    else:
        return False


def threeByThreeUpdater(row, column):
    threeByThreeList = []
    if row < 3:
        if column < 3:
            for rowIterator in puzzleGrid[0:3]:
                for number in rowIterator[0:3]:
                    threeByThreeList.append(number)
        elif column < 6:
            for rowIterator in puzzleGrid[0:3]:
                for number in rowIterator[3:6]:
                    threeByThreeList.append(number)
        else:
            for rowIterator in puzzleGrid[0:3]:
                for number in rowIterator[6:9]:
                    threeByThreeList.append(number)

    elif row < 6:
        if column < 3:
            for rowIterator in puzzleGrid[3:6]:
                for number in rowIterator[0:3]:
                    threeByThreeList.append(number)
        elif column < 6:
            for rowIterator in puzzleGrid[3:6]:
                for number in rowIterator[3:6]:
                    threeByThreeList.append(number)
        else:
            for rowIterator in puzzleGrid[3:6]:
                for number in rowIterator[6:9]:
                    threeByThreeList.append(number)

    else:
        if column < 3:
            for rowIterator in puzzleGrid[6:9]:
                for number in rowIterator[0:3]:
                    threeByThreeList.append(number)
        elif column < 6:
            for rowIterator in puzzleGrid[6:9]:
                for number in rowIterator[3:6]:
                    threeByThreeList.append(number)
        else:
            for rowIterator in puzzleGrid[6:9]:
                for number in rowIterator[6:9]:
                    threeByThreeList.append(number)

    return threeByThreeList

def redSquareRemover():
    if len(red_squares) > 0:
        removable_red_squares = {}
        for key, value in red_squares.items():
            for column in value:
                number = puzzleGrid[key][column]
                column_list = []
                for row in puzzleGrid:
                    column_list.append(row[column])

                three_by_three = threeByThreeUpdater(key, column)

                row_check = False
                column_check = False
                three_by_three_check = False

                if puzzleGrid[key].count(number) < 2 or number == 0:
                    row_check = True

                if column_list.count(number) < 2 or number == 0:
                    column_check = True

                if three_by_three.count(number) < 2 or number == 0:
                    three_by_three_check = True

                if row_check == True and column_check == True and three_by_three_check == True:
                    rect = row_dict[key][column]
                    inner_rect = pygame.Rect(rect.x + 1, rect.y + 1, 48, 48)
                    pygame.draw.rect(SCREEN, WHITE, inner_rect)
                    if key not in removable_red_squares:
                        removable_red_squares[key] = [column]
                    else:
                        removable_red_squares[key].append(column)

        for key, value in removable_red_squares.items():
            for column in value:
                if key in red_squares and column in red_squares[key]:
                    red_squares[key].remove(column)

                if len(red_squares[key]) < 1:
                    del red_squares[key]

        removable_red_squares = {}
        return



def fullChecker():
    rowCheck = False
    columnCheck = False
    threeByThreeCheck = False
    zeroCheck = False

    column_dict = {}
    for i in range(9):
        column_dict[i] = []
        for row in puzzleGrid:
            column_dict[i].append(row[i])

    three_by_three_dict = {}
    x = 0
    y = 0
    for i in range(9):
        three_by_three_to_add = threeByThreeUpdater(x, y)
        three_by_three_dict[i] = three_by_three_to_add
        x += 3
        if x == 9:
            x = 0
            y += 3

    for row in puzzleGrid:
        if len(set(row)) == len(row):
            rowCheck = True
        else:
            rowCheck = False
            break

    for key, value in column_dict.items():
        if len(set(value)) == len(value):
            columnCheck = True
        else:
            columnCheck = False
            break

    for key, value in three_by_three_dict.items():
        if len(set(value)) == len(value):
            threeByThreeCheck = True
        else:
            threeByThreeCheck = False
            break

    for row in puzzleGrid:
        if 0 not in row:
            zeroCheck = True
        else:
            zeroCheck = False
            break

    if rowCheck == True and columnCheck == True and threeByThreeCheck == True:
        if zeroCheck == True:
            print("yay!")
            winScreen()


def winScreen():
    #SCREEN.fill(WHITE)
    puzzleDisplayer(firstLoop=False)

    width = 300
    length = 100
    x = 200
    y = 400
    rect = pygame.Rect(x, y, width, length)
    inner_rect = pygame.Rect(x + 3, y + 3, width - 5, length - 5)
    pygame.draw.rect(SCREEN, BLACK, rect, 5)
    pygame.draw.rect(SCREEN, GREEN, inner_rect)

    textSurface = FONT.render('YOU WIN', False, (0, 0, 0))
    SCREEN.blit(textSurface, (285, 425))


    pygame.display.update()
    time.sleep(5)
    pygame.quit()
    sys.exit()















main()

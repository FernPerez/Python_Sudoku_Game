"""
Filename: SudokuGameTitle.py
Author: Fernando
Created: July 31, 2021
"""

import pygame
import sys
import time
from GridByDifficultyGenerator import PuzzleByDifficultyGenerator
from SudokuSquare import SudokuSquare
from GridByDifficultyGenerator import PuzzleByDifficultyGenerator
import copy

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (171, 215, 235)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700
all_sprites = pygame.sprite.Group()

class TitleScreen():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill(WHITE)
        self.FONT = pygame.font.SysFont('Times New Roman', 30)
        self.TITLEFONT = pygame.font.SysFont('Times New Roman', 80)
        self.SUBTITLEFONT = pygame.font.SysFont('Times New Roman', 20)
        self.running = True

    def genScreen(self):
        while self.running:
            self.startButton()
            self.title()
            pygame.display.update()
            event = pygame.event.wait()
            # for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if self.button.collidepoint(pos):
                        self.genPuzzle()
                        print("finished")
                        self.running = False


            pygame.display.update()


    def startButton(self):
        width = 300
        length = 100
        x = 200
        y = 400
        rect = pygame.Rect(x, y, width, length)
        inner_rect = pygame.Rect(x + 3, y + 3, width-5, length-5)
        pygame.draw.rect(self.SCREEN, BLACK, rect, 5)
        pygame.draw.rect(self.SCREEN, BLUE, inner_rect)
        self.button = rect
        self.startText()

    def startText(self):
        textSurface = self.FONT.render('START', False, (0, 0, 0))
        self.SCREEN.blit(textSurface, (300, 425))

    def title(self):
        textSurface = self.TITLEFONT.render('SUDOKU', False, (0, 0, 0))
        self.SCREEN.blit(textSurface, (185, 150))
        textSurface = self.SUBTITLEFONT.render('by Fernando Perez', False, (0,0,0))
        self.SCREEN.blit(textSurface, (260, 240))

    def genPuzzle(self):
        #self.SCREEN.fill(WHITE)
        # textSurface = self.FONT.render('Generating Puzzle...', False, (0, 0, 0))
        # self.SCREEN.blit(textSurface, (240, 240))
        # pygame.display.update()
        print("start")
        puzzle = PuzzleByDifficultyGenerator()
        puzzle.gridGenerator()
        self.original_grid = copy.deepcopy(puzzle.grid.rows)
        puzzle.mediumMode()
        self.adjusted_grid = puzzle.grid.rows




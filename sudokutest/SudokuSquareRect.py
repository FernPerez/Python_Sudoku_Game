"""
Filename: SudokuSquare.py
Author: Fernando
Created: July 31, 2021
"""

import pygame
import sys

WHITE = (255,0,255)

class SudokuSquare():
    def __init__(self):
        self.surf = pygame.Surface((50, 50))
        self.surf.fill(255, 0, 0)


    def clicked(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if self.collidepoint():
                    pass

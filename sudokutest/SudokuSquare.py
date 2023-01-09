"""
Filename: SudokuSquare.py
Author: Fernando
Created: July 31, 2021
"""

import pygame
import sys

WHITE = (255,0,255)

class SudokuSquare(pygame.sprite.Sprite):
    def __init__(self):
        # super(SudokuSquare, self).init()
        self.surf =pygame.Surface((50, 50))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect()





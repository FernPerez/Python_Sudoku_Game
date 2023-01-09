import pygame
import sys
from GridByDifficultyGenerator import PuzzleByDifficultyGenerator
from SudokuSquare import SudokuSquare

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_HEIGHT = 700
WINDOW_WIDTH = 700
all_sprites = pygame.sprite.Group()

def main():
    global SCREEN, CLOCK, FONT
    pygame.init()
    pygame.font.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    FONT = pygame.font.SysFont('Times New Roman', 30)
    running = True

    while running:
        square = SudokuSquare()
        all_sprites.add(square)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            pygame.display.update()

    for entity in all_sprites:
        SCREEN.blit(entity.surf, entity.rect)

main()
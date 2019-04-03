import sys
import pygame

if __name__ == "__main__":
    pygame.init()

    size = width, height = 800, 600
    offwhite = 242, 230, 217

    screen = pygame.display.set_mode(size)
    screen.fill(offwhite)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

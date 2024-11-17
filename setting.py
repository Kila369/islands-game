# COLORS (r, g, b)
import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOUR = DARKGREY


# game settings
TILESIZE = 16
ROWS = 30
COLS = 30
WIDTH = TILESIZE * ROWS
HEIGHT = TILESIZE * COLS
FPS = 60
TITLE = "Islands game"
NAVBAR_HEIGHT = 0  # Height for the navigation bar at the top
FONT_SIZE = 48

heart_image = pygame.transform.scale(pygame.image.load(os.path.join("assets","heart.png")), (20, 20))
pygame.font.init()

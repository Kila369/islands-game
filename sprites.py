import pygame
from setting import *

class Tile:
  def __init__(self, x, y, height):
    self.x, self.y = x * TILESIZE, y *TILESIZE
    self.height = height
    self.isLand = bool(height)
    self.islandId = -1;
    
  def draw(self, board_surface):
    color = self.get_color(self.height)
    pygame.draw.rect(board_surface, color, (self.x, self.y, TILESIZE, TILESIZE))
    
  def __repr__(self):
    return str(self.height)

  @staticmethod
  def get_color(height):
    if height < 0:
      return RED
    elif height == 0:
        return (0, 0, 128)  # Deep blue for water
    elif height < 250:
        # Transition from blue (water) to green (low hills)
        red = 194 + int(height / 250 * 61)  
        green = 178 + int(height / 250 * 77) 
        blue = 128 - int(height / 250 * 128) 
        return (red, green, blue)
    elif height < 500:
        # Transition from yellow to green (mid hills)
        red = 255 - int((height - 250) / 250 * 255)  
        green = 255 
        blue = 0  
        return (red, green, blue)
    elif height < 750:
        # Transition from green to brown (higher land)
        red = 128 + int((height - 500) / 250 * 127) 
        green = 255 - int((height - 500) / 250 * 128) 
        blue = int((height - 500) / 250 * 64)  
        return (red, green, blue)
    else:
        # Transition to white for the highest points (mountain peaks)
        gray = 255 - int((1000 - height) / 250 * 128)
        return (gray, gray, gray)

class Board:
  def __init__(self, list):
    self.board_surface = pygame.Surface((WIDTH, HEIGHT))
    self.board_list = [
      [Tile(col, row, list[row][col]) for row in range(len(list))] for col in range(len(list[0]))
    ]
    self.visited = []
    self.islandHeights = []

  def explore(self, x, y):
    current_tile = self.board_list[x][y]
    if (x, y) in self.visited:
      return (0, 0)

    self.visited.append((x,y))
    if not current_tile.isLand:
      return (0, 0)
    self.board_list[x][y].islandId = len(self.islandHeights)
    total_height = current_tile.height
    total_tiles = 1
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
        (0, -1),          (0, 1),     # Left, Right
        (1, -1), (1, 0), (1, 1)       # Bottom-left, Bottom, Bottom-right
    ]

    for dx, dy in neighbors:
      new_x = x + dx
      new_y = y + dy
      if not self.is_inside(new_x, new_y):
        continue
      exploreResult = self.explore(new_x, new_y)
      total_height += exploreResult[0]
      total_tiles += exploreResult[1]
          
    return (total_height, total_tiles)

  @staticmethod
  def is_inside(x, y):
    return 0 <= x < ROWS and 0 <= y < COLS
  
  def draw(self,screen):
    for row in self.board_list:
      for tile in row:
        tile.draw(self.board_surface)
      screen.blit(self.board_surface, (0, NAVBAR_HEIGHT))

  def display_board(self):
    for row in self.board_list:
      print(row)

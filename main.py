import pygame
import requests

from setting import *
from sprites import *
class Game:
  def __init__(self):
    self.screen = pygame.display.set_mode((WIDTH, HEIGHT + NAVBAR_HEIGHT))
    pygame.display.set_caption(TITLE)
    self.clock = pygame.time.Clock()
    self.height_list = self.getHeightsList()
    self.lives = 3
    self.level = 1
    self.allTimeAttempts = 0
    self.allTimeHits = 0
    self.allTimeAccuracy = 0
    self.shouldUpdate = True
    
  def getHeightsList(self):
    response = requests.get('https://jobfair.nordeus.com/jf24-fullstack-challenge/test')
    splitted_response = [x.split(" ") for x in response.text.split('\n')]
    height_list = [[int(item) for item in sublist] for sublist in splitted_response]
    return height_list
  
  def new(self):
    self.board = Board(self.height_list)
    # self.board.display_board()
    for x in range(ROWS):
      for y in range(COLS):
        result = self.board.explore(x, y)
        if result[1] > 0:
          self.board.islandHeights.append(result[0]/result[1])
          
  def run(self):
    self.playing = True
    while self.playing:
      self.clock.tick(FPS)
      self.events()
      if self.shouldUpdate:
        self.draw()
        self.shouldUpdate = False
    else:
      self.end_screen()
      
  def colorMiss(self, islandId):
    for x in range(ROWS):
      for y in range(COLS):
        if self.board.board_list[x][y].islandId == islandId:
          self.board.board_list[x][y].height = -1

  def draw(self):
    self.screen.fill(BGCOLOUR)
    self.board.draw(self.screen)
    for i in range(self.lives):
      self.screen.blit(heart_image, (i * 30, 0)) 
    self.show_text("Level " + str(self.level) + " of 10", WIDTH - 60, 12, 24)
    self.show_text("Accuracy " + str(self.allTimeAccuracy) + "%", WIDTH - 180, 12, 24)
    pygame.display.flip()

  def show_text(self, text, x= WIDTH // 2, y= HEIGHT // 2 + NAVBAR_HEIGHT // 2, font_size=FONT_SIZE):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(x, y))
    self.screen.blit(text_surface, text_rect)
    pygame.display.flip()

  def events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit(0)
        
      if event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = pygame.mouse.get_pos()
        mx //= TILESIZE
        my //= TILESIZE
        
        if event.button == 1:
          islandId = self.board.board_list[mx][my].islandId
          if islandId == -1:
            return
          self.allTimeAttempts += 1
          if self.board.islandHeights[islandId] == max(self.board.islandHeights):
            self.win = True
            self.playing = False
            self.allTimeHits += 1
          else:
            if islandId >= 0:
             self.colorMiss(islandId)
            self.lives -= 1
            if (self.lives == 0):
              self.win = False
              self.playing = False
          self.allTimeAccuracy = round(self.allTimeHits / self.allTimeAttempts * 100, 2)
          self.shouldUpdate = True
                
  def end_screen(self):
    if self.win:
      if self.level == 10:
        self.show_text('Victory! Click to play again')
        self.level = 1
      else:
        self.show_text('Correct! Click for next level')
        self.level += 1
    else:
       self.show_text('You lost! Click to restart')
       self.level = 1

    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          quit(0)
          
        if event.type == pygame.MOUSEBUTTONDOWN:
          self.lives = 3
          self.height_list = self.getHeightsList()
          self.shouldUpdate = True
          return

game = Game()
while True:
  game.new()
  game.run()
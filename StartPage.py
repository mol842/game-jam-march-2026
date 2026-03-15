import pygame
from Button import *

class StartPage:
  def __init__(self, game):
    self.game = game
    self.background = None
    try:
      self.background = pygame.image.load("images/start_background.png")
    except:
      pass 
    self.start_button = Button(0, 0, 800, 500, "", lambda: self.start_game())

  def start_game(self):
    self.game.start_room_select()

  def handle_event(self, event, game):
    self.start_button.handle_event(event, game)

  def draw(self, game):
    if self.background:
      game.screen.blit(self.background, (0, 0))
    else:
      # just use colour no picture yet yay
      game.screen.fill((100, 150, 200))
    
    font = pygame.font.Font(None, 48)
    text = font.render("START!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 250))
    game.screen.blit(text, text_rect)
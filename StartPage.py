import pygame
from Button import *

class StartPage:
  def __init__(self, game):
    self.game = game
    self.original_background = None
    game.set_background_image("start_background.png")
    self.start_button = Button(self.game, 0, 0, 800, 500, "", lambda: self.start_game())

  def start_game(self):
    self.game.start_intro_dialogue()

    # self.game.start_room_select()

  def handle_event(self, event, game):
    self.start_button.handle_event(event, game)

  def draw(self, game):    
    font = pygame.font.Font(None, 48)
    text = font.render("START!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(400, 250))
    game.screen.blit(text, text_rect)
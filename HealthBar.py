import pygame
from pygame.locals import Color

class HealthBar:
  def __init__(self, game, x, y, width, height, max_health, curr_health):
    self.game = game
    self.original_x = x
    self.original_y = y
    self.original_width = width
    self.original_height = height
    self.max_health = max_health
    self.curr_health = curr_health

    self.update_size()

  def update_size(self):
    self.x = self.original_x # * (self.game.width / 800.0)
    self.y = self.original_y  #* (self.game.height / 500.0)
    self.width = self.original_width #* (self.game.width / 800.0)
    self.height = self.original_height  #* (self.game.height / 500.0)

  def draw(self, game):
    self.update_size()
    ## LITERALLY JUST A GREEN AND RED RECTANGLE BUT ILL FIX ITTTTTT PROLLY
    # STOLE THIS FROM STACKOVERFLOW
    pygame.draw.rect(game.screen, Color(255, 0, 0), (self.x, self.y, self.width, self.height))
    if self.max_health > 0:
      health_width = (self.curr_health / self.max_health) * self.width
      pygame.draw.rect(game.screen, Color(0, 255, 0), (self.x, self.y, health_width, self.height))

  def update_health(self, new_health):
    self.curr_health = max(0, min(new_health, self.max_health))
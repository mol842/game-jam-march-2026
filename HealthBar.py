import pygame
from pygame.locals import Color

class HealthBar:
  def __init__(self, x, y, width, height, max_health, curr_health):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.max_health = max_health
    self.curr_health = curr_health

  def draw(self, game):
    ## LITERALLY JUST A GREEN AND RED RECTANGLE BUT ILL FIX ITTTTTT PROLLY
    # STOLE THIS FROM STACKOVERFLOW
    pygame.draw.rect(game.screen, Color(255, 0, 0), (self.x, self.y, self.width, self.height))
    if self.max_health > 0:
      health_width = (self.curr_health / self.max_health) * self.width
      pygame.draw.rect(game.screen, Color(0, 255, 0), (self.x, self.y, health_width, self.height))

  def update_health(self, new_health):
    self.curr_health = max(0, min(new_health, self.max_health))
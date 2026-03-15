import pygame
from pygame.locals import Color
import random

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

    self.shake_frames = 0
    self.shake_intensity = 0
    self.damage_popups = []


  def update_size(self):
    self.x = self.original_x # * (self.game.width / 800.0)
    self.y = self.original_y  #* (self.game.height / 500.0)
    self.width = self.original_width #* (self.game.width / 800.0)
    self.height = self.original_height  #* (self.game.height / 500.0)


  def update_health(self, new_health):
    if (new_health < self.curr_health):
      print("SHAKING")
      self.shake_frames = 60
      self.shake_intensity = 12

      self.damage_popups.append({
          'text': f'-{self.curr_health - new_health}',
          'x': self.x + self.width / 2,
          'y': self.y,
          'timer': 60
      })

    self.curr_health = max(0, min(new_health, self.max_health))


      
  def draw_simple(self, game):
    self.update_size()
    ## LITERALLY JUST A GREEN AND RED RECTANGLE BUT ILL FIX ITTTTTT PROLLY
    # STOLE THIS FROM STACKOVERFLOW
    pygame.draw.rect(game.screen, Color(255, 0, 0), (self.x, self.y, self.width, self.height))
    if self.max_health > 0:
      health_width = (self.curr_health / self.max_health) * self.width
      pygame.draw.rect(game.screen, Color(0, 255, 0), (self.x, self.y, health_width, self.height))

  def draw(self, game):
    self.update_size()

    offset_x = 0
    if self.shake_frames > 0:
      offset_x = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
      self.shake_frames -= 1
      self.shake_intensity = max(0, self.shake_intensity - 0.3)

    x = self.x + offset_x

    pygame.draw.rect(game.screen, (60, 20, 20), (x, self.y, self.width, self.height), border_radius=4)
    if self.max_health > 0:
      health_width = (self.curr_health / self.max_health) * self.width
      health_ratio = self.curr_health / self.max_health
      r = int(255 * (1 - health_ratio))
      g = int(200 * health_ratio)
      colour = (r, g, 40)
      pygame.draw.rect(game.screen, colour, (x, self.y, health_width, self.height), border_radius=4)
    pygame.draw.rect(game.screen, (200, 200, 200), (x, self.y, self.width, self.height), 2, border_radius=4)

    font = pygame.font.Font(None, int(28 * (game.height / 500.0)))
    for popup in self.damage_popups[:]:
      progress = 1 - (popup['timer'] / 60)
      draw_y = popup['y'] - progress * 40
      text = font.render(popup['text'], True, (255, 80, 80))
      text.set_alpha(min(255, popup['timer'] * 6))
      game.screen.blit(text, text.get_rect(center=(popup['x'], draw_y)))
      popup['timer'] -= 1
      if popup['timer'] <= 0:
        self.damage_popups.remove(popup)

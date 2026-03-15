import pygame
import json
import os
from HealthBar import HealthBar

class Enemy2:
  def __init__(self, data, game):
    self.game = game
    self.name = data.get('name', 'WHO KNOWS')
    self.description = data.get('description', 'WHO KNOWS')
    self.type = data.get('type', '???')
    self.type = data.get('relationship', '???')
    self.start_health = data.get('start_health', 100)
    self.curr_health = data.get('curr_health', self.start_health)
    self.original_x = data.get('x', 0)
    self.original_y = data.get('y', 0)
    self.original_width = data.get('width', 50)
    self.original_height = data.get('height', 50)
    self.image_path = data.get('image', '')

    self.battle_script = data.get('battles', [])
    
    self.attacks = self.battle_script[0]["your-moves"]
    self.attack_index = 0

    # NO IMAGE OH GOD MAGENTA CUBE TIME
    self.original_image = None
    if self.image_path:
      full_path = os.path.join('images', self.image_path)
      if os.path.exists(full_path):
        self.original_image = pygame.image.load(full_path)

    self.health_bar = HealthBar(self.game, 0, 0, 0, 0, self.start_health, self.curr_health)
    self.update_size()

  def update_size(self):
    self.x = self.original_x * (self.game.width / 800.0)
    self.y = self.original_y * (self.game.height / 500.0)
    self.width = self.original_width * (self.game.width / 800.0)
    self.height = self.original_height * (self.game.height / 500.0)

    if self.original_image:
      self.image = pygame.transform.scale(self.original_image, (int(self.width), int(self.height)))
    else:
      self.image = pygame.Surface((int(self.width), int(self.height)))
      self.image.fill((255, 0, 255))

    # HEALTH BAR
    self.health_bar.original_x = self.x
    self.health_bar.original_y = self.y - 15 * (self.game.height / 500.0)
    self.health_bar.original_width = self.width
    self.health_bar.original_height = 10 * (self.game.height / 500.0)
    self.health_bar.update_size()

  def draw(self, game):
    self.update_size()
    game.screen.blit(self.image, (self.x, self.y))
    self.health_bar.draw(game)

  def take_damage(self, damage):
    self.curr_health -= damage
    self.health_bar.update_health(self.curr_health)

  def heal(self, amount):
    self.curr_health += amount
    self.health_bar.update_health(self.curr_health)

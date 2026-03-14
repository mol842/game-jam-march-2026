import pygame
import json
import os
from HealthBar import HealthBar

class Enemy:
  def __init__(self, json_file):
    with open(json_file, 'r') as f:
      data = json.load(f)

    self.name = data.get('name', 'WHO KNOWS')
    self.description = data.get('description', 'WHO KNOWS')
    self.type = data.get('type', '???')
    self.start_health = data.get('start_health', 100)
    self.curr_health = data.get('curr_health', self.start_health)
    self.x = data.get('x', 0)
    self.y = data.get('y', 0)
    self.width = data.get('width', 50)
    self.height = data.get('height', 50)
    self.image_path = data.get('image', '')

    # NO IMAGE OH GOD MAGENTA CUBE TIME
    self.image = pygame.Surface((self.width, self.height))
    self.image.fill((255, 0, 255)) 

    if self.image_path:
      full_path = os.path.join('images', self.image_path)
      if os.path.exists(full_path):
        self.image = pygame.image.load(full_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    self.health_bar = HealthBar(self.x, self.y - 15, self.width, 10, self.start_health, self.curr_health)

  def draw(self, game):
    game.screen.blit(self.image, (self.x, self.y))
    self.health_bar.draw(game)

  def take_damage(self, damage):
    self.curr_health -= damage
    self.health_bar.update_health(self.curr_health)

  def heal(self, amount):
    self.curr_health += amount
    self.health_bar.update_health(self.curr_health)

  def act(self):
    # PLACEHOLDER ADD ACTUAL WHATEVER
    # self.heal(5)
    pass
import pygame
import json
import os
from HealthBar import HealthBar
import random
from utils import *

class Enemy2:
  def __init__(self, data, game):
    self.game = game
    self.name = data.get('name', 'WHO KNOWS')
    self.description = data.get('description', 'WHO KNOWS')
    self.type = data.get('type', '???')
    self.relationship = data.get('relationship', '???')
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

      full_path = os.path.join(resource_path('images'), self.image_path)
      print("LOADING ENEMY IMAGE", full_path)

      if os.path.exists(full_path):
        self.original_image = pygame.image.load(full_path)
      else:
        print("NO ENEMY IMAGE EXISTS")

    self.shake_frames = 0
    self.shake_intensity = 0
    self.damage_popups = [] 
    # {text, x, y, timer, amount}


    self.health_bar = HealthBar(self.game, 0, 0, 0, 0, self.name, self.start_health, self.curr_health)
    self.update_size()

  def update_size(self):
    self.x = self.original_x * (self.game.width / 800.0)
    self.y = self.original_y * (self.game.height / 500.0)
    self.width = self.original_width * (self.game.width / 800.0)
    self.height = self.original_height * (self.game.height / 500.0)

    if self.original_image:
      self.image = pygame.transform.smoothscale(self.original_image, (int(self.width), int(self.height)))
    else:
      self.image = pygame.Surface((int(self.width), int(self.height)))
      self.image.fill((255, 0, 255))

    # HEALTH BAR
    self.health_bar.original_x = self.x
    self.health_bar.original_y = self.y - 15 * (self.game.height / 500.0)
    self.health_bar.original_width = self.width
    self.health_bar.original_height = 10 * (self.game.height / 500.0)
    self.health_bar.update_size()

  def draw(self, game, scale=1.0, show_health=True):
    self.update_size()


    offset_x, offset_y = 0, 0
    if self.shake_frames > 0:
      offset_x = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
      offset_y = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
      self.shake_frames -= 1
      self.shake_intensity = max(0, self.shake_intensity - 0.3)


    if scale != 1.0:
        scaled_width = int(self.width * scale)
        scaled_height = int(self.height * scale)
        scaled_image = pygame.transform.smoothscale(self.image, (scaled_width, scaled_height))
        scaled_x = self.x - (self.width * (scale - 1) / 2)
        scaled_y = self.y - (self.height * (scale - 1) / 2)
        # game.screen.blit(scaled_image, (scaled_x, scaled_y))
        game.screen.blit(scaled_image, (scaled_x + offset_x, scaled_y + offset_y))

    else:
        # game.screen.blit(self.image, (self.x, self.y))
        game.screen.blit(self.image, (self.x + offset_x, self.y + offset_y))

    if show_health:
        self.health_bar.draw(game)


  def take_damage(self, damage):
    self.curr_health -= damage
    self.health_bar.update_health(self.curr_health)
    self.shake_frames = 20
    self.shake_intensity = 8
    self.damage_popups.append({
        'text': f'-{damage}',
        'x': self.x + self.width / 2,
        'y': self.y,
        'timer': 60  
    })


  def heal(self, amount):
    self.curr_health += amount
    self.health_bar.update_health(self.curr_health)

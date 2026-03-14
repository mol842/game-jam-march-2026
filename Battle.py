import pygame
import time
from Enemy import Enemy
from Button import Button

class Battle:
  def __init__(self, enemy_name, game):
    self.game = game
    # GET THE ENEMY FROM THE FILE
    self.enemy = Enemy(f"enemies/{enemy_name}.json")
    self.turn = 'player' 

    self.buttons = [
      Button(100, 350, 100, 50, "Attack", self.attack),
      Button(250, 350, 100, 50, "Yell", self.attack),
      Button(400, 350, 100, 50, "Cry",  self.attack)
    ]

  def attack(self):
    # PLACEHOLDERRRR
    print("PLAYER MOVED")
    self.enemy.take_damage(10)
    self.switch_turn()

  def switch_turn(self):
    if self.turn == 'player':
      self.turn = 'enemy'
    else:
      self.turn = 'player'

    print("TURN NOW:", self.turn)

  def handle_event(self, event):
    if self.turn == 'player':
      for button in self.buttons:
        button.handle_event(event, self.game)

  def update(self):
    if self.turn == 'enemy':
      self.enemy.act()
      self.switch_turn()

  def draw(self, game):
    self.enemy.draw(game)
    if self.turn == 'player':
      for button in self.buttons:
        button.draw(game)


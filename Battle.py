import pygame
import time
from Enemy import Enemy
from Button import Button

class Battle:
  def __init__(self, enemy_name, game):
    self.game = game
    # GET THE ENEMY FROM THE FILE
    self.enemy = Enemy(f"enemies/{enemy_name}.json")
    # self.battle_script = self.enemy["battles"][0]
    self.battle_script = self.enemy.battle_script[0]

    self.turn = 'player' 
    self.enemy_action_time = 0
    

    self.show_popup = False
    self.popup_message = ""
    self.popup_timer = 0
    self.popup_button = Button(100, 150, 300, 300, "POPUP", None)
    self.popup_button.clickable = False

    self.buttons = [
      Button(100, 350, 100, 50, "Attack", self.attack),
      Button(250, 350, 100, 50, "Yell", self.attack),
      Button(400, 350, 100, 50, "Cry",  self.attack)
    ]

  def start_intro(self):
    self.battle_script["intro"]
    pass


  def attack(self):
    # PLACEHOLDERRRR
    print("PLAYER MOVED")

    self.popup_message = "You used Attack"
    self.show_popup = True
    self.popup_timer = time.time() + 2
    self.popup_button.set_text(self.popup_message)
    # self.switch_turn()

    self.enemy.take_damage(10)

  def switch_turn(self):
    if self.turn == 'player':
      self.turn = 'enemy'
      self.enemy_action_time = time.time() + 1
    elif self.turn == 'enemy':
      self.turn = 'player'
      self.enemy_action_time = 0

    print("TURN NOW:", self.turn)

  def handle_event(self, event):
    if self.turn == 'player' and not self.show_popup:
      for button in self.buttons:
        button.handle_event(event, self.game)

  def update(self):
    # if self.turn == 'enemy' and self.enemy_action_time == 0:
    #   self.enemy_action_time = time.time() + 2
    if self.turn == 'enemy' and time.time() >= self.enemy_action_time and not self.show_popup:
      self.enemy_act()
      # self.switch_turn()

    if self.show_popup and time.time() > self.popup_timer:
      self.show_popup = False
      self.switch_turn()

  def enemy_act(self):
    # PLACEHOLDERRR
    print("ENEMY ACTED")
    self.popup_message = "Enemy used PLACEHOLDER ATTACKKKKKK"
    self.show_popup = True
    self.popup_timer = time.time() + 2
    self.popup_button.set_text(self.popup_message)

  def draw(self, game):
    self.enemy.draw(game)

    if self.show_popup:
      self.popup_button.draw(self.game)

    elif self.turn == 'player':
      for button in self.buttons:
        button.draw(game)



import pygame
import time
import json
from Enemy2 import Enemy2
from Button import Button
from HealthBar import HealthBar

class Battle2:
  def __init__(self, enemy_name, game):
    self.game = game
    with open(f"enemies/{enemy_name}.json", 'r') as f:
      self.data = json.load(f)
    self.enemy = Enemy2(self.data)
    self.battle_script = self.data['battles'][0]

    self.stage = "intro"
    self.player_health = 100
    self.player_health_bar = HealthBar(100, 400, 200, 20, 100, self.player_health)

    self.turn = 'player'
    self.enemy_action_time = 0

    self.move_buttons = {}
    self.move_indices = {}

    ## MAKE THE BUTTONS
    move_names = ["Facts & Logic", "Blatant Lie", "Emotional Manipulation", "Unnecessary Escalation"]
    positions = [(100, 350), (250, 350), (400, 350), (100, 420)]
    for i, move_name in enumerate(move_names):
      if move_name in self.battle_script["your-moves"]:
        x, y = positions[i]
        self.move_buttons[move_name] = Button(x, y, 120, 50, move_name, lambda mn=move_name: self.player_move(mn))
        self.move_indices[move_name] = 0

    self.their_moves = self.battle_script["their-moves"]
    self.their_move_index = 0

    # HARDCODING INTERMISSIONS WE LIVE IN HELL
    self.intermission_50_triggered = False
    self.intermission_25_triggered = False
    self.pending_response = None


  def start_intro(self):
    print("STARTING THE INTRO")
    self.game.dialogue_box.init_dialogue(self.battle_script["intro"], lambda: self.set_stage("battle"))

  def player_move(self, move_name):
    if self.move_indices[move_name] < len(self.battle_script["your-moves"][move_name]):
      move_data = self.battle_script["your-moves"][move_name][self.move_indices[move_name]]
      self.pending_response = move_data["response"]
      self.enemy.take_damage(move_data["damage"])
      self.game.dialogue_box.init_dialogue([{"speaker": "You", "text": move_data["description"]}], lambda: self.show_response())
      print("SHOWING YOUR MOVE")

      
      self.move_indices[move_name] += 1
      if self.move_indices[move_name] >= len(self.battle_script["your-moves"][move_name]):
        self.move_buttons[move_name].hide()

  def show_response(self):
    print("SHOWING THEIR RESPONSE")
    self.game.dialogue_box.init_dialogue([{"speaker": "Fred", "text": self.pending_response}], lambda: self.switch_turn())
    self.pending_response = None
    self.game.dialogue_box.show()

  def set_stage(self, stage):
    self.stage = stage

  def switch_turn(self):
    if self.turn == 'player':
      self.turn = 'enemy'
    else:
      self.turn = 'player'

  def update(self):
    if self.stage == "intro":
      # print("YOURE IN THE INTRO")
      # ONCE THE DIALOGUE IS DONE BASICALLY
      if not self.game.dialogue_box.dialogue_list:
        self.stage = "battle"
        # print("FINISHED THE INTRO")

    elif self.stage == "battle":

      ## HEALTH CUTSCENES
      if self.enemy.curr_health <= (0.5 * self.enemy.start_health) and not self.intermission_50_triggered and not self.game.dialogue_box.dialogue_list:
        self.intermission_50_triggered = True
        self.stage = "intermisison-50%"
        self.game.dialogue_box.init_dialogue(self.battle_script["intermisison-50%"], lambda: self.set_stage("battle"))
      
      elif self.enemy.curr_health <= (0.25 * self.enemy.start_health) and not self.intermission_25_triggered and not self.game.dialogue_box.dialogue_list:
        self.intermission_25_triggered = True
        self.stage = "intermisison-25%"
        self.game.dialogue_box.init_dialogue(self.battle_script["intermisison-25%"], lambda: self.set_stage("battle"))

      ## WIN / LOSE!
      elif self.enemy.curr_health <= 0 and not self.game.dialogue_box.dialogue_list:
        self.stage = "end"
        self.game.dialogue_box.init_dialogue(self.battle_script["win"])
      elif self.player_health <= 0 and not self.game.dialogue_box.dialogue_list:
        self.stage = "end"
        self.game.dialogue_box.init_dialogue(self.battle_script["lose"])
      else:
        if self.turn == 'enemy' and not self.game.dialogue_box.dialogue_list:
          self.enemy_act()
    elif self.stage == "end":
      if not self.game.dialogue_box.dialogue_list:
        # enddddd battle
        pass

  def enemy_act(self):
    move = self.their_moves[self.their_move_index]
    self.game.dialogue_box.init_dialogue([{"speaker": self.enemy.name, "text": move["description"]}], lambda: self.switch_turn())
    self.player_health -= move["damage"]
    self.player_health_bar.update_health(self.player_health)
    self.their_move_index = (self.their_move_index + 1) % len(self.their_moves)

  def switch_turn(self):
    if self.turn == 'player':
      self.turn = 'enemy'
    else:
      self.turn = 'player'

  def handle_event(self, event):
    if self.stage == "battle" and self.turn == 'player' and not self.game.dialogue_box.dialogue_list:
      for btn in self.move_buttons.values():
        if btn.clickable:
          btn.handle_event(event, self.game)

  def draw(self, game):
    if (self.stage != "end"):
      self.enemy.draw(game)
      self.player_health_bar.draw(game)
      if self.stage == "battle" and self.turn == 'player' and not self.game.dialogue_box.dialogue_list:
        for btn in self.move_buttons.values():
          if btn.clickable:
            btn.draw(game)
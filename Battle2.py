import pygame
import time
import json
from Enemy2 import Enemy2
from Button import Button
from HealthBar import HealthBar
from PopupConfirm import Popup

class Battle2:
  def __init__(self, enemy_name, game, end_callback=None):
    self.game = game
    self.end_callback = end_callback
    with open(f"enemies/{enemy_name}.json", 'r') as f:
      self.data = json.load(f)
    self.enemy = Enemy2(self.data, self.game)
    self.battle_script = self.data['battles'][0]

    self.stage = "intro"
    self.player_start_health = 10
    self.player_health = self.player_start_health
    self.player_health_bar = HealthBar(self.game, 100, 100, 300, 40, "Your Health", self.player_start_health, self.player_health)

    self.result_popup = None
    self.won = None
    self.turn = 'player'
    self.enemy_moveion_time = 0

    self.move_buttons = {}
    self.move_indices = {}

    ## MAKE THE BUTTONS
    move_names = ["Facts & Logic", "Blatant Lie", "Emotional Manipulation", "Unnecessary Escalation"]
    button_width = 300
    button_height = 50
    start_y = 100
    x = 100
    for i, move_name in enumerate(move_names):
      if move_name in self.battle_script["your-moves"]:
        # x, y = positions[i]
        self.move_buttons[move_name] = Button(self.game, x, start_y + i*(button_height + 20), button_width, button_height, move_name, lambda mn=move_name: self.player_move(mn))
        # self.move_buttons[move_name] = Button(x, y, 120, 50, move_name, lambda mn=move_name: self.player_move(mn))
        self.move_indices[move_name] = 0

    self.their_moves = self.battle_script["their-moves"]
    self.their_move_index = 0

    # HARDCODING INTERMISSIONS WE LIVE IN HELL
    self.intermission_50_triggered = False
    self.intermission_25_triggered = False
    self.pending_response = None


  def start_intro(self):
    print("STARTING THE INTRO")
    # reset health because annoyingly it sometimes persists
    self.enemy.curr_health = self.enemy.start_health
    self.player_health = self.player_start_health
    self.game.dialogue_box.init_dialogue(self.battle_script["intro"], lambda: self.set_stage("battle"))

  def player_move(self, move_name):

    if self.move_indices[move_name] < len(self.battle_script["your-moves"][move_name]):
      move_info = self.battle_script["your-moves"][move_name][self.move_indices[move_name]]
      self.pending_response = move_info["response"]
      self.enemy.take_damage(move_info["damage"])
      if "dialogue" in move_info:
        self.game.dialogue_box.init_dialogue(move_info["dialogue"], lambda: self.show_response())
      else:
       self.game.dialogue_box.init_dialogue([{"speaker": "You", "text": move_info["description"]}], lambda: self.show_response())
      print("SHOWING YOUR MOVE")

      
      self.move_indices[move_name] += 1
      if self.move_indices[move_name] >= len(self.battle_script["your-moves"][move_name]):
        self.move_buttons[move_name].hide()

  def enemy_move(self):
    move_info = self.their_moves[self.their_move_index]
    if "dialogue" in move_info:
      self.game.dialogue_box.init_dialogue(move_info["dialogue"], lambda: self.switch_turn())
    else:
      self.game.dialogue_box.init_dialogue([{"speaker": "Narrator", "text": move_info["description"]}], lambda: self.switch_turn())

    self.game.dialogue_box.show()
    print("ENEMY MOVED!")

    # TAKE DAMAGE
    self.player_health -= move_info["damage"]
    self.player_health_bar.update_health(self.player_health)
    self.their_move_index = (self.their_move_index + 1) % len(self.their_moves)



  def show_response(self):
    # print("SHOWING THEIR RESPONSE")
    # self.game.dialogue_box.init_dialogue([{"speaker": self.enemy.name, "text": self.pending_response}], lambda: self.switch_turn())

    # self.pending_response = None
    # self.game.dialogue_box.show()
    self.switch_turn()

  def set_stage(self, stage):
    print("SETTING THE STAGE FOOORRRR", stage)
    self.stage = stage

  def switch_turn(self):
    print("SWITCHING TURN")
    if self.turn == 'player':
      self.turn = 'enemy'
      print("ENEMY MOVE!")

    else:
      self.turn = 'player'
      print("YOUR MOVE!")


  def update(self):
    if self.stage == "intro":
      # print("YOURE IN THE INTRO")
      # ONCE THE DIALOGUE IS DONE BASICALLY
      if not self.game.dialogue_box.dialogue_list:
        self.stage = "battle"
        print("FINISHED THE INTRO")

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
        self.won = True
        self.game.dialogue_box.init_dialogue(self.battle_script["win"])

        self.game.update_score(True, self.enemy.name)
      elif self.player_health <= 0 and not self.game.dialogue_box.dialogue_list:
        self.stage = "end"
        self.won = False
        self.game.dialogue_box.init_dialogue(self.battle_script["lose"])
        self.game.update_score(False, self.enemy.name)

      else:
        if self.turn == 'enemy' and not self.game.dialogue_box.dialogue_list:
          self.enemy_move()

    elif self.stage == "end":
      if not self.game.dialogue_box.dialogue_list:
        if not self.result_popup:
          self.result_popup = Popup.result(self.game, self.enemy.name, self.won)
        if self.result_popup and not self.result_popup.visible:
          self.result_popup = None
          if self.end_callback:
            self.end_callback()
          else:
            self.stage = "stopped"
            self.game.start_room_select()


  def handle_event(self, event):
    if self.result_popup:
      self.result_popup.handle_event(event, self.game)
    if self.stage == "battle" and self.turn == 'player' and not self.game.dialogue_box.dialogue_list:
      for btn in self.move_buttons.values():
        if btn.clickable:
          btn.handle_event(event, self.game)

  def draw(self, game):
    # print(self.stage)
    if (self.stage != "stopped"):
      # scale = 2.0 if self.game.dialogue_box.visible else 1.0
      scale = 1.0
      show_health = True
      if self.game.dialogue_box.visible and self.stage != "battle" and self.stage !="intermisison-50%":
        show_health = False
        scale = 2.0
      self.enemy.draw(game, scale=scale, show_health=show_health)


      if self.stage == "battle" or self.stage =="intermisison-50%":
        self.player_health_bar.draw(game)
        if self.turn == 'player' and not self.game.dialogue_box.dialogue_list:
          for btn in self.move_buttons.values():
            if btn.clickable:
              btn.draw(game)

    if self.result_popup:
      self.result_popup.draw(self.game)

import pygame
from Button import *
from Battle2 import *

class RoomSelect:
  def __init__(self, game):
    self.game = game
    self.visited_rooms = [False, False, False, False]
    self.current_room = None
    self.room_enemies = [
      ["fred", "fred", "fred"],
      ["fred", "fred", "fred"],
      ["fred", "fred", "fred"] ,
      ["fred", "fred", "fred"]
    ]
    self.current_enemy_index = 0
    
    self.room_buttons = []
    ### SQUARE OF BUTTTONSNSSS
    for i in range(4):
      button = Button(200 + (i % 2) * 200, 150 + (i // 2) * 100, 150, 50, f"Room {i+1}", lambda idx=i: self.start_room(idx))
      self.room_buttons.append(button)
    
    # PROCEED BUTTON BUT HIDDEN (REVEALED WHEN YOUVE DONE ALL THE ROOMS)
    self.proceed_button = Button(350, 400, 100, 50, "Proceed", self.go_to_end)
    # self.proceed_button.hide()

  def start_room(self, room_index):
    if not self.visited_rooms[room_index]:
      self.visited_rooms[room_index] = True
      self.room_buttons[room_index].disable()
      self.room_buttons[room_index].set_text(f"Room {room_index+1}\n(VISITED)")
      self.current_room = room_index
      self.current_enemy_index = 0
      self.start_next_battle()
      
      # Check if all rooms visited
      if all(self.visited_rooms):
        self.proceed_button.show()

  def start_next_battle(self):
    if self.current_room is not None and self.current_enemy_index < len(self.room_enemies[self.current_room]):
      print("STARTING BATTLE",self.current_enemy_index, "FOR ROOM", self.current_room)
      enemy_name = self.room_enemies[self.current_room][self.current_enemy_index]
      self.game.battle = Battle2(enemy_name, self.game, self.battle_ended)
      self.game.battle.start_intro()
      self.game.mode = "battle"
      self.current_enemy_index += 1

  def battle_ended(self):
    # Called when a battle ends, start next enemy or return to room select
    if self.current_enemy_index < 3:
      self.start_next_battle()
    else:
      self.game.mode = "room_select"

  def go_to_end(self):
    print("STARTING END SCREEN")
    self.game.start_end_screen()

  def handle_event(self, event, game):
    for button in self.room_buttons:
      button.handle_event(event, game)
    if self.proceed_button.visible:
      self.proceed_button.handle_event(event, game)

  def draw(self, game):
    game.screen.fill((50, 50, 50))
    
    # TITLE
    font = pygame.font.Font(None, 36)
    title = font.render("Select a Room", True, (255, 255, 255))
    game.screen.blit(title, (350, 50))
    
    # ROOM BUTTONS
    # CHANGE TO BE AN IMAGE WHEN I HAVE ONE
    for button in self.room_buttons:
      button.draw(game)

    # ENEMY NAMES JUST FOR DEBUGGING
    small_font = pygame.font.Font(None, 20)
    for i in range(4):
      enemy_text = f"Enemies: {', '.join(self.room_enemies[i])}"
      text = small_font.render(enemy_text, True, (200, 200, 200))
      game.screen.blit(text, (200 + (i % 2) * 200, 210 + (i // 2) * 100))
    
    self.proceed_button.draw(game)
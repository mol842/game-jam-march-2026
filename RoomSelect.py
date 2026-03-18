import pygame
from Button import *
from Battle2 import *
from PopupConfirm import Popup
import math
class RoomSelect:
  def __init__(self, game):
    self.game = game

    # using for colours
    self.font_mapping = json.load(open('fonts/font_mapping.json'))

    self.visited_rooms = [False, False, False, False]
    # photo names are also uhhhhhhhhh the same .png
    # self.room_names = ["lounge", "library", "patio", "kitchen"]
    # self.current_room = None
    # self.room_enemies = [
    #   ["Louis", "Linh"],
    #   ["Quân", "Lia"],
    #   ["Caspian", "fred"] ,
    #   ["Thi Há", "fred"]
    # ]

    self.current_room = None
    self.visited_rooms = [False, False, False, False, False, False]
    self.room_enemies = [
      ["Louis"],
      ["Linh"],
      ["Lia"],
      ["Caspian"] ,
      ["Thi Há"],
      ["Quân"],
    ]
    self.room_names = [
      "Lounge",
      "Library",
      "Kitchen",
      "Study" ,
      "Dining Room",
      "Patio",
    ]

    self.room_enemies = [
      ["Caspian"] ,
      ["Linh"],

      ["Quân"],
      ["Lia"],

      ["Louis"],
      ["Thi Há"],
    ]
    self.room_names = [
      "Study" ,
      "Library",

      "Patio",
      "Kitchen",

      "Lounge",
      "Dining Room",
    ]


    self.current_enemy_index = 0

    # MUST VISIT IN ORDERRRR
    self.prerequisites = {
        "Linh": "Caspian",
        "Lia": "Quân",
        "Thi Há": "Louis"
    }
    self.enemy_to_room = {self.room_enemies[i][0]: i for i in range(len(self.room_enemies))}


    # self.room_buttons = []
    # ### SQUARE OF BUTTTONSNSSS
    # for i in range(4):
    #   button = Button(self.game, 200 + (i % 2) * 200, 150 + (i // 2) * 100, 150, 50, self.room_names[i], lambda idx=i: self.start_room(idx))
    #   self.room_buttons.append(button)
    
    # # PROCEED BUTTON BUT HIDDEN (REVEALED WHEN YOUVE DONE ALL THE ROOMS)
    # self.proceed_button = Button(self.game, 300, 400, 200, 50, "Leave the party", self.handle_proceed_click, color=(48, 25, 52))
    # # self.proceed_button.hide()
    # self.popup = None

    # semicircle of buttons
    self.room_buttons = []
    num_rooms = len(self.room_names)
    btn_w, btn_h = 130, 100
 
    start_angle = math.radians(200)
    end_angle   = math.radians(340)
    # oh god
    cx, cy = 400, 410   # centre of the arc (raw 800x500 coords)
    rx, ry = 325, 300   # horizontal and vertical radii
 
    for i in range(num_rooms):
      t = i / (num_rooms - 1)
      angle = start_angle + t * (end_angle - start_angle)
      bx = cx + rx * math.cos(angle) - btn_w / 2
      by = cy + ry * math.sin(angle) - btn_h / 2

      button_colour = (99,99,99)
      font = None
      if self.room_enemies[i][0] in self.font_mapping:
        button_colour = eval(self.font_mapping[self.room_enemies[i][0]]["box-colour"])
        font = self.font_mapping[self.room_enemies[i][0]]['font']
      button = Button(
        self.game, bx, by, btn_w, btn_h,
        self.room_names[i],
        lambda idx=i: self.start_room(idx),
        color=button_colour,
        font=font,
        font_size=22
      )
      enemy = self.room_enemies[i][0]
      if enemy in self.prerequisites:
        button.disable()
        gray = sum(button_colour) / 3
        desaturated_color = tuple(int(c * 0.1 + gray * 0.9) for c in button_colour)
        button.color = desaturated_color  # locked color
        button.set_text(f"{self.room_names[i]}\n(LOCKED)")
      self.room_buttons.append(button)
 
    self.proceed_button = Button(
      self.game, 400 - 100, 440, 200, 45,
      "Leave the party", self.handle_proceed_click,
      color=(48, 25, 52)
    )
    self.popup = None
 



  def start_room(self, room_index):
    enemy_name = self.room_enemies[room_index][0]
    if enemy_name in self.prerequisites:
      prereq = self.prerequisites[enemy_name]
      prereq_room = self.enemy_to_room[prereq]
      if not self.visited_rooms[prereq_room]:
        message = f"This room is locked until you visit {prereq} in the {self.room_names[prereq_room]}."
        self.popup = Popup.confirm(self.game, message, "OK", "OK", self.close_popup, self.close_popup)
        return
    if not self.visited_rooms[room_index]:
      self.visited_rooms[room_index] = True
      self.room_buttons[room_index].disable()

      self.room_buttons[room_index].color = (99,99,99)

      button_colour = (99,99,99)
      gray = sum(button_colour) / 3
      desaturated_color = tuple(int(c * 0.1 + gray * 0.9) for c in button_colour)
      self.room_buttons[room_index].color = desaturated_color  # locked color

      self.room_buttons[room_index].set_text(f"{self.room_names[room_index]}\n(VISITED)")

      
      self.current_room = room_index
      self.current_enemy_index = 0
      self.start_next_battle()
      
      self.game.set_background_image(f"rooms/{self.room_names[self.current_room]}.png")

      # Check if all rooms visited
      if all(self.visited_rooms):
        self.proceed_button.show()


      # UNLOCK ROOMS 
      for locked_enemy, prereq in self.prerequisites.items():
        prereq_room = self.enemy_to_room[prereq]
        locked_room = self.enemy_to_room[locked_enemy]
        if self.visited_rooms[prereq_room] and not self.visited_rooms[locked_room]:
          self.room_buttons[locked_room].clickable = True
          self.room_buttons[locked_room].color = eval(self.font_mapping[locked_enemy]["box-colour"])
          self.room_buttons[locked_room].set_text(self.room_names[locked_room])

  def start_next_battle(self):
    if self.current_room is not None and self.current_enemy_index < len(self.room_enemies[self.current_room]):

      print("STARTING BATTLE",self.current_enemy_index, "FOR ROOM", self.current_room)
      enemy_name = self.room_enemies[self.current_room][self.current_enemy_index]
      self.game.battle = Battle2(enemy_name, self.game, self.battle_ended)
      self.game.battle.start_intro()
      self.game.mode = "battle"
      self.current_enemy_index += 1

    elif self.current_room is not None:
      self.game.start_room_select()
      self.current_room = None




  def battle_ended(self):
    # GO TO NEXT ENEMY OR ROOM SELECT
    # THIS ISNT WORKING... WHY>
    if self.current_enemy_index < 3:
      self.start_next_battle()
    else:
      self.game.start_room_select()
      self.game.mode = "room_select"

  def go_to_end(self):
    print("STARTING END SCREEN")
    self.game.start_end_screen()

  def handle_proceed_click(self):
    if len(self.game.wins + self.game.losses) < 6:
      n = 6 - len(self.game.wins + self.game.losses) 
      message = f"Do you really want to leave the party?\nyou still have {n} people to speak to"
      self.popup = Popup.confirm(self.game, message, "I'm sure, leave", "Stay", self.go_to_end, self.close_popup)
    else:
      self.go_to_end()

  def close_popup(self):
    self.popup = None

  def handle_event(self, event, game):
    if self.popup:
      self.popup.handle_event(event, game)
    else:
      for button in self.room_buttons:
        button.handle_event(event, game)
      if self.proceed_button.visible:
        self.proceed_button.handle_event(event, game)

  def draw(self, game):
    # TITLE
    # font = pygame.font.Font(None, int(36 * (game.height / 500.0)))
    # title = font.render("Select a Room", True, (255, 255, 255))
    # game.screen.blit(title, (int(350 * game.width / 800), int(50 * game.height / 500)))
    
    sw, sh = game.width, game.height
    sx, sy = sw / 800.0, sh / 500.0
 
    # TITLE (centred)
    font = pygame.font.Font(resource_path(f"fonts/Crimson_Text/CrimsonText-Bold.ttf"), int(36 * sy))
    title = font.render("Select a Room", True, (255, 255, 255))
    game.screen.blit(title, (sw // 2 - title.get_width() // 2, int(30 * sy) -30))


    # TALLY
    tally_font = pygame.font.Font(resource_path(f"fonts/Crimson_Text/CrimsonText-Bold.ttf"), int(28 * (game.height / 500.0)))
    small_font = pygame.font.Font(resource_path(f"fonts/Crimson_Text/CrimsonText-Bold.ttf"), int(20 * (game.height / 500.0)))
    wins = len(game.wins)
    losses = len(game.losses)
    tally_x = int(620 * (game.width / 800.0))
    tally_y = int(30 * (game.height / 500.0))
    padding = int(10 * (game.height / 500.0))
    # box around it
    box_width = int(150 * (game.width / 800.0))
    box_height = int(80 * (game.height / 500.0))
    pygame.draw.rect(game.screen, (40, 40, 40), (tally_x, tally_y, box_width, box_height), border_radius=8)
    pygame.draw.rect(game.screen, (120, 120, 120), (tally_x, tally_y, box_width, box_height), 2, border_radius=8)

    won_label = tally_font.render(f"WINS: {wins}", True, (100, 220, 100))
    game.screen.blit(won_label, (tally_x + padding, tally_y + padding))
    lost_label = tally_font.render(f"LOSSES: {losses}", True, (220, 100, 100))
    game.screen.blit(lost_label, (tally_x + padding, tally_y + padding + int(30 * (game.height / 500.0))))

    mouse_pos = pygame.mouse.get_pos()
    tally_rect = pygame.Rect(tally_x, tally_y, box_width, box_height)
    if tally_rect.collidepoint(mouse_pos) and (game.wins or game.losses):
      all_names = [f"WIN: {n}" for n in game.wins] + [f"LOSS: {n}" for n in game.losses]
      hover_y = tally_y + box_height + padding
      hover_w = int(150 * (game.width / 800.0))
      hover_h = int(len(all_names) * 22 * (game.height / 500.0) + padding * 2)
      pygame.draw.rect(game.screen, (40, 40, 40), (tally_x, hover_y, hover_w, hover_h), border_radius=6)
      pygame.draw.rect(game.screen, (120, 120, 120), (tally_x, hover_y, hover_w, hover_h), 1, border_radius=6)
      for i, name in enumerate(all_names):
        colour = (100, 220, 100) if name.startswith("WIN") else (220, 100, 100)
        label = small_font.render(name, True, colour)
        game.screen.blit(label, (tally_x + padding, hover_y + padding + i * int(22 * (game.height / 500.0))))


    # ROOM BUTTONS
    # CHANGE TO BE AN IMAGE WHEN I HAVE ONE
    for button in self.room_buttons:
      button.draw(game)
    
    self.proceed_button.draw(game)

    if self.popup:
      self.popup.draw(game)
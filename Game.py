import pygame
import json
from Button import *
from Battle2 import *
from DialogueBox import *
from StartPage import *
from RoomSelect import *
from EndScreen import *

WIDTH = 1400
HEIGHT = 800
GAME_TITLE = "hmmm"
class Game:
  def __init__(self):
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()


    self.buttons = []
    self.background = None
    self.battle = None

    self.width = WIDTH
    self.height = HEIGHT

    self.start_page = StartPage(self)
    self.room_select = RoomSelect(self)
    self.end_screen = EndScreen(self)

    self.dialogue_box = DialogueBox(self)
    self.buttons.append(self.dialogue_box)

    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    clock.tick(60)

    self.stopped = False

    self.mode = "start_page"
    print('STARTED')

  def set_background_image(self, filename):
    try:
      print("SETTING BACKGROUND IMAGE TO", filename)
      self.background = pygame.image.load(f"images/{filename}")

    except:
      print("didnt load background oops") 
    self.update_background()


  def update_background(self):
    if self.background:
      self.background = pygame.transform.scale(self.background, (self.width, self.height))
    else:
      self.background = None

  def init_dialogue(self, dialogue):
    self.dialogue_box.init_dialogue(dialogue)
    self.mode = "dialogue"

  def battle_mode(self):
    self.mode = "battle"

  def start_room_select(self):
    print("STARTING ROOM SELECTIONs")
    self.set_background_image("house.png")
    self.mode = "room_select"

  def start_end_screen(self):
    self.end_screen.start()
    self.mode = "end_screen"


  def draw(self):
    # BACKGROUND
    # self.screen.fill((255, 255, 255))
    if (self.background):
      self.screen.blit(self.background, (0, 0))

    if self.mode == "start_page":
      self.start_page.draw(self)
    elif self.mode == "room_select":
      self.room_select.draw(self)
    elif self.mode == "end_screen":
      self.end_screen.draw(self)
    else:
      for button in self.buttons:
        button.draw(self)

      if self.battle and self.mode=="battle":
        self.battle.draw(self)

    pygame.display.update()


  def update(self):
    # print(self.mode)
    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          print("CLICKED: ", event.pos)


      if event.type == pygame.QUIT:
        self.stopped = True


      ## IF RESIZE CHANGE EVRYTHING
      if event.type == pygame.VIDEORESIZE:
        self.width = event.w
        self.height = event.h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        # if hasattr(self.start_page, 'update_background'):
        #   self.start_page.update_background()
        # if hasattr(self.end_screen, 'update_background'):
        #   self.end_screen.update_background()
        self.update_background()

      if self.mode == "start_page":
        self.start_page.handle_event(event, self)
      elif self.mode == "room_select":
        self.room_select.handle_event(event, self)
      elif self.mode == "end_screen":
        self.end_screen.handle_event(event, self)
      else:
        if len(self.dialogue_box.dialogue_list) > 0:

          for button in self.buttons:
            button.handle_event(event, self)

        elif self.battle and self.mode=="battle":
          self.battle.handle_event(event)
        

    if self.battle:
      self.battle.update()

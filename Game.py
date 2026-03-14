import pygame
import json
from Button import *
from Battle import *
from Dialogue_box import *

WIDTH = 800
HEIGHT = 500

class Game:
  def __init__(self):
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()


    self.buttons = []
    self.background = None
    self.battle = None
    self.battle = Battle("fred", self)

    self.dialogue_box = DialogueBox(100, 100, 100, 100, "what?")
    self.dialogue_box.init_dialogue(
      [
        {
          "speaker": "You",
          "text": "whatever"
        },
        {
          "speaker": "Fred",
          "text": "yayyyyyy"
        }
      ]
      )
    self.buttons.append(self.dialogue_box)

    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("hmmm")
    clock = pygame.time.Clock()
    clock.tick(60)

    # self.buttons.append(Button(100, 100, 100, 100, "text", None))

    self.stopped = False
    print('STARTED')


  def draw(self):
    # BACKGROUND
    self.screen.fill((255, 255, 255))
    if (self.background):
      self.screen.blit(self.background, (0, 0))

    for button in self.buttons:
      button.draw(self)

    if self.battle:
      self.battle.draw(self)

    pygame.display.update()

  def update(self):
    if self.battle:
      self.battle.update()

    for event in pygame.event.get():
      if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          print("CLICKED: ", event.pos)


      if event.type == pygame.QUIT:
        self.stopped = True

      if self.battle:
        self.battle.handle_event(event)

      for button in self.buttons:
        button.handle_event(event, self)


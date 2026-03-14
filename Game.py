import pygame
import json
from Button import *

WIDTH = 1000
HEIGHT = 1000

class Game:
  def __init__(self):
    self.buttons = []
    self.background = None

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("hmmm")
    clock = pygame.time.Clock()
    clock.tick(60)

    self.buttons.append(Button(100, 100, 100, 100, "text", None))

    self.stopped = False
    print('STARTED')


  def draw(self):
    # BACKGROUND
    self.screen.fill((255, 255, 255))
    if (self.background):
      self.screen.blit(self.background, (0, 0))

    for button in self.buttons:
      button.draw(self)

    pygame.display.update()

  def update(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.stopped = True


      for button in self.buttons:
        button.handle_event(event, self)

      if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
          print("CLICKED: ", event.pos)


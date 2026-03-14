import pygame
import json

class Game:
  def __init__(self):
    self.buttons = []
    self.background = None


    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    self.screen = pygame.display.set_mode((160*4, 144*4))
    pygame.display.set_caption("hmmm")
    clock = pygame.time.Clock()
    clock.tick(60)

    self.stopped = False
    print('STARTED')


  def render(self):
    # BACKGROUND
    self.screen.fill((255, 255, 255))
    if (self.background):
        self.screen.blit(self.background, (0, 0))

    pygame.display.update()

  def update(self):
    pass
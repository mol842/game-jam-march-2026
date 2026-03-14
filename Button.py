import pygame
import os
from pygame.locals import Color

class Button:
  def __init__(self, x, y, width, height, text, action, color=(93, 93, 93), font=None):
    self.x = x
    self.y = y
    self.width = width
    self.height = height

    self.color = color
    self.text = text
    self.font = pygame.font.Font(None, 28) if not font else font

    self.clickable = True
    self.visible = True

    self.action = action

    self.rect = pygame.Rect(x, y, width, height)

  def handle_event(self, event, game):
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      if self.rect.collidepoint(event.pos):
        print('CLICKED A BUTTON: ', self.text)
        if (self.action):
          print("RUNNING ACTION")
          self.action()

  def enable(self):
    self.clickable = True
    self.visible = True
    
  def disable(self):
    self.clickable = False
    self.visible = False

  def set_text(self, text): 
    self.text = text

  def draw(self, game):
    if self.visible:
      pygame.draw.rect(game.screen, Color(self.color), self.rect, 2)
      text_surface = self.font.render(self.text, False, Color(self.color))
      text_size = text_surface.get_rect().size

      ## fix this it was wayyyy more complicated last game. yay.
      leftPadding = (self.width - text_size[0])/2
      topPadding = (self.height - text_size[1])/2

      game.screen.blit(text_surface, (self.x + leftPadding, self.y + topPadding))
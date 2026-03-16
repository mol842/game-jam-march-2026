import pygame
import os
from pygame.locals import Color
from utils import *

class Button:
  def __init__(self, game, x, y, width, height, text, action, color=(90, 93, 93), font=None, text_color=None):
    self.game = game
    self.original_x = x
    self.original_y = y
    self.original_width = width
    self.original_height = height

    self.color = color
    self.text_color = text_color if text_color else (0,0,0)
    self.text = text
    self.font_path = resource_path("fonts/") + font if font else None

    self.clickable = True
    self.visible = True

    self.action = action
    self.update_size()

  def update_size(self):
    self.x = self.original_x * (self.game.width / 800.0)
    self.y = self.original_y * (self.game.height / 500.0)
    self.width = self.original_width * (self.game.width / 800.0)
    self.height = self.original_height * (self.game.height / 500.0)
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    font_size = 28 * (self.game.height / 500.0)
    if self.font_path:
      if not hasattr(self, 'font') or not self.font or self.font.get_height() != int(font_size):
        self.font = pygame.font.Font(self.font_path, int(font_size))
    else:
      if not hasattr(self, 'font') or not self.font or self.font.get_height() != int(font_size):
        self.font = pygame.font.Font(None, int(font_size))

  def handle_event(self, event, game, force=False):
    if force or event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clickable:
      if force or self.rect.collidepoint(event.pos):
        print('CLICKED A BUTTON: ', self.text)
        if (self.action):
          print("RUNNING ACTION", self.action.__name__)
          self.action()

  # def enable(self):
  #   self.clickable = True
  #   self.visible = True
  
  def disable(self):
    self.clickable = False


  def show(self):
    self.visible = True
    self.clickable = True

    # print("THIS BUTTON IS NOW VISIBLE")
    # print(self.visible, self.clickable)


  def hide(self):
    # print("HIDINGGGG")
    self.clickable = False
    self.visible = False

  def set_text(self, text): 
    self.text = text

  # def draw(self, game):
  #   self.update_size()
  #   # print(self.visible)
  #   if self.visible:
  #     pygame.draw.rect(game.screen, Color(self.color), self.rect, 0)
  #     text = self.font.render(self.text, False, Color(self.text_color))
  #     text_size = text.get_rect().size

  #     ## fix this it was wayyyy more complicated last game. yay.
  #     leftPadding = (self.width - text_size[0])/2
  #     topPadding = (self.height - text_size[1])/2

  #     game.screen.blit(text, (self.x + leftPadding, self.y + topPadding))
  #     # print(self.text)


  def draw(self, game):
    if self.visible:
      self.update_size()

      pygame.draw.rect(game.screen, Color(self.color), self.rect, 0, border_radius=8)
      # YANKED FROM CYANOPHOBIA
      wrapped_lines = []
      words = self.text.split()
      current_line = ""
      padding = 20 * (self.game.width / 800.0)
      for word in words:
        test_line = f"{current_line} {word}".strip()
        if self.font.render(test_line, True, Color(self.text_color)).get_width() <= self.width - padding * 2:
          current_line = test_line
        else:
          if current_line:
            wrapped_lines.append(current_line)
          current_line = word
      if current_line:
        wrapped_lines.append(current_line)

      line_height = self.font.get_height()
      total_text_height = len(wrapped_lines) * line_height
      start_y = self.y + (self.height - total_text_height) / 2

      for i, line in enumerate(wrapped_lines):
        rendered = self.font.render(line, True, Color(self.text_color))
        x = self.x + (self.width - rendered.get_width()) / 2
        game.screen.blit(rendered, (x, start_y + i * line_height))
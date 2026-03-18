import json
import os
import pygame
from PopupConfirm import Popup
from Button import Button
from utils import *
import textwrap


DEFAULT_TEXT_TITLE = (255, 255, 255)
DEFAULT_TEXT_WHITE = (255, 255, 255)

BG_DARK       = (28, 24, 32)
BG_MID        = (40, 34, 48)
TEXT_MUTED    = (255, 255, 255)
OVERLAY_COLOR = (0, 0, 0)

class EnemyPopup(Popup):
  def __init__(self, game, enemy):
    self.game = game
    self.enemy = enemy

    sx = game.width / 800.0
    sy = game.height / 500.0

    popup_w = int(560 * sx)
    popup_h = int(400 * sy)
    popup_x = (game.width - popup_w) // 2
    popup_y = (game.height - popup_h) // 2

    self.bg_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)

    font_mapping = json.load(open('fonts/font_mapping.json'))

    entry = font_mapping.get(enemy.name)
    if entry is None:
      self.accent_color = DEFAULT_TEXT_TITLE
      self.text_title = DEFAULT_TEXT_WHITE
      self.text_white = DEFAULT_TEXT_WHITE
      self.font_title = pygame.font.Font(None, int(22 * sy))
      self.font_label = pygame.font.Font(None, int(18 * sy))
      self.font_body = pygame.font.Font(None, int(16 * sy))
      self.font_animal_fact = pygame.font.Font(None, int(14 * sy))
    else:
      accent_color = eval(entry.get("box-colour", "")) or DEFAULT_TEXT_TITLE
      text_colour = eval(entry.get("text-colour", "")) or DEFAULT_TEXT_WHITE
      self.accent_color = accent_color
      self.text_title = (255, 255, 255)
      self.text_white = (255, 255, 255)
      font_path = entry.get("font")
      self.font_title = pygame.font.Font(None, int(22 * sy))
      self.font_label = pygame.font.Font(None, int(18 * sy))
      self.font_body = pygame.font.Font(None, int(16 * sy))


      if font_path:
        full_path = os.path.join(resource_path("fonts"), font_path)
        self.font_title = pygame.font.Font(full_path, int(22 * sy))
        self.font_label = pygame.font.Font(full_path, int(18 * sy))
        self.font_body = pygame.font.Font(full_path, int(16 * sy))
        self.font_animal_fact = pygame.font.Font(full_path, int(14 * sy)) if font_path else pygame.font.Font(None, int(14 * sy))

    self.border_dim = tuple(int(c * 0.45 + 20) for c in self.accent_color)
    self.border_lit = tuple(min(255, int(c * 0.7 + 80)) for c in self.accent_color)

    btn_h      = int(38 * sy)
    btn_w      = int(110 * sx)
    btn_margin = int(18 * sy)
    btn_x_raw  = (popup_x + popup_w - btn_w - int(20 * sx)) / sx
    btn_y_raw  = (popup_y + popup_h - btn_h - btn_margin) / sy
    btn_w_raw  = btn_w / sx
    btn_h_raw  = btn_h / sy

    btn_colour = tuple(int(c * 0.7) for c in self.accent_color)

    self.fight_button = Button(
      game, btn_x_raw, btn_y_raw, btn_w_raw, btn_h_raw,
      "FIGHT!", self._close,
      color=btn_colour, text_color=self.text_white,
    )

    self.visible = True

  def handle_event(self, event, game):
    if not self.visible:
      return
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      if not self.bg_rect.collidepoint(event.pos):
        self._close()
    self.fight_button.handle_event(event, game)

  def draw(self, game):
    if not self.visible:
      return

    sx = game.width / 800.0
    sy = game.height / 500.0

    overlay = pygame.Surface((game.width, game.height), pygame.SRCALPHA)
    overlay.fill((*OVERLAY_COLOR, 180))
    game.screen.blit(overlay, (0, 0))

    card = pygame.Surface((self.bg_rect.width, self.bg_rect.height), pygame.SRCALPHA)
    card.fill((*BG_DARK, 255))

    inner = pygame.Rect(3, 3, self.bg_rect.width - 6, self.bg_rect.height - 6)
    pygame.draw.rect(card, BG_MID, inner)

    pygame.draw.rect(card, self.border_dim, (0, 0, self.bg_rect.width, self.bg_rect.height), 2, border_radius=12)
    pygame.draw.rect(card, self.border_lit, (1, 1, self.bg_rect.width - 2, self.bg_rect.height - 2), 1, border_radius=11)

    img_size = int(180 * sy)
    img_x    = int(24 * sx)
    img_y    = (self.bg_rect.height - img_size) // 2 + int(4 * sy)

    if self.enemy.original_image:
      frame_pad  = int(4 * sx)
      frame_rect = pygame.Rect(
        img_x - frame_pad, img_y - frame_pad,
        img_size + frame_pad * 2, img_size + frame_pad * 2,
      )
      pygame.draw.rect(card, self.border_dim, frame_rect, 0, border_radius=8)
      pygame.draw.rect(card, self.accent_color, frame_rect, 1, border_radius=8)

      scaled = pygame.transform.smoothscale(self.enemy.original_image, (img_size, img_size))
      card.blit(scaled, (img_x, img_y))

    text_x  = int(230 * sx)
    title_y = int(52 * sy)
    body_y  = int(100 * sy)
    line_h  = int(32 * sy)

    title_surf = self.font_title.render(
      f"ENCOUNTER: {self.enemy.name.upper()}", True, self.text_title
    )
    card.blit(title_surf, (text_x, title_y))

    divider_y = title_y + int(28 * sy)
    pygame.draw.line(
      card, self.border_lit,
      (text_x, divider_y),
      (self.bg_rect.width - int(20 * sx), divider_y),
      1,
    )

    fields = [
      ("Type",         [self.enemy.type]),
      ("Relationship", [self.enemy.relationship]),
      ("Description",  [part.strip() for part in self.enemy.description.split("-")] if "-" in self.enemy.description else [self.enemy.description]),
    ]
    if self.enemy.animal_fact:
      fields.append(("Animal Fact", textwrap.wrap(self.enemy.animal_fact, width=60)))

    y = body_y
    for label, values in fields:
      if label != "Animal Fact":
        label_surf = self.font_label.render(f"{label}:", True, TEXT_MUTED)
        label_w = label_surf.get_width() + int(8 * sx)
        card.blit(label_surf, (text_x, y))
      else:
        label_w = -40
      for value in values:
        if label == "Animal Fact":
          value_surf = self.font_animal_fact.render(value, True, self.text_white)
        else:
          value_surf = self.font_body.render(value, True, self.text_white)
        card.blit(value_surf, (text_x + label_w, y))
        y += line_h

    game.screen.blit(card, (self.bg_rect.x, self.bg_rect.y))

    self.fight_button.draw(game)
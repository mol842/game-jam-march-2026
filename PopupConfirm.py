import pygame
from Button import Button

CONFIRM_GREEN = (76, 153, 76)
CANCEL_RED = (180, 60, 60)
WIN_GREEN = (60, 140, 80)
LOSS_RED = (160, 55, 55)


class Popup:
  def __init__(self, game, mode, message, confirm_text=None, cancel_text=None, confirm_callback=None, cancel_callback=None):
    self.game = game
    self.mode = mode
    self.message = message
    self.visible = True

    sx = game.width / 800.0
    sy = game.height / 500.0

    # BOX
    popup_w = int(400 * sx) if mode == "confirm" else int(360 * sx)
    popup_h = int(150 * sy) if mode == "confirm" else int(150 * sy)
    popup_x = (game.width - popup_w) // 2
    popup_y = (game.height - popup_h) // 2
    self.bg_rect = pygame.Rect(popup_x, popup_y, popup_w, popup_h)
    self.bg_color = (50, 50, 50)

    self.font = pygame.font.Font(None, int(24 * sy))

    # BUTTONS
    btn_h = int(40 * sy)
    btn_margin = int(20 * sy)
    btn_y_raw = (popup_y + popup_h - btn_h - btn_margin) / sy

    if mode == "confirm":
      self.confirm_callback = confirm_callback or self._close
      self.cancel_callback = cancel_callback or self._close

      btn_w = int(120 * sx)
      btn_gap = int(20 * sx)
      total_w = btn_w * 2 + btn_gap
      btn_start_x_raw = (popup_x + (popup_w - total_w) // 2) / sx
      btn_w_raw = btn_w / sx
      btn_h_raw = btn_h / sy
      btn_gap_raw = btn_gap / sx

      self.cancel_button = Button(
        game, btn_start_x_raw, btn_y_raw, btn_w_raw, btn_h_raw,
        cancel_text, self.cancel_callback,
        color=CANCEL_RED, text_color=(255, 255, 255),
      )
      self.confirm_button = Button(
        game, btn_start_x_raw + btn_w_raw + btn_gap_raw, btn_y_raw, btn_w_raw, btn_h_raw,
        confirm_text, self.confirm_callback,
        color=CONFIRM_GREEN, text_color=(255, 255, 255),
      )

    elif mode == "result":
      won = (confirm_text == "yay!")
      self.bg_color = WIN_GREEN if won else LOSS_RED
      btn_color = (40, 110, 55) if won else (120, 35, 35)

      btn_w = int(80 * sx)
      btn_x_raw = (popup_x + (popup_w - btn_w) // 2) / sx
      btn_w_raw = btn_w / sx
      btn_h_raw = btn_h / sy

      self.result_button = Button(
        game, btn_x_raw, btn_y_raw, btn_w_raw, btn_h_raw,
        confirm_text, self._close,
        color=btn_color, text_color=(255, 255, 255),
      )

  @staticmethod
  def confirm(game, message, confirm_text, cancel_text, confirm_callback, cancel_callback=None):
    return Popup(game, "confirm", message, confirm_text=confirm_text, cancel_text=cancel_text, confirm_callback=confirm_callback, cancel_callback=cancel_callback)

  @staticmethod
  def result(game, opponent_name, won):
    button_text = "yay!" if won else "aww."
    message = f"You won the argument against {opponent_name}!" if won else f"You lost the argument against {opponent_name}!"
    return Popup(game, "result", message, confirm_text=button_text)

  def _close(self):
    self.visible = False

  def handle_event(self, event, game):
    if not self.visible:
      return
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      outside = not self.bg_rect.collidepoint(event.pos)
      if outside:
        if self.mode == "result":
          self._close()
        # CLOSE IF YOU CLICK OUTSIDE
        else:
          self.cancel_callback()
    if self.mode == "confirm":
      self.cancel_button.handle_event(event, game)
      self.confirm_button.handle_event(event, game)
    elif self.mode == "result":
      self.result_button.handle_event(event, game)

  def draw(self, game):
    if not self.visible:
      return
    overlay = pygame.Surface((game.width, game.height))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    game.screen.blit(overlay, (0, 0))

    pygame.draw.rect(game.screen, self.bg_color, self.bg_rect, border_radius=10)
    pygame.draw.rect(game.screen, (200, 200, 200), self.bg_rect, 2, border_radius=10)

    # TEXT
    sy = game.height / 500.0
    y_offset = self.bg_rect.y + int(20 * sy)
    for line in self.message.split('\n'):
      surf = self.font.render(line, True, (255, 255, 255))
      text_x = self.bg_rect.x + (self.bg_rect.width - surf.get_width()) // 2
      game.screen.blit(surf, (text_x, y_offset))
      y_offset += int(30 * sy)

    # BUTTONS
    if self.mode == "confirm":
      self.cancel_button.draw(game)
      self.confirm_button.draw(game)
    elif self.mode == "result":
      self.result_button.draw(game)
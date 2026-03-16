import pygame
from Button import *
import json
from pygame.locals import Color
from utils import *

class DialogueBox(Button):
  def __init__(self, game):
    ## SET UP ALL THE FONTS
    self.font_mapping = json.load(open('fonts/font_mapping.json'))
    self.loaded_fonts = {}
    for speaker, data in self.font_mapping.items():
      font_name = data["font"]
      font_path = resource_path(f"fonts/{font_name}")
      self.loaded_fonts[speaker] = font_path
    self.current_speaker = "You"

    super().__init__(game, 100, 300, 600, 190, "hello", self.next_dialogue)
    self.game = game
    self.dialogue_list = []
    self.dialogue_index = 0
    self.callback = None
    self.triangle_size = 20

  def update_size(self):
    super().update_size()
    if self.current_speaker in self.loaded_fonts:
      font_path = self.loaded_fonts[self.current_speaker]
      ## CAN I CHANGE SO IT DOESNT LOAD EVERY LOOP? THATS SOOOO INEFFICIENT
      # print("LOADING FONT!!", font_path)
      font_size = int(28 * (self.game.height / 500.0))
      self.font = pygame.font.Font(font_path, font_size)
    else:
      # print("NO FONT FOR", self.current_speaker)
      font_size = 28 * (self.game.height / 500.0)
      self.font = pygame.font.Font(None, int(font_size))
    self.triangle_size = 20 * (self.game.height / 500.0)
    self.triangle_rect = pygame.Rect(self.x, self.y + self.height - self.triangle_size, self.triangle_size, self.triangle_size)

  def init_dialogue(self, dialogue, callback=None):
    print("INITIALISING DIALOGUE", dialogue[0]["text"], callback)
    self.dialogue_list = dialogue
    self.dialogue_index = 0
    self.callback = callback
    self.current_speaker = self.dialogue_list[self.dialogue_index]["speaker"]

    # SET UP FONT
    if self.current_speaker in self.font_mapping:
      mapping = self.font_mapping[self.current_speaker]
      self.color = eval(mapping["box-colour"])
      self.text_color = eval(mapping["text-colour"])
    else:
      self.color = (93, 93, 93)
      self.text_color = (93, 93, 93)

    self.set_text(self.dialogue_list[self.dialogue_index]["text"])
    self.show()
    self.visible = True
    print(self.dialogue_list)


  def end_dialogue(self):
    print("ENDING THE DIALOGUE AT INDEX", self.dialogue_index, self.dialogue_list[self.dialogue_index]["text"])
    self.hide()
    self.dialogue_list = []
    self.dialogue_index = 0
    if self.callback:
      print("RUNNING CALLBACK", self.callback.__name__)
      self.callback()
      self.callback = None
    else:
      print("NO CALLBACK, ENDING")
      self.game.battle_mode()


  def next_dialogue(self):
    print("NEXT")
    if (self.dialogue_index < len(self.dialogue_list)-1):
      self.dialogue_index += 1

      self.current_speaker = self.dialogue_list[self.dialogue_index]["speaker"]
      ## SET THE COLOUR ETC WHATEVER I DONT CARE
      if self.current_speaker in self.font_mapping:
        mapping = self.font_mapping[self.current_speaker]
        self.color = eval(mapping["box-colour"])
        self.text_color = eval(mapping["text-colour"])
        print(mapping)
      else:
        self.color = (93, 93, 93)
        self.text_color = (93, 93, 93)
      self.set_text(self.dialogue_list[self.dialogue_index]["text"])

    else:
      print("ENDING!")
      self.end_dialogue()

  def previous_dialogue(self):
    print("PREVIOUS")
    if self.dialogue_index > 0:
      self.dialogue_index -= 1

      self.current_speaker = self.dialogue_list[self.dialogue_index]["speaker"]
      if self.current_speaker in self.font_mapping:
        mapping = self.font_mapping[self.current_speaker]
        self.color = eval(mapping["box-colour"])
        self.text_color = eval(mapping["text-colour"])
      else:
        self.color = (93, 93, 93)
        self.text_color = (93, 93, 93)
      self.set_text(self.dialogue_list[self.dialogue_index]["text"])
    else:
      print("AT FIRST, DO NOTHING")

  def handle_event(self, event, game):

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            self.previous_dialogue()
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
          super().handle_event(event, game, force=True)

    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clickable and self.visible:
      if self.triangle_rect.collidepoint(event.pos):
        self.previous_dialogue()
      else:
        super().handle_event(event, game)

  def draw(self, game):
    super().draw(game)
    ## ADD THE NAME OF WHOEVER IS SPEAKING
    if self.current_speaker and self.visible:
      speaker_text = self.font.render(self.current_speaker, False, Color(self.text_color))
      speaker_rect = speaker_text.get_rect(center=(self.x + self.width / 2, self.y + 20))
      game.screen.blit(speaker_text, speaker_rect)
      # TRIAMGLE TO GO BACKWARDS

      pad = 3
      points = [
        (self.x, self.y + self.height - self.triangle_size / 2 - pad),
        (self.x + self.triangle_size, self.y + self.height - self.triangle_size- pad),
        (self.x + self.triangle_size, self.y + self.height- pad)
      ]
      pygame.draw.polygon(game.screen,  self.text_color, points)
  

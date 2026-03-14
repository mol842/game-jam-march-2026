import pygame
from Button import *

class DialogueBox(Button):
  def __init__(self, x, y, width, height, text, color=(93, 93, 93), font=None):
    super().__init__(100, 100, 500, 500, "hello", self.next_dialogue)
    self.dialogue_list = []
    self.dialogue_index = 0

  def init_dialogue(self, dialogue):
    print("INITIALISING DIALOGUE")
    self.dialogue_list = dialogue
    self.dialogue_index = 0
    self.set_text(self.dialogue_list[self.dialogue_index]["text"])


  def end_dialogue(self):
    self.dialogue_list = []
    self.dialogue_index = 0
    self.hide()


  def next_dialogue(self):
    if (self.dialogue_index < len(self.dialogue_list)-1):
      self.dialogue_index += 1
      self.set_text(self.dialogue_list[self.dialogue_index]["text"])
      ## SET THE COLOUR ETC WHATEVER I DONT CARE
    else:
      self.end_dialogue()
  

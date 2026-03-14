import pygame
from Button import *

class DialogueBox(Button):
  def __init__(self, game, x, y, width, height, text, color=(93, 93, 93), font=None):
    super().__init__(100, 100, 500, 500, "hello", self.next_dialogue)
    self.game = game
    self.dialogue_list = []
    self.dialogue_index = 0
    self.callback = None

  def init_dialogue(self, dialogue, callback=None):
    print("INITIALISING DIALOGUE", dialogue[0]["text"])
    self.dialogue_list = dialogue
    self.dialogue_index = 0
    self.callback = callback
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
      self.callback()
      self.callback = None
    else:
      self.game.battle_mode()


  def next_dialogue(self):
    print("NEXT")
    if (self.dialogue_index < len(self.dialogue_list)-1):
      self.dialogue_index += 1
      self.set_text(self.dialogue_list[self.dialogue_index]["text"])
      ## SET THE COLOUR ETC WHATEVER I DONT CARE
    else:
      print("ENDING!")
      self.end_dialogue()
  

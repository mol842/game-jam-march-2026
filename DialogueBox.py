import pygame
from Button import *

class DialogueBox(Button):
  def __init__(self, game):
    super().__init__(100, 300, 500, 200, "hello", self.next_dialogue)
    self.game = game
    self.dialogue_list = []
    self.dialogue_index = 0
    self.callback = None

  def init_dialogue(self, dialogue, callback=None):
    print("INITIALISING DIALOGUE", dialogue[0]["text"], callback)
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
      self.set_text(self.dialogue_list[self.dialogue_index]["text"])
      ## SET THE COLOUR ETC WHATEVER I DONT CARE
    else:
      print("ENDING!")
      self.end_dialogue()
  

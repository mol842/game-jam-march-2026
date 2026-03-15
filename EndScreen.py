import pygame
from Button import *

class EndScreen:
  def __init__(self, game):
    self.game = game
    self.background = None
    self.final_image = None
    self.showing_image = False
    
    # self.background = pygame.image.load("images/end_background.png")
    # self.final_image = pygame.image.load("images/final_image.png")
  
    ## need to get in from json
    self.dialogue = [
      {"speaker": "Narrator", "text": "w0w"},
      {"speaker": "Narrator", "text": "you finished. it."},
      {"speaker": "Narrator", "text": "yay."}
    ]
    self.dialogue_index = 0
    
    self.next_button = Button(self.game, 350, 400, 100, 50, "Next", self.next_dialogue)

  def start(self):
    print("STARTING ENDING")
    self.dialogue_index = 0
    self.showing_image = False
    self.next_button.show()

  def next_dialogue(self):
    self.dialogue_index += 1
    if self.dialogue_index >= len(self.dialogue):
      self.show_final_image()

  def show_final_image(self):
    # MAKE THIS DEPENDENT ON THE SCORE
    self.showing_image = True
    self.next_button.hide()

  def handle_event(self, event, game):
    if not self.showing_image and self.next_button.visible:
      self.next_button.handle_event(event, game)

  def draw(self, game):
    if self.background:
      game.screen.blit(self.background, (0, 0))
    else:
      game.screen.fill((0, 0, 0)) 

    font = pygame.font.Font(None, 24)

    ## FINAL ANIMAL IMAGE
    if self.showing_image:
      if self.final_image:
        img_rect = self.final_image.get_rect(center=(400, 250))
        game.screen.blit(self.final_image, img_rect)
      else:
        ## YELLOW BOX PLACEHOLDER
        pygame.draw.rect(game.screen, (255, 255, 0), (300, 200, 200, 100))
        text = font.render("FINAL IMAGE", True, (0, 0, 0))
        game.screen.blit(text, (350, 240))

    else:
      # GO THROUGH DIALOGUE
      if self.dialogue_index < len(self.dialogue):
        speaker = self.dialogue[self.dialogue_index]["speaker"]
        text = self.dialogue[self.dialogue_index]["text"]

        speaker_text = font.render(f"{speaker}:", True, (255, 255, 255))
        dialogue_text = font.render(text, True, (255, 255, 255))
        game.screen.blit(speaker_text, (100, 200))
        game.screen.blit(dialogue_text, (100, 230))
      
      self.next_button.draw(game)
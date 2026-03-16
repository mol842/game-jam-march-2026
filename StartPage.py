import pygame
from Button import *
from utils import *

class StartPage:
  def __init__(self, game):
    self.game = game
    self.original_background = None
    game.set_background_image("start_background.png")
    self.start_button = Button(self.game, 0, 0, 800, 500, "", lambda: self.start_game())

  def start_game(self):
    self.game.start_intro_dialogue()

    # self.game.start_room_select()

  def handle_event(self, event, game):
    self.start_button.handle_event(event, game)
#pygame.font.Font(resource_path(f"fonts/Crimson_Text/CrimsonText-Bold.ttf")
  def draw(self, game):    
    x = 110
    font_name = "Crimson_Text/CrimsonText-Bold.ttf"
    title_font = pygame.font.Font(resource_path(f"fonts/{font_name}"), 72)
    title_text = title_font.render("Kin Selection", True, (255, 255, 255))
    title_rect = title_text.get_rect(topleft=(x, 180))
    game.screen.blit(title_text, title_rect)

    font_name = "Crimson_Text/CrimsonText-Regular.ttf"

    noun_font = pygame.font.Font(resource_path(f"fonts/{font_name}"), 36)
    noun_text = noun_font.render("(noun) A form of natural selection. Some animals cooperate with relatives,", True, (180, 180, 180))
    noun_rect = noun_text.get_rect(topleft=(x, title_rect.bottom + 10))
    game.screen.blit(noun_text, noun_rect)

    noun_text = noun_font.render("even if this brings risk to themselves.", True, (180, 180, 180))
    noun_rect = noun_text.get_rect(topleft=(x, title_rect.bottom + 40))
    game.screen.blit(noun_text, noun_rect)



    subtitle_font = pygame.font.Font(resource_path(f"fonts/{font_name}"), 36)
    subtitle_text = subtitle_font.render("Click anywhere to start", True, (200, 200, 200))
    subtitle_rect = subtitle_text.get_rect(topleft=(x, noun_rect.bottom + 50))
    game.screen.blit(subtitle_text, subtitle_rect)
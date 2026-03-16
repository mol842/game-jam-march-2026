import pygame
from Button import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (169, 169, 169)
LIGHT_GRAY = (235, 235, 235)
DARK_GRAY = (169, 169, 169)
CREAM = (240, 220, 180)
PURPLE = (180, 160, 220)
RED = (128, 0, 32)
BOX_COLOR = (0, 0, 0, 128)  
from utils import *

class EndScreen:
  def __init__(self, game):
    self.game = game
    self.background = None
    self.final_image = None
    self.showing_image = False

    self.your_animal = None
    self.your_animal_message = None
    self.your_animal_image = None

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
    self.game.set_background_image("black.png")
    # self.game.set_background_image(None)

    self.dialogue_index = 0
    self.showing_image = False
    self.next_button.show()

  def next_dialogue(self):
    self.dialogue_index += 1
    if self.dialogue_index >= len(self.dialogue):
      self.assign_animal()
      self.show_final_image()

  def show_final_image(self):
    # MAKE THIS DEPENDENT ON THE SCORE
    self.showing_image = True
    self.next_button.hide()
    self.final_image = pygame.image.load(resource_path(f"images/animals/{self.your_animal_image}"))
    self.game.set_background_image(f"animals/{self.your_animal_image}")

  def handle_event(self, event, game):
    if not self.showing_image and self.next_button.visible:
      self.next_button.handle_event(event, game)

  def draw(self, game):
    scale = game.height / 500.0
    
    if self.showing_image: # FINAL ANIMAL
      title_font = pygame.font.Font(resource_path(f"fonts/Crimson_Text/CrimsonText-Bold.ttf"), int(48 * scale))
      animal_label = title_font.render(f"You are a {self.your_animal}!", True, WHITE)
      game.screen.blit(animal_label, animal_label.get_rect(center=(game.width // 2 - 4, int(340 * scale) - 38)))
      animal_label = title_font.render(f"You are a {self.your_animal}!", True, BLACK)
      game.screen.blit(animal_label, animal_label.get_rect(center=(game.width // 2, int(340 * scale) - 40)))


      msg_font = pygame.font.Font(resource_path(f"fonts/Crimson_Text/CrimsonText-Regular.ttf"), int(26 * scale))
      words = self.your_animal_message.split()
      # WRAPPING THE STUPID TEXT
      lines, current = [], ""
      for word in words:
        test = f"{current} {word}".strip()
        if msg_font.render(test, True, BLACK).get_width() < game.width - int(200 * scale):
          current = test
        else:
          lines.append(current)
          current = word
      if current:
        lines.append(current)

      # BOX BEHIND
      box_width = game.width - int(200 * scale)
      box_height = len(lines) * int(30 * scale) + 20
      box_x = (game.width - box_width) // 2
      box_y = int(390 * scale) - 80
      box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
      pygame.draw.rect(box_surface, BOX_COLOR, (0, 0, box_width, box_height), border_radius=10)
      game.screen.blit(box_surface, (box_x, box_y))

      for i, line in enumerate(lines):
        rendered = msg_font.render(line, True, PURPLE)
        game.screen.blit(rendered, rendered.get_rect(center=(game.width // 2, int(390 * scale) + i * int(30 * scale) - 40)))

      thank_you_text = "Thank you for playing Kin Selection.\nPost your animal in the comments below!\n- Eleanor and Molly"
      thank_you_lines = thank_you_text.split('\n')
      for i, line in enumerate(thank_you_lines):
        thank_rendered = msg_font.render(line, True, RED)
        game.screen.blit(thank_rendered, thank_rendered.get_rect(topright=(game.width - 20, 20 + i * int(30 * scale))))

    else: # SPEAKER END TEXT
      if self.dialogue_index < len(self.dialogue):
        speaker = self.dialogue[self.dialogue_index]["speaker"]
        text = self.dialogue[self.dialogue_index]["text"]

        speaker_font = pygame.font.Font(resource_path(f"fonts/Crimson_Text/CrimsonText-Regular.ttf"), int(22 * scale))
        speaker_rendered = speaker_font.render(speaker.upper(), True, PURPLE)
        game.screen.blit(speaker_rendered, speaker_rendered.get_rect(centerx=game.width // 2, y=int(170 * scale)))

        text_font = pygame.font.Font(resource_path(f"fonts/Crimson_Text/CrimsonText-Regular.ttf"), int(30 * scale))
        words = text.split()
        lines, current = [], ""
        for word in words:
          test = f"{current} {word}".strip()
          if text_font.render(test, True, BLACK).get_width() < game.width - int(200 * scale):
            current = test
          else:
            lines.append(current)
            current = word
        if current:
          lines.append(current)

        total_h = len(lines) * int(34 * scale)
        start_y = int(200 * scale)
        for i, line in enumerate(lines):
          rendered = text_font.render(line, True, DARK_GRAY)
          game.screen.blit(rendered, rendered.get_rect(centerx=game.width // 2, y=start_y + i * int(34 * scale)))

      self.next_button.draw(game)


  def draw_old(self, game):
    font = pygame.font.Font(None, 24)

    ## FINAL ANIMAL IMAGE
    if self.showing_image:
      animal_text = font.render(f"Your Animal: {self.your_animal}", True, WHITE)
      game.screen.blit(animal_text, (100, 350))
      message_text = font.render(self.your_animal_message, True, WHITE)
      game.screen.blit(message_text, (100, 380))

    else:
      # GO THROUGH DIALOGUE
      if self.dialogue_index < len(self.dialogue):
        speaker = self.dialogue[self.dialogue_index]["speaker"]
        text = self.dialogue[self.dialogue_index]["text"]

        speaker_text = font.render(f"{speaker}:", True, WHITE)
        dialogue_text = font.render(text, True, WHITE)
        game.screen.blit(speaker_text, (100, 200))
        game.screen.blit(dialogue_text, (100, 230))
      
      self.next_button.draw(game)


  def assign_animal(self):
    # self.game.wins

    wins = len(self.game.wins)
    losses = len(self.game.losses)
    total = wins + losses
    win_rate = wins / total if total > 0 else 0


    # animal hierarchy by socialness

    # Clam (didnt show up)
    
    # Mantis Shrimp (very low score)
    # New Guinea Amau frog (low score)

    # Log nosed echidna (medium score)
    # Helmeted honeyeater
    # Australian Bees (high score)
    ## one for low completion


    if total < 3:
      self.your_animal = "Clam"
      self.your_animal_image = "Clam.png"
      self.your_animal_message = (
        "Did you even come to the party? You didn't even try.  "
        "Were you hiding in the bathroom the whole time? "
        "Fun fact: clams have no brain. They live a solitary life, no brain, no friends. "
        "This could mean nothing."
      )


    elif win_rate < 0.35:
      self.your_animal = "Mantis Shrimp"
      self.your_animal_image = "Shrimp.png"
      self.your_animal_message = (
        "Wow. Your own family destroyed you. "
        "Nobody at this party will ever forgive you. Was it really worth it? "
        "Fun fact: The mantis shrimp can snap its claw at the speed of a .22 caliber bullet (so fast it produces light). "
        "It hunts by spearing, stunning, or dismembering its prey. "
        "You caused a similar level of damage today. Congrats, you're not invited next year."
      )

    elif win_rate < 0.5:
      self.your_animal = "New Guinea Amau Frog"
      self.your_animal_image = "Frog.png"
      self.your_animal_message = (
        "You lost more than you won. That's... I mean.... you tried? "
        "It could be worse, at least they don't ALL hate you. "
        "Fun fact: The New Guinea Amau frog is the world's smallest vertebrate animal, weighing approximately 10mg. "
        "Easy to miss. You didn't ruin the evening but you definitely tried. "
      )

    elif win_rate < 0.65:
      self.your_animal = "Long-Nosed Echidna"
      self.your_animal_image = "Echidna.png"
      self.your_animal_message = (
        "You are exceptionally mediocre. You won some... you lost some... everyone remains mildly annoyed at you. "
        "Fun fact: The long-nosed echidna mating ritual involves sad little 'trains' of males following females amd hoping for the best. "
        "(that's you!) "
        "I mean... could be worse. At least some people like you. "
      )

    elif win_rate < 1.0 or (total < 6):
      self.your_animal = "Helmeted Honeyeater"
      self.your_animal_image = "Bird.png"
      self.your_animal_message = (
        # "This could be worse! You resolved more problems than you caused. "
        "You resolved more problems than you caused! "
        "Most people actually like you! I mean. You're not solving any deeper issues here, but good job! "
        "Fun fact: helmeted honeyeaters are a cooperative species. The whole community works together to raise their chicks and defend their nests. "
        "That's already better than what your dad could manage! "
      )

    else:
      self.your_animal = "SugarBag Bee"
      self.your_animal_image = "Bees.png"
      self.your_animal_message = (
        "Wow. A perfect score. You resolved every single argument. "
        "Everyone came in ready to fight and somehow left feeling... okay? Impressive! "
        "Fun fact: unlike most bees, sugarbag bees are stingless. They don't need agression to protect their hive. "
        "Congrats on breaking the cycle and all that. "
      )



    # if total < 3:
    #   self.your_animal = "Clam"
    #   self.your_animal_message = "Man. You didn't even try." \
    #   "Did you even come to this party? Were you hiding in the bathroom the whole time?"

    #   self.your_animal_image = "Clam.png"

    # elif win_rate < 0.35:
    #   self.your_animal = "New Guinea Amau frog"
    #   self.your_animal_image = "Frog.png"
    #   self.your_animal_message = "Wow. Your own family destroyed you. " \
    #   "Half of these people still forward chain emails and you couldn't even beat them in an argument. Genuinely impressive. " \
    #   "Congrats on the failure."

    # elif win_rate < 0.5:
    #   self.your_animal = "Tortoise"
    #   self.your_animal_image = "Tortoise.png"
    #   self.your_animal_message = "You lost more than you won. That's... I mean.... you tried? " \
    #   "It could be worse, maybe they don't ALL hate you."

    # elif win_rate < 0.65:
    #   self.your_animal = "Log-Nosed Echidna"
    #   self.your_animal_image = "Echidna.png"
    #   self.your_animal_message = "Exceptionally mediocre. You won some. You lost some. Everyone is mildly annoyed at you." \
    #   "You didn't ruin their evening but you absolutely tried."

    # elif win_rate < 1.0:
    #   self.your_animal = "Honey Badger"
    #   self.your_animal_image = "Badger.png"
    #   self.your_animal_message = "Okay... wooowww. " \
    #   "You demolished most of your relationships and only ONE person managed to shut you up. " \
    #   "Congrats, you're not invited to next year's thing."


    # else:
    #   self.your_animal = "Mantis Shrimp"
    #   self.your_animal_image = "Shrimp.png"
    #   self.your_animal_message = "Wow. A perfect score. You won every argument. " \
    #   "Nobody at this party will ever forgive you. Was it really worth it?" \
    #   "This shrimp is capable of snapping it's creepy little claw at speeds which are comparable to that of a 22 caliber bullet, generating 15 hundred newtons of force (so fast it produces light)." \
    #   "It can hunt by either spearing, stunning or dismembering its prey. That's... kind of terrifying." \
    #   ""

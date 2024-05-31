
# a faire prochain cours
# dessiner carré contenant attaque possible
# dessiner attaque ordinateur
# capter clique de la souris sur l'écran

import random
from enum import Enum
import arcade
import arcade.gui

import attack_animation
from attack_animation import AttackType, AttackAnimation

FRONT_TEXT = "Appuyer sur une image pour faire une attaque!"
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roche, papier, ciseaux"
DEFAULT_LINE_HEIGHT = 45  # The default line height for text.
PLAYER_SCALE = 1
PLAYER_IMAGE_X = (SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)
PLAYER_IMAGE_Y = SCREEN_HEIGHT / 2.5
COMPUTER_IMAGE_X = (SCREEN_WIDTH / 2) * 1.5
COMPUTER_IMAGE_Y = SCREEN_HEIGHT / 2.5
ATTACK_FRAME_WIDTH = 154 / 2
ATTACK_FRAME_HEIGHT = 154 / 2


class GameState(Enum):
  NOT_STARTED = 0
  ROUND_DONE = 1
  GAME_OVER = 2
  ROUND_ACTIVE = 3




class MyGame(arcade.Window):
  """
  La classe principale de l'application

  NOTE: Vous pouvez effacer les méthodes que vous n'avez pas besoin.
  Si vous en avez besoin, remplacer le mot clé "pass" par votre propre code.
  """



  def __init__(self, width, height, title):
      super().__init__(width, height, title)

      arcade.set_background_color(arcade.color.BLACK_OLIVE)



      self.player = None
      self.computer = None
      self.players = None
      self.rock = None
      self.paper = None
      self.scissors = None
      self.player_score = 0
      self.computer_score = 0
      self.player_attack_type = {}
      self.computer_attack_type = None
      self.player_attack_chosen = False
      self.player_won_round = None
      self.draw_round = None
      self.game_state = GameState.NOT_STARTED
      self.attack = False
      self.pc_attack = None

  def setup(self):
      """
      Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
      fois si vous recommencer une nouvelle partie.
      """
      # C'est ici que vous allez créer vos listes de sprites et vos sprites.
      # Prenez note que vous devriez attribuer une valeur à tous les attributs créés dans __init__

      self.player_score = 0
      self.computer_score = 0
      self.player_attack_type = {}
      self.computer_attack_type = None
      self.player_attack_chosen = False
      self.player_won_round = None
      self.draw_round = None

      self.attack = False
      self.pc_attack = None

      self.player = arcade.Sprite("assets\player.png",0.3)
      self.player.center_x = PLAYER_IMAGE_X
      self.player.center_y = PLAYER_IMAGE_Y
      self.computer = arcade.Sprite("assets\compy.png", 1.5)
      self.computer.center_x = COMPUTER_IMAGE_X
      self.computer.center_y = COMPUTER_IMAGE_Y
      self.scissors = attack_animation.AttackAnimation(AttackType.SCISSORS)
      self.paper = attack_animation.AttackAnimation(AttackType.PAPER)
      self.rock = attack_animation.AttackAnimation(AttackType.ROCK)

      self.scissors_c = arcade.Sprite("assets\scissors.png", 0.5)
      self.paper_c = arcade.Sprite("assets\spaper.png", 0.5)
      self.rock_c = arcade.Sprite("assets\srock.png", 0.5)
      self.players = arcade.SpriteList()
      self.players.append(self.player)
      self.players.append(self.computer)





  def validate_victory(self):
      if self.computer_attack_type == self.player_attack_type:
          self.draw_round = True
      if self.computer_attack_type == AttackType.ROCK and self.player_attack_type == AttackType.PAPER:
          self.player_score += 1
          self.player_won_round = True
      elif self.computer_attack_type == AttackType.PAPER and self.player_attack_type == AttackType.ROCK:
          self.computer_score += 1
          self.player_won_round = False
      elif self.computer_attack_type == AttackType.SCISSORS and self.player_attack_type == AttackType.PAPER:
          self.computer_score += 1
          self.player_won_round = False
      elif self.computer_attack_type == AttackType.PAPER and self.player_attack_type == AttackType.SCISSORS:
          self.player_score += 1
          self.player_won_round = True
      elif self.computer_attack_type == AttackType.SCISSORS and self.player_attack_type == AttackType.ROCK:
          self.player_score += 1
          self.player_won_round = True
      elif self.computer_attack_type == AttackType.ROCK and self.player_attack_type == AttackType.SCISSORS:
          self.computer_score += 1
          self.player_won_round = False



  def draw_possible_attack(self):
      self.rock.center_x = 160
      self.rock.center_y = 155
      self.rock.draw()

      self.paper.center_x = 260
      self.paper.center_y = 155
      self.paper.draw()

      self.scissors.center_x = 360
      self.scissors.center_y = 155
      self.scissors.draw()







  def draw_scores(self):
      arcade.draw_text('Le pointage du joueur est: ' + str(self.player_score),
                       100,
                       70,
                       arcade.color.LIGHT_BLUE,
                       20)
      arcade.draw_text("Le pointage de l'ordinateur est: " + str(self.computer_score),
                       550,
                       70,
                       arcade.color.LIGHT_BLUE,
                       20)

  def draw_instructions(self):
      if self.game_state == GameState.ROUND_ACTIVE:
          arcade.draw_text(FRONT_TEXT,
                           0,
                           450,
                           arcade.color.LIGHT_BLUE,
                           30,
                           width=SCREEN_WIDTH,
                           align="center")

      elif self.game_state == GameState.GAME_OVER:
          if self.player_score == 3:
              arcade.draw_text("Vous gagnez la partie!",
                               0,
                               450,
                               arcade.color.LIGHT_BLUE,
                               30,
                               width=SCREEN_WIDTH,
                               align="center")
              arcade.draw_text("Appuyer sur 'ESPACE' pour débuter une nouvelle partie",
                               0,
                               400,
                               arcade.color.LIGHT_BLUE,
                               30,
                               width=SCREEN_WIDTH,
                               align="center")
          elif self.computer_score == 3:
              arcade.draw_text("Vous avez perdu la partie...",
                           0,
                           450,
                           arcade.color.LIGHT_BLUE,
                           30,
                           width=SCREEN_WIDTH,
                           align="center")
              arcade.draw_text("Appuyer sur 'ESPACE' pour débuter une nouvelle partie",
                           0,
                           400,
                           arcade.color.LIGHT_BLUE,
                           30,
                           width=SCREEN_WIDTH,
                           align="center")
      elif self.game_state == GameState.NOT_STARTED:
              arcade.draw_text("Appuyer sur 'ESPACE' pour commencer la ronde!",
                               0,
                               450,
                               arcade.color.LIGHT_BLUE,
                               30,
                               width=SCREEN_WIDTH,
                               align="center")

      elif self.game_state == GameState.ROUND_DONE:
              if self.player_won_round == False and self.draw_round == False:
                  arcade.draw_text("L'ordinateur a gagné la ronde!",
                                   0,
                                   350,
                                   arcade.color.LIGHT_BLUE,
                                   30,
                                   width=SCREEN_WIDTH,
                                   align="center")
              elif self.draw_round == True:
                  arcade.draw_text("Ronde nulle.",
                                   0,
                                   350,
                                   arcade.color.LIGHT_BLUE,
                                   30,
                                   width=SCREEN_WIDTH,
                                   align="center")
              elif self.player_won_round == True:
                  arcade.draw_text("Vous avez gagné gagné la ronde!",
                                   0,
                                   350,
                                   arcade.color.LIGHT_BLUE,
                                   30,
                                   width=SCREEN_WIDTH,
                                   align="center")



  def on_draw(self):


      arcade.start_render()

      arcade.draw_text(SCREEN_TITLE,
                       0,
                       SCREEN_HEIGHT - DEFAULT_LINE_HEIGHT * 2,
                       arcade.color.BLACK_BEAN,
                       60,
                       width=SCREEN_WIDTH,
                       align="center")

      # Display title


      arcade.draw_rectangle_outline(150,
                                     150,
                                     70,
                                     70, arcade.color.RED_BROWN)
      arcade.draw_rectangle_outline(250,
                                    150,
                                    70,
                                    70, arcade.color.RED_BROWN)
      arcade.draw_rectangle_outline(350,
                                    150,
                                    70,
                                    70, arcade.color.RED_BROWN)



      arcade.draw_rectangle_outline(770,
                                    150,
                                    70,
                                    70, arcade.color.RED_BROWN)
      if self.pc_attack == 0:

          self.rock_c.center_x = 780
          self.rock_c.center_y = 155
          self.rock_c.draw()
      elif self.pc_attack == 1:

          self.paper_c.center_x = 780
          self.paper_c.center_y = 155
          self.paper_c.draw()
      elif self.pc_attack == 2:

          self.scissors_c.center_x = 780
          self.scissors_c.center_y = 155
          self.scissors_c.draw()

      self.draw_instructions()
      self.players.draw()
      self.draw_possible_attack()
      self.draw_scores()




  def on_update(self, delta_time):
      self.rock.on_update()
      self.paper.on_update()
      self.scissors.on_update()
      if self.game_state == GameState.ROUND_ACTIVE and self.player_attack_chosen == True:
           self.pc_attack = random.randint(0, 2)

           if self.pc_attack == 0:
               self.computer_attack_type = AttackType.ROCK
           elif self.pc_attack == 1:
               self.computer_attack_type = AttackType.PAPER
           else:
               self.computer_attack_type = AttackType.SCISSORS
           self.validate_victory()
           self.game_state = GameState.ROUND_DONE



      if self.player_score == 3:
           self.game_state = GameState.GAME_OVER
      if self.computer_score == 3:
           self.game_state = GameState.GAME_OVER




  def on_key_press(self, key, key_modifiers):
      if self.game_state == GameState.NOT_STARTED:
          self.game_state = GameState.ROUND_ACTIVE

      if self.game_state == GameState.ROUND_DONE:
          self.reset_round()
          self.game_state = GameState.ROUND_ACTIVE

      if self.game_state == GameState.GAME_OVER:
          self.setup()
          self.game_state = GameState.NOT_STARTED

  def reset_round(self):
      """
      Réinitialiser les variables qui ont été modifiées
      """
      self.computer_attack_type = -1
      self.player_attack_chosen = False
      self.player_attack_type = {AttackType.ROCK: False, AttackType.PAPER: False, AttackType.SCISSORS: False}
      self.computer_attack_type = {AttackType.ROCK: False, AttackType.PAPER: False, AttackType.SCISSORS: False}
      self.player_won_round = False
      self.draw_round = False
      self.game_state = GameState.NOT_STARTED



  def on_mouse_press(self, x, y, button, key_modifiers):
      if self.rock.collides_with_point((x, y)):
          self.player_attack_type = AttackType.ROCK
          self.player_attack_chosen = True
      if self.paper.collides_with_point((x, y)):
          self.player_attack_type = AttackType.PAPER
          self.player_attack_chosen = True

      if self.scissors.collides_with_point((x, y)):
          self.player_attack_type = AttackType.SCISSORS
          self.player_attack_chosen = True



def main():
  """ Main method """
  game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
  game.setup()
  arcade.run()


if __name__ == "__main__":
  main()


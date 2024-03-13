from game.game import Game
from utils import getColor

import pygame
from pygame import KEYDOWN, QUIT, MOUSEBUTTONDOWN, KEYUP

from game.movement_utils import Movements


class Solo(Game):
    def __init__(self, level="1-1", resolution=(512, 480), fps=True, pause_color=getColor('BLUE'),
                 basic_movements=('up', 'down', 'left', 'right', 'A', 'B'), restart=False):
        super().__init__(level, resolution, fps, pause_color)

        self.restartOnFinish = restart
        self.lives = 2
        self.key_binding = {"Haut": pygame.K_z,
                            "Bas": pygame.K_s,
                            "Gauche": pygame.K_q,
                            "Droite": pygame.K_d,
                            "A": pygame.K_SPACE,
                            "B": pygame.K_LSHIFT}
        self.key_pressed = {key: False for key in self.key_binding.keys()}

        self.movements = Movements(basic_movements)

    # TODO: regler bug retour du niveau suivant
    def play(self) -> None:
        """
        Permet de lancer le mode solo de Super Mario Bros
        """
        Game.play(self)

        # Boucle principale
        done = True
        pause = False
        info = {"flag_get": False}

        # Action de base avant d'entrer dans le jeu NOOP → No Operation, Mario ne fait rien
        action = ['NOOP']

        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # Si on clique sur le bouton pause, on met le jeu en pause et on change l'image du bouton
                    if self.pause_rect.collidepoint(event.pos):
                        pause = self.activation_pause(pause)

                    elif self.back_rect.collidepoint(event.pos):
                        return None

                # Cherche quelles touches ont été pressées
                elif event.type == KEYDOWN:
                    for key in self.key_pressed.keys():
                        if event.key == self.key_binding[key]:
                            if "NOOP" in action:
                                action.remove("NOOP")
                            action.append(self.movements.translate_key_to_action(key))
                            self.key_pressed[key] = True

                # Cherche quelles touches ont été relâchées
                elif event.type == KEYUP:
                    for key in self.key_pressed.keys():
                        if event.key == self.key_binding[key] and self.key_pressed[key]:
                            while self.movements.translate_key_to_action(key) in action:
                                action.remove(self.movements.translate_key_to_action(key))
                            self.key_pressed[key] = False

            x = self.movements.translate_movement_user(action)

            # Si le jeu est en cours
            if not pause:
                if done:
                    if info["flag_get"]:
                        self.next_level()
                        self.key_pressed = {key: False for key in self.key_binding.keys()}
                        return self.play()

                    self.env.reset()

                # On actualise l'environnement du jeu en fonction des combinaisons de commandes de l'utilisateur
                ob, reward, done, info = self.env.step(x)

                # Rotation et conversion de l'état en surface Pygame pour adapter les modules gym et pygame entre eux
                surface = self.conversion_pygame(ob)

                # Affichage de la surface sur l'écran
                self.screen.blit(surface, (0, 0))
                self.screen.blit(self.pause_image, self.pause_rect)
            else:
                self.pause_on(surface)

            pygame.display.update()

            # Affichage de 60 FPS
            self.activation_fps()

import os

import numpy as np
import pygame
from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros

from utils import getColor
from game.movement_utils import Movements

import time

from abc import ABC, abstractmethod


class Game(ABC):
    """
    La classe Game est la classe mère des classes IA et Solo.
    Cette classe initie l'environnement de Super Mario Bros
    """

    def __init__(self, level: str = "1-1", resolution: tuple = (512, 480), fps: bool = False,
                 pause_color=getColor('BLUE')):
        """
        @param level: niveau du jeu [1~8-1~4]
        @param resolution: tuple de la taille du jeu
        @param fps: Si vrai le jeu est bloqué à 60 img/s, sinon illimité
        @param pause_color: la filtre de couleur du jeu en pause
        """
        self.level = level
        self.resolution = resolution
        self.fps = fps
        self.learning = 0
        self.pause_color = pause_color

        # initialise la classe mouvement
        self.movements = Movements(['left', 'right', 'up', 'down', 'A', 'B'])
        # environnement de Super Mario Bros
        self.env = None

        self.screen = pygame.display.set_mode(resolution)
        self.ico = pygame.image.load('./assets/logo.bmp')

        self.MARGIN_TOP = 25 * self.resolution[1] / 480
        self.MARGIN_RIGHT = 5 * self.resolution[0] / 512

        self.size_button = (40 * self.resolution[0] / 512, 40 * self.resolution[0] / 512)

        self.pause_image = pygame.image.load('./assets/pause.bmp')
        self.pause_image = pygame.transform.scale(self.pause_image, self.size_button)
        self.pause_rect = self.pause_image.get_rect()
        self.pause_filter = pygame.Surface(resolution)

        self.resume_image = pygame.image.load('./assets/resume.bmp')
        self.resume_image = pygame.transform.scale(self.resume_image, self.size_button)
        self.resume_rect = self.resume_image.get_rect()

        # Chargement de l'image pour le bouton retour
        self.back_image = pygame.image.load('./assets/back.bmp')
        self.back_image = pygame.transform.scale(self.back_image, self.size_button)
        self.back_rect = self.back_image.get_rect()

    def set_fps(self, fps: bool) -> None:
        """
        Modifier la valeur fps de la classe Game
        @param fps: Vrai bloque les fps, Faux laisse les FPS en 'illimité'
        """
        self.fps = fps

    def set_resolution(self, res: tuple) -> None:
        """
        Modifier la valeur resolution du jeu de la classe Game
        @param res: Tuple de la taille de la fenêtre
        """
        self.resolution = res

        self.MARGIN_TOP = 25 * self.resolution[1] / 480
        self.MARGIN_RIGHT = 5 * self.resolution[0] / 512

        self.pause_filter = pygame.Surface(res)
        self.size_button = (40 * self.resolution[0] / 512, 40 * self.resolution[0] / 512)

        self.pause_image = pygame.image.load('./assets/pause.bmp')
        self.pause_image = pygame.transform.scale(self.pause_image, self.size_button)
        self.pause_rect = self.pause_image.get_rect()

        self.resume_image = pygame.image.load('./assets/resume.bmp')
        self.resume_image = pygame.transform.scale(self.resume_image, self.size_button)
        self.resume_rect = self.resume_image.get_rect()

        # Chargement de l'image pour le bouton retour
        self.back_image = pygame.image.load('./assets/back.bmp')
        self.back_image = pygame.transform.scale(self.back_image, self.size_button)
        self.back_rect = self.back_image.get_rect()

    def set_level(self, level: str) -> None:
        """
        Modifie le level joué
        @param level: level de mario sous la forme n-n avec n compris entre 1 et 4
        """
        self.level = level

    def set_pause_color(self, color: tuple) -> None:
        """
        Modifier la couleur de la fenêtre de jeu en pause
        @param color: Tuple des valeurs RGB de la couleur
        """
        self.pause_color = color

    def set_movements(self, basic_movements: (str,)) -> None:
        """
        Modifie les mouvements de base de Mario
        @param basic_movements: tuple des mouvements de Mario
        """
        self.movements = Movements(basic_movements)

    def set_env(self) -> None:
        """
        Crée l'environnement de SuperMarioBros et les mouvements de Mario
        """
        self.env = gym_super_mario_bros.make('SuperMarioBros-' + self.level + '-v0')
        self.env = JoypadSpace(self.env, self.movements.get_all_movements())

    def next_level(self) -> None:
        """
        Permet de passer au niveau suivant de Mario
        """
        world = int(self.level[0])
        level = int(self.level[-1])

        if level + 1 > 4:
            self.level = str(world + 1) + "-1"
        else:
            self.level = str(world) + "-" + str(level + 1)

    def init_screen(self) -> None:
        """
        Initialise la page pygame du jeu
        """
        # Permet de centrer l'affichage des fenêtres
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        # Initialisation de la fenêtre
        self.screen = pygame.display.set_mode(self.resolution)
        self.ico = pygame.image.load('./assets/logo.bmp')
        pygame.display.set_icon(self.ico)

        pygame.display.set_caption("Projet: Super Mario Bros IA")
        pygame.display.set_icon(self.ico)
        self.pause_rect.topright = (self.screen.get_rect().right - self.MARGIN_RIGHT,
                                    self.screen.get_rect().top + self.MARGIN_TOP)

        self.pause_filter.fill(self.pause_color)
        self.pause_filter.set_alpha(128)

        self.resume_rect.topright = (self.screen.get_rect().right - self.MARGIN_RIGHT,
                                     self.screen.get_rect().top + self.MARGIN_TOP)

        # Positionnement du bouton retour
        self.back_rect.topleft = \
            (self.screen.get_rect().left + self.MARGIN_RIGHT, self.screen.get_rect().top + self.MARGIN_TOP)

    def conversion_pygame(self, ob):
        """
        Rotation et conversion de l'état en surface Pygame pour adapter les modules gym et pygame entre eux
        @param ob: environnement qu'affiche le jeu Mario
        @return: surface pygame de la page
        """
        ob = np.rot90(ob)
        surface = pygame.surfarray.make_surface(ob)
        surface = pygame.transform.scale(surface, self.resolution)
        surface = pygame.transform.flip(surface, True, False)
        return surface

    def pause_on(self, surface) -> None:
        """
        Filtre l'image et remplace le bouton pause
        @param surface: la surface pygame
        """
        self.screen.blit(surface, (0, 0))
        self.screen.blit(self.pause_filter, (0, 0))
        self.screen.blit(self.pause_image, self.pause_rect)
        self.screen.blit(self.back_image, self.back_rect)

    def quit(self) -> None:
        """
        Quitte l'environnement Mario et pygame
        """
        pygame.quit()
        self.env.close()
        exit()

    def activation_pause(self, pause: bool) -> bool:
        """
        Si pause : change l'image du bouton pause
        Sinon charge le bouton pause
        @param pause: état de pause du jeu
        @return: not pause
        """
        pause = not pause
        if pause:
            self.pause_image = self.resume_image
        else:
            self.pause_image = pygame.image.load('./assets/pause.bmp')
            self.pause_image = pygame.transform.scale(self.pause_image, self.size_button)

        return pause

    def activation_fps(self, t: int = 60) -> None:
        """
        Fait attendre 1/t secondes si fps est Vrai
        """
        if self.fps:
            wait_time = 1 / t
            time.sleep(wait_time)

    def play(self) -> None:
        """
        Permet d'initialiser l'environnement
        """

        pygame.display.set_mode(self.resolution)
        # creation environnement du jeu
        self.set_env()

        # Initialisation de l'environnement Super Mario Bros
        self.init_screen()

    def show(self, movement: bool) -> None:
        """
        Montre l'environnement utilisé
        @param movement: si Vrai Mario effectue des mouvements aléatoires sinon Mario ne fait rien
        """
        self.play()
        done = True
        action = 0
        while True:
            if done:
                self.env.reset()
            if movement:
                action = self.env.action_space.sample()
                print(self.movements.get_all_movements()[action])
            ob, _, done, _ = self.env.step(action)
            # Rotation et conversion de l'état en surface Pygame pour adapter les modules gym et pygame entre eux
            surface = self.conversion_pygame(ob)

            # Affichage de la surface sur l'écran
            self.screen.blit(surface, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            pygame.display.update()
            self.activation_fps()



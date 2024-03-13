import pickle
import os
import numpy as np
import neat
import cv2
import pygame
from pygame import QUIT, MOUSEBUTTONDOWN

from game.rewards import Rewards
from game.game import Game
from utils import getColor
from game.change_config_feedforward import change_outputs
from game.read_file import read_file


class StopTrainingException(Exception):
    pass


# TODO: renommer les chemins de fichiers de sauvegarde et ajouter des dossiers
# TODO: ajouter informations sur l'ecran pygame sur les information de l'IA (voit neat -> module qui le fait)
# TODO: enlever les libs/
class IA(Game):
    """
    Classe héritière de Game
    Cette classe permet de créer, sauvegarder et charger une IA sur Super Mario Bros
    """
    def __init__(self, level: str = "1-1", resolution: tuple = (512, 480), fps: bool = False,
                 pause_color=getColor('BLUE'), configuration: str = 'game/config-feedforward', type: str = 'speed'):
        """
        @param level: niveau du jeu [1~8-1~4]
        @param resolution: tuple de la taille du jeu
        @param fps: Si vrai le jeu est bloqué à 60 img/s, sinon illimité
        @param pause_color: la filtre de couleur du jeu en pause
        @param configuration: chemin du fichier de la configuration de neat
        @param type: type de l'IA (speed, coins, score)
        """

        super().__init__(level, resolution, fps, pause_color)
        # la classe qui permet de récompenser l'IA
        self.rewards = Rewards(type, level)

        # chemin pour accéder aux différents fichiers
        self.path_config = configuration
        self.path_checkpoint = "game/neat-checkpoint/"
        self.path_genome = "game/best_ia/"

        # type de l'IA
        self.type = type
        self.int_to_type = {0: 'speed', 1: 'coins'}

        # configuration neat créé à partir du fichier de config
        self.configuration = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                         neat.DefaultSpeciesSet, neat.DefaultStagnation, configuration)
        # Creation d'une population
        self.p = neat.Population(self.configuration)

    def set_path_checkpoint(self, path_checkpoint: str):
        self.path_checkpoint = path_checkpoint

    def set_path_genome(self, path_genome: str):
        self.path_genome = path_genome

    def set_level(self, level: str) -> None:
        Game.set_level(self, level)
        self.rewards.set_level(level)

    def set_config_movements(self, moves) -> None:
        """
        Modifie les mouvements de base de Mario et change la configuration de la population
        @param moves: liste des mouvements de Mario ou str des mouvements
        """
        change_outputs(self.path_config, len(moves))
        self.configuration = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                         neat.DefaultSpeciesSet, neat.DefaultStagnation, self.path_config)
        self.p = neat.Population(self.configuration)

    def set_type(self, t) -> None:
        """
        Modifie le type de l'IA
        @param t: type de l'IA, si t est de type int le convertit en str
        """
        self.type = t
        self.rewards.set_type(t)

    def dimension_env(self, div_x: int, div_y: int) -> (float, float):
        """
        Récupère la resolution du jeu et la divise en x et y.
        @param div_x: valeur de la division x
        @param div_y: valeur de la division y
        @return: tuple des resolutions x et y divisées
        """
        iny, inx, inc = self.env.observation_space.shape

        inx = int(inx / div_x)
        iny = int(iny / div_y)
        return inx, iny

    def dimension_pic(self, ob, dim: (float, float)):
        """
        Redimensionne l'environnement actuel pour réduire le nombre de données recu par l'IA
        @param ob: environnement qu'affiche le jeu Mario
        @param dim: dimension qu'affiche le jeu Mario
        @return: image simplifiée de l'image recue
        """
        # redimensionne l'image
        ob = cv2.resize(ob, dim)
        # convertit sur une palette de gris
        ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
        # aplati l'image en une matrice de dimensions inx par iny
        ob = np.reshape(ob, dim)

        # transforme l'image en une seule dimension
        imgarray = ob.flatten()

        return imgarray

    def eval_genomes(self, genomes, config):
        """
        Entrainment d'une génération de Mario
        @param genomes: ensemble des genes de notre IA
        @param config: les configurations choisies pour entrainer l'IA
        """
        for genome_id, genome in genomes:
            # reset de l'environnement
            ob = self.env.reset()

            # dimensions de l'environnement
            dim = self.dimension_env(8, 8)

            # Creation d'un reseau de neurones
            net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)

            # initialisation des variables pour fitness
            self.rewards.set_rewards()

            # si Faux la partie d'un Mario n'est pas fini, Vrai sinon
            done = False

            # si Faux la partie continue, sinon elle est mise en pause
            pause = False
            # boucle pour un individu
            while not done:

                # jeu en cours
                if not pause:
                    # enlève des informations inutiles a l'image pour l'IA
                    imgarray = self.dimension_pic(ob, dim)

                    # calculs des outputs
                    nnOutput = net.activate(imgarray)

                    # convertit les outputs en action de mario
                    action = self.movements.translate_outputs(nnOutput)
                    ob, _, done, info = self.env.step(action)

                    # rotation et conversion de l'état surface Pygame pour adapter les modules gym et pygame entre eux
                    surface = self.conversion_pygame(ob)

                    # Affichage de la surface sur l'écran
                    self.screen.blit(surface, (0, 0))
                    self.screen.blit(self.pause_image, self.pause_rect)

                    # calcule le fitness du genome actuel
                    done = self.rewards.calcul_rewards(info, done)
                    # actualise le fitness du genome actuel
                    genome.fitness = self.rewards.get_info()['fitness_current']

                    # à la fin de la partie d'un Mario indique son id et son niveau de fitness
                    if done:
                        print("id : ", genome_id, "fitness : ", genome.fitness)

                # jeu en pause
                else:
                    self.pause_on(surface)

                # événements pygame
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.quit()

                    elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                        # Si on clique sur le bouton pause, on met le jeu en pause et on change l'image du bouton
                        if self.pause_rect.collidepoint(event.pos):
                            pause = self.activation_pause(pause)

                        elif self.back_rect.collidepoint(event.pos):
                            raise StopTrainingException()

                # Affichage de 60 FPS
                self.activation_fps()

                pygame.display.update()

    def play(self) -> None:
        """
        Commence l'entrainement de Mario et sauvegarde le mario qui a réussi l'objectif
        lors de l'entrainement des générations sont sauvegardés sous la forme :
            ia_levelMario_typeMario_nombreMouvements_generation
        """
        # initialise l'environnement
        Game.play(self)

        # str des mouvements pour la sauvegarde de fichiers
        str_move = self.movements.translate_movements_to_str()
        # configuration des mouvements
        self.set_config_movements(str_move)

        # chemin de la sauvegarde des checkpoints
        name_file = 'ia_' + self.level + '_' + self.rewards.get_type() + '_' + str_move
        save_path = self.path_checkpoint + name_file

        # enregistrement statistique
        self.p.add_reporter(neat.StdOutReporter(True))
        # pour chaque generation
        stat = neat.StatisticsReporter()
        self.p.add_reporter(stat)

        # enregistre l'état de l'algorithme et fait une sauvegarde toute les 100 générations et les 30 minutes
        self.p.add_reporter(neat.Checkpointer(100, 1800, (save_path + '_')))

        print(self.movements.basic_movements)

        # lance l'entrainement de l'IA et si un retour en arrière est effectué on sauvegarde le meilleur mario
        try:
            winner = self.p.run(self.eval_genomes)
        except StopTrainingException:
            if "winner" not in locals():
                winner = self.p.best_genome
                save_path += '.save'

        if winner is not None:
            save_path = self.path_genome + name_file
            print("save at :", save_path)
            self.save_genome(winner, save_path)

    def load_genome(self, name_file: str) -> None:
        """
        Ouvre un fichier .pkl et lit le réseau de neurones du Mario
        @param name_file : nom fichier écrit sous la forme : ia_levelMario_typeMario_nombreMouvements.pkl
        """
        # chemin du fichier
        file_path = self.path_genome + name_file
        # information récupérer sur le nom du fichier
        name, level, type, moves = read_file(file_path)

        self.set_type(type)

        # configuration des mouvements
        self.movements.translate_str_to_movements(moves)
        self.set_config_movements(moves)

        index = file_path.rindex(".")
        if file_path[index:] == ".pkl":
            with open(file_path, "rb") as f:
                genome = pickle.load(f)

            Game.play(self)

            # Convertit genome pour qu'il puisse être élu par eval_genomes
            genomes = [(1, genome)]

            try:
                # L'IA fait le niveau
                self.eval_genomes(genomes, self.configuration)
            except StopTrainingException:
                print("Retour effectue")

    def load_checkpoint(self, name_file: str) -> None:
        """
        Reprend l'entrainement de Ma rio sélectionner
        @param name_file : nom du fichier de checkpoint sous la forme : ia_levelMario_typeMario_nombreMouvements_nbrGen
        """
        if "." in name_file:
            return None
        file_path = self.path_checkpoint + name_file
        name, level, type, moves, generation = read_file(file_path)

        self.set_type(type)
        print(self.type)
        self.movements.translate_str_to_movements(moves)
        self.set_config_movements(moves)

        Game.play(self)
        self.p = neat.Checkpointer().restore_checkpoint(file_path)

        # enregistrement statistique
        self.p.add_reporter(neat.StdOutReporter(True))
        stat = neat.StatisticsReporter()
        self.p.add_reporter(stat)

        str_move = (self.movements.translate_movements_to_str())

        name_file = 'ia_' + level + '_' + type + '_' + str_move
        save_path = self.path_checkpoint + name_file
        # enregistre l'état de l'algorithme
        self.p.add_reporter(neat.Checkpointer(100, 1800, (save_path + '_')))
        # reprend l'entrainement de l'IA
        try:
            winner = self.p.run(self.eval_genomes)
        except StopTrainingException:
            if "winner" not in locals() :
                winner = self.p.best_genome
                name_file += '.save'

        if winner is not None:
            save_path = self.path_genome + name_file
            print("save at :", save_path)
            self.save_genome(winner, save_path)

    def save_genome(self, genome: neat.genome.DefaultGenome, save_path: str) -> None:
        """
        Enregistre le réseau de neurones d'un mario
        @param genome: un genome mario
        @param save_path:  le chemin du fichier voulu
        """
        with open(save_path + '.pkl', 'wb') as output:
            pickle.dump(genome, output, 1)



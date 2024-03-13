import sys

import pygame
import os
from interface_graphique.button import Button
from game.solo import Solo
from interface_graphique.screen_create import ScreenCreate
from interface_graphique.screen_renderer import ScreenRenderer
from interface_graphique.sort_key import sort_key
from utils import get_font
from class_son.sounds import Sounds

from game.ia import IA

# Centrer l'affichage des fenêtres
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.display.set_caption("Projet: Super Mario Bros IA")
ico = pygame.image.load("assets/logo.png")
pygame.display.set_icon(ico)

# TODO: changer le mot IA FINALE
class Screen:

    def __init__(self, resolution=(1280, 720), margin_x=180, margin_y=100, hover_color=(255, 0, 0)):
        pygame.init()
        self.level = "1-1"
        self.create = ScreenCreate()
        self.render = ScreenRenderer()
        self.game_IA = IA()
        self.game_solo = Solo()
        self.option = "ECRAN"
        self.resolution = resolution
        self.base_resolution = resolution
        self.margin_x, self.margin_y = margin_x, margin_y
        self.margin_x_ratio, self.margin_y_ratio = self.margin_x / self.resolution[0], self.margin_y / self.resolution[
            1]
        self.hover_color = hover_color
        self.base_color = "#d7fcd4"
        self.min_spacing = 10

        self.screen = None

        self.background_file = os.path.join("assets", "background.jpg")

        self.font_size = int(resolution[1] * 0.08)
        self.base_font_size = self.font_size
        self.font_name = "./assets/font.ttf"
        self.font_file = self.font_file = os.path.join("assets", "font.ttf")
        self.font = pygame.font.Font("./assets/font.ttf", self.font_size)

        self.sound = Sounds()

        # TODO: Utiliser l'attribut Font plutôt que 4 attributs qui référence tous à une police
        # self.font = Font(resolution)

    def set_resolution(self, res):
        self.resolution = res
        self.render.update_margins(self)
        self.render.update_font_size(self)
        self.render.update_screen_resolution(self)

    def set_game_resolution(self, res):
        self.game_IA.set_resolution(res)
        self.game_solo.set_resolution(res)

    def set_game_level(self, level):
        self.game_IA.set_level(level)
        self.game_solo.set_level(level)

    def set_key_controls(self, y, maxWidth, textWidth) -> None:
        """
        Permet d'associer les contrôles de Mario au clavier
        :return None:
        """

        keyBinding = {}
        param = self.resolution[1] / 720
        FONTSIZE = 75

        # Enregistrer l'arrière-plan avant d'afficher les touches à assigner
        background = self.screen.copy()

        for key in self.game_solo.key_binding:
            # Afficher l'arrière-plan précédent pour effacer les touches assignées précédemment
            self.screen.blit(background, (0, 0))

            font = get_font(FONTSIZE)
            textKeyWidth = font.size(key)[0]
            espace_restant = maxWidth - textWidth - textKeyWidth

            # Création du texte de la commande à configurer :
            OPTIONS_TEXT_KEY = get_font(FONTSIZE).render(key, True, "#d7fcd4")
            OPTIONS_RECT_KEY = OPTIONS_TEXT_KEY.get_rect(
                topleft=(self.margin_x + textWidth + espace_restant, y * param))

            waiting = True
            while waiting:
                # Afficher le texte de la commande
                self.screen.blit(OPTIONS_TEXT_KEY, OPTIONS_RECT_KEY)
                pygame.display.flip()

                # Attendre une touche de clavier
                for event in pygame.event.get():

                    # Si on clique sur la croix cela ferme la fenêtre et le programme
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            return None
                        if event.key not in keyBinding.values():
                            keyBinding[key] = event.key
                            print(key, "a été associé à la touche", pygame.key.name(event.key).upper())
                            waiting = False

        # Afficher l'arrière-plan précédent pour effacer les touches précédemment entrées
        self.screen.blit(background, (0, 0))
        pygame.display.update()

        self.game_solo.key_binding = keyBinding

    def event_management(self, buttons: [Button], custom_actions: dict = None) -> None:
        """
        Gestion des événements pygame de base avec la croix qui arrête le processus
        ainsi que la gestion des boutons entrés en paramètre (si l'on clique cela effectuera la bonne action)
        :param buttons:
        :param custom_actions: Un dictionnaire contenant les actions personnalisées pour certains boutons
        :return:
        """

        self.resolution = self.resolution
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Gestion du clic sur les boutons
                for button in buttons:
                    if button.checkForInput((mouse_x, mouse_y)):
                        self.sound.playsong("click")
                        if custom_actions and button in custom_actions:
                            custom_actions[button]()
                            return None
                        elif button.action is not None:
                            eval(button.action)
                            return None

    def update_buttons(self, buttons: [Button]) -> None:
        """
        Permet de mettre à jour les boutons
        notamment leur couleur au passage de la souris ou au clic
        :param buttons:
        :return:
        """
        for button in buttons:
            button.changeColor(pygame.mouse.get_pos())
            button.update(self.screen)

    def calculate_font_size(self, options, min_spacing):
        font_size = self.font_size
        current_font = pygame.font.Font(self.font_name, font_size)

        available_space = self.resolution[0] - 2 * self.margin_x
        total_width = sum(current_font.size(option_text)[0] for option_text, _ in options) + (
                len(options) - 1) * min_spacing

        while total_width > available_space:
            font_size -= 1
            current_font = pygame.font.Font(self.font_name, font_size)
            total_width = sum(current_font.size(option_text)[0] for option_text, _ in options) + (
                    len(options) - 1) * min_spacing

        return font_size

    def calculate_font_height(self, text, available_height, min_spacing=10):
        current_font_size = self.font_size
        current_font = pygame.font.Font(self.font_name, current_font_size)
        text_height = current_font.size(text)[1]

        while text_height < available_height - min_spacing:
            current_font_size += 1
            current_font = pygame.font.Font(self.font_name, current_font_size)
            text_height = current_font.size(text)[1]

        return current_font_size - 1

    def init_screen(self):

        # Centrer l'affichage des fenêtres
        self.screen = pygame.display.set_mode(self.resolution)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption("Projet: Super Mario Bros IA")
        ico = pygame.image.load("./assets/logo.bmp")
        pygame.display.set_icon(ico)

    def main_menu(self):

        self.init_screen()

        title = "Menu Principal"

        buttons_data = [
            {"text": "NIVEAUX", "action": "self.levels()"},
            {"text": "OPTIONS", "action": "self.options_screen()"},
            {"text": "QUITTER", "action": "sys.exit()"}
        ]

        self.create.create_menu_window(self, title, buttons_data, True)

    def play_solo(self):
        self.game_solo.play()
        pygame.display.set_mode(self.resolution)
        self.choix_mode()

    def play_ia(self, *args):
        self.game_IA.play()
        pygame.display.set_mode(self.resolution)
        self.ia_menu()

    def choix_mode(self):

        title = "Choix du mode"

        buttons_data = [
            {"text": "IA", "action": "self.ia_menu()"},
            {"text": "SOLO", "action": "self.play_solo()"},
            {"text": "RETOUR", "action": "self.levels()"}
        ]

        self.create.create_menu_window(self, title, buttons_data)

    def options_screen(self) -> None:
        """
        Affiche le menu d'option d'écran à la fenêtre
        :return:
        """

        title = "ECRAN"

        # Options d'écran
        game_resolutions = [("768x700",(768, 700)), ("512x480", (512, 480)), ("256x240", (256, 240))]
        menu_resolutions = [("1280x720", (1280, 720)), ("1920x1080", (1920, 1080))]
        options_data = [
            {
                "desc text": "RESOLUTION JEU :",
                "fontsize": self.font_size,
                "method": "self.set_game_resolution",
                "attribute": "screen.game_IA.resolution",
                "options": game_resolutions
            },
            {
                "desc text": "RESOLUTION MENU :",
                "fontsize": self.font_size,
                "method": "self.set_resolution",
                "attribute": "screen.resolution",
                "options": menu_resolutions
            }
        ]

        self.create.create_option_window(self, options_data, title)

    def options_game(self) -> None:
        """
        Permet d'afficher le menu d'option de jeu à la fenêtre
        :return:
        """

        title = "JEU"

        # Options d'écran
        fps = [("ILLIMITE", False), ("60", True)]  # True veut dire qu'on limite les FPS
        options_data = [
            {
                "desc text": "FPS MODE IA :",
                "fontsize": self.font_size,
                "method": "self.game_IA.set_fps",
                "attribute": "screen.game_IA.fps",
                "options": fps
            }
        ]

        self.create.create_option_window(self, options_data, title)

    def configure_key(self, key):
        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    self.game_solo.key_binding[key] = event.key
                    waiting = False
                    self.options_controls()

    def configure_all_keys(self):
        controls = ["Haut", "Bas", "Gauche", "Droite", "A", "B"]

        for control in controls:
            self.configure_key(control)

    def options_controls(self, onStart=None) -> None:
        if onStart is not None:
            self.init_screen()

        title = "CONTROLES"
        controls = ["Haut", "Bas", "Gauche", "Droite", "A", "B"]

        options_data = []

        for index, control in enumerate(controls):
            current_key = pygame.key.name(self.game_solo.key_binding[control]).upper()

            options_data.append({
                "desc text": f"{control}: {current_key}",
                "fontsize": self.font_size // 2,
                "method": f"self.configure_key('{control}')",
                "attribute": "",
                "options": [],
                "position": (self.margin_x, self.margin_y * (index + 2))
            }
            )

        if onStart == "all":
            self.configure_all_keys()
            self.game_solo.play()
            return None

        self.create.create_option_window(self, options_data, title)


    def ia_menu(self):

        title = "IA"

        buttons_data = [
            {"text": "NOUVELLE IA", "action": "self.ia_options()"},
            {"text": "CHARGER CHECKPOINT", "action": "self.load_ia(self.game_IA.path_checkpoint)"},
            {"text": "CHARGER GENOME", "action": "self.load_ia(self.game_IA.path_genome, '.pkl')"},
            {"text": "RETOUR", "action": "self.choix_mode()"}
        ]

        self.create.create_menu_window(self, title, buttons_data)

    def ia_options(self):
        """
        Affiche le menu d'option d'écran à la fenêtre
        :return:
        """
        # TODO afficher en gris ou blanc le type IA choisi
        titles_data = [{"name": "PARAMETRES IA", "method": "self.ia_options()"}]

        title = "PARAMETRES IA"

        # Options d'écran
        types = [("RAPIDITE", "'speed'"), ("PIECES", "'coins'"), ("SCORE", "'score'"), ("SANS STOP", "'nostop'")]

        moves = [("GAUCHE", "'left'"), ("HAUT", "'up'"), ("BAS", "'down'"), ("B", "'B'")]
        dict_moves = []
        for move in moves:
            dict_moves.append({
                "desc text": "",
                "fontsize": self.font_size,
                "method": "self.game_IA.movements.add_movement",
                "attribute": f"screen.game_IA.movements.has_movement({move[1]})",
                "options": [(move[0], move[1])]
            })

        options_data = [
                           {
                               "desc text": "TYPE :",
                               "fontsize": self.font_size,
                               "method": "self.game_IA.set_type",
                               "attribute": "screen.game_IA.type",
                               "options": types
                           }

                       ] + dict_moves + [{"desc text": "",
                                          "fontsize": self.font_size,
                                          "method": "self.play_ia",
                                          "attribute": "True",
                                          "options": [("ACCEPTER", True)]}]

        self.create.create_option_window(self, options_data, title, titles_data, back_method="self.ia_menu()")

    def levels(self) -> None:
        """
        Permet d'afficher les niveaux disponibles du jeu
        :return None:
        """

        # Rafraichit le fond d'écran du menu
        self.render.render_option_background(self)

        # Définition de constant représentant la résolution de la fenêtre en 2 valeurs
        resMenuX = self.resolution[0]
        resMenuY = self.resolution[1]

        # TODO: Créer des fonctions pour raccourcir le code et le rendre plus simple au niveau du calcul des tailles des textes
        # Définition des polices et de leur taille du titre, des sous-titres monde, des niveaux et du back
        FONTSIZE_TITLE = 70
        font_title = get_font(FONTSIZE_TITLE)

        FONTSIZE_WORLD = 65
        FONTSIZE_LEVEL = 50
        font_level = get_font(FONTSIZE_LEVEL)

        FONTSIZE_BACK = 45

        # Définition d'un rapport entre les 2 polices
        rapportWL = FONTSIZE_WORLD / FONTSIZE_LEVEL
        textWidthWrld = textWidthLvl = 0
        maxWidth = resMenuX - self.margin_x * 2
        maxHeight = resMenuY - max(font_title.size("A")[1] + self.margin_y, self.margin_y * 2)

        test_width = test_height = True

        while test_width:

            # Calcul des largeurs pour centrer correctement à la fenêtre les textes et boutons
            FONTSIZE_LEVEL -= rapportWL * 2
            FONTSIZE_WORLD -= 2
            font_world = get_font(FONTSIZE_WORLD)
            textWidthWrld, textHeightWrld = font_world.size("MONDE 1")
            totalWidth = textWidthWrld * 4

            if totalWidth < maxWidth:
                test_width = False

        totalHeight = textHeightTitle = textHeightWrld = textHeightLvl = 0

        while test_height:

            # Calcul des hauteurs pour centrer correctement à la fenêtre les textes et boutons
            FONTSIZE_LEVEL -= rapportWL * 2
            FONTSIZE_WORLD -= 2
            font_level = get_font(int(FONTSIZE_LEVEL))
            font_world = get_font(FONTSIZE_WORLD)
            textWidthLvl, textHeightLvl = font_level.size("Lvl 1")
            textWidthWrld, textHeightWrld = font_world.size("MONDE 1")
            totalHeight = textHeightWrld * 2 + textHeightLvl * 8

            if totalHeight < maxHeight:
                test_height = False

        # Calcul des espaces non utilisés par les boutons et textes
        espace_restantY = (maxHeight - totalHeight) / 9
        totalWidth = textWidthWrld * 4
        espace_restantX = (maxWidth - totalWidth) / 3
        margin_center_level = (textWidthWrld - textWidthLvl) / 2

        def check_existing_file(level_name: str) -> bool:
            file_prefix = f'ia_{level_name}'
            for file in os.listdir(self.game_IA.path_genome):
                if file.startswith(file_prefix) and file.endswith('.pkl') and 'save' not in file:
                    return True
            return False

        # Création dynamique de chaque bouton pour les niveaux du jeu
        buttonLevels = []

        for world in range(8):
            if world < 4:
                worldY = max(textHeightTitle // 1.5, self.margin_y)
                worldX = espace_restantX * world + textWidthWrld * world + self.margin_x
            else:
                worldY = max(textHeightTitle // 1.5,
                             self.margin_y) + textHeightWrld + textHeightLvl * 4 + espace_restantY * 5
                worldX = espace_restantX * (world - 4) + textWidthWrld * (world - 4) + self.margin_x

            world_texte = get_font(FONTSIZE_WORLD).render("MONDE " + str(world + 1), True, "#b68f40")
            world_rect = world_texte.get_rect(topleft=(worldX, worldY))
            self.screen.blit(world_texte, world_rect)

            worldY += textHeightWrld + espace_restantY

            for level in range(4):
                level_name = str(world + 1) + "-" + str(level + 1)
                base_color = "#d7fcd4" if check_existing_file(level_name) else "#000000"

                buttonLevels.append(
                    Button(image=None,
                           pos=(worldX + margin_center_level, worldY),
                           text_input="Lvl " + str(level + 1),
                           font=get_font(int(FONTSIZE_LEVEL)),
                           base_color=base_color,
                           hovering_color=self.hover_color))

                worldY += textHeightLvl + espace_restantY

        info_color_text = "Couleur verte : IA finit le niveau | Couleur noire : IA ne finit pas le niveau"
        info_color_font = get_font(30)
        info_color_surface = info_color_font.render(info_color_text, True, "#b68f40")
        info_color_rect = info_color_surface.get_rect(center=(resMenuX // 2, resMenuY - 50))
        self.screen.blit(info_color_surface, info_color_rect)

        while True:

            # Récupération de la position de la souris
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Création des boutons
            for button in buttonLevels:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            BACK_BUTTON = Button(image=None,
                                 pos=(30, 30),
                                 text_input="RETOUR", font=get_font(FONTSIZE_BACK), base_color="#d7fcd4",
                                 hovering_color=self.hover_color)

            # Création du texte Niveaux en en-tête
            MENU_TEXT = get_font(80).render("Niveaux", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(
                center=(resMenuX / 2, textHeightTitle + 55 * resMenuY / self.base_resolution[1]))
            self.screen.blit(MENU_TEXT, MENU_RECT)

            # Change la couleur des boutons au passage de la souris dessus
            for button in [BACK_BUTTON] + buttonLevels:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            # Récupération des événements
            for event in pygame.event.get():
                # Clic sur la croix en haut à droite de la fenêtre, ferme la fenêtre et le programme
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Au clic gauche de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clic sur retour alors on revient au menu principal
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.sound.playsong('click')
                        self.main_menu()
                    world, level = 1, 0
                    # Vérification si le clic est effectué sur un bouton
                    for button in buttonLevels:
                        level += 1
                        if level > 4:
                            world += 1
                            level = 1
                        if button.checkForInput(MENU_MOUSE_POS):
                            self.sound.playsong('click')
                            self.set_game_level(str(world) + "-" + str(level))
                            self.choix_mode()

            pygame.display.update()

    def load_ia(self, folder, type_load=None):
        """
        Menu pour charger les IA
        :return None:
        """
        def list_checkpoint_files(level: str) -> list:
            # TODO explication
            checkpoint_files = []
            for file in os.listdir(folder):
                if file.startswith(f'ia_{level}_') and "." not in file:
                    checkpoint_files.append(file)
            return checkpoint_files

        def list_ai_files(level: str) -> list:
            ia_files = []
            for file in os.listdir(folder):
                if file.startswith(f'ia_{level}_') and file.endswith(type_load):
                    ia_files.append(file)
            return ia_files

        if type_load is None:
            ai_files = list_checkpoint_files(self.game_solo.level)
            ai_files = sorted(ai_files, key=sort_key)
        else:
            ai_files = list_ai_files(self.game_solo.level)
        ai_buttons = []

        FONTSIZE_FILE = int(20 * (self.resolution[0]/1280))
        font_file = get_font(FONTSIZE_FILE)
        FONTSIZE_BACK = 45

        # Position initiale des boutons de fichiers
        x = self.margin_x - 100
        y = self.margin_y

        # Création des boutons pour chaque fichier
        for file in ai_files:
            ai_buttons.append(
                Button(image=None,
                       pos=(x, y),
                       text_input=file,
                       font=font_file,
                       base_color="#d7fcd4",
                       hovering_color=self.hover_color))
            if y < self.resolution[1]-100:
                y += 50 * (self.resolution[0]/1920)
            else:
                y = self.margin_y
                x += 300 * (self.resolution[0]/1920)

        while True:
            # Récupération de la position de la souris
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            # Rafraichit le fond d'écran du menu
            self.render.render_option_background(self)

            # Création du bouton Retour
            BACK_BUTTON = Button(image=None,
                                 pos=(30, 30),
                                 text_input="RETOUR", font=get_font(FONTSIZE_BACK), base_color="#d7fcd4",
                                 hovering_color=self.hover_color)

            # Change la couleur des boutons au passage de la souris dessus
            for button in ai_buttons + [BACK_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(self.screen)

            # Récupération des événements
            for event in pygame.event.get():
                # Clic sur la croix en haut à droite de la fenêtre, ferme la fenêtre et le programme
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Au clic gauche de la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si clic sur retour alors on revient au menu précédent
                    if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.sound.playsong('click')
                        self.choix_mode()

                    # Vérification si le clic est effectué sur un bouton de fichier
                    for button, file in zip(ai_buttons, ai_files):
                        if button.checkForInput(MENU_MOUSE_POS):
                            self.sound.playsong('click')
                            # Chargez l'IA à partir du fichier sélectionné ici
                            print(f"Chargement de l'IA depuis {file}")
                            # Vous pouvez appeler une méthode pour charger l'IA en utilisant le nom du fichier

                            if file.endswith('.pkl'):
                                self.game_IA.load_genome(file)
                            else:
                                self.game_IA.load_checkpoint(file)
                            pygame.display.set_mode(self.resolution)
                            self.choix_mode()
            pygame.display.update()

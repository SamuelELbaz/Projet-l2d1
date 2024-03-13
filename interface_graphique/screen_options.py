import sys

import pygame

from interface_graphique.button import Button
from utils import get_font

titles_data = [
    {"name": "ECRAN", "method": "self.options_screen()"},
    {"name": "CONTROLES", "method": "self.options_controls()"},
    {"name": "JEU", "method": "self.options_game()"}
]


def create_option_window(self, options_data, title_option, titles_data=titles_data, back_method="self.main_menu()"):
    self.option = title_option

    # Ajout du fond d'écran du menu option à l'écran
    self.render_option_background()

    # Espace des titres des options à
    title_spacing = int(self.resolution[0] * 0.05)

    # Bouton Retour
    back_button = Button(None, (
        self.resolution[0] // 2 - self.font.size("Retour")[0] // 2, self.resolution[1] - self.margin_y), "RETOUR",
                         self.font, self.base_color, self.hover_color, back_method)

    # Boutons d'options et des titres
    option_title_buttons = self.create_option_title_buttons(title_spacing, titles_data)
    has_options = sum([len(option_data["options"]) for option_data in options_data]) > 0

    running = True
    buttons = []
    while running:
        if options_data and has_options:
            option_buttons = self.create_option_buttons(options_data)
            buttons += option_buttons + option_title_buttons + [back_button]
            # Dessiner le texte des options
            self.draw_options_text(options_data)
        elif options_data:
            y = 0
            for option_data in options_data:
                button = Button(None, (self.margin_x, self.margin_y + y), option_data["desc text"], self.font,
                                self.base_color, self.hover_color, option_data["method"])
                buttons.append(button)
                y += 1
            buttons += option_title_buttons + [back_button]
        else:
            buttons += option_title_buttons + [back_button]
        # Gestion des événements
        self.event_management(buttons)

        # Mise à jour des boutons
        self.update_buttons(buttons)

        # Mise à jour de la surface d'affichage complète à l'écran
        pygame.display.flip()


def options_screen(self) -> None:
    """
    Affiche le menu d'option d'écran à la fenêtre
    :return:
    """

    title = "ECRAN"

    # Options d'écran
    game_resolutions = [("512x480", (512, 480)), ("256x240", (256, 240))]
    menu_resolutions = [("1280x720", (1280, 720)), ("1920x1080", (1920, 1080))]
    options_data = [
        {
            "desc text": "RESOLUTION JEU :",
            "fontsize": self.font_size,
            "method": "self.game_IA.set_resolution",
            "attribute": "self.game_IA.resolution",
            "options": game_resolutions
        },
        {
            "desc text": "RESOLUTION MENU :",
            "fontsize": self.font_size,
            "method": "self.set_resolution",
            "attribute": "self.resolution",
            "options": menu_resolutions
        }
    ]

    create_option_window(self, options_data, title)


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
            "attribute": "self.game_IA.fps",
            "options": fps
        }
    ]

    create_option_window(self, options_data, title)


def options_controls(self) -> None:
    """
    Permet d'afficher le menu d'option des contrôles à la fenêtre
    :return:
    """

    title = "CONTROLES"

    # Options d'écran
    options_data = [
        {
            "desc text": "CONFIGURER TOUTES LES TOUCHES",
            "fontsize": self.font_size,
            "method": "self.set_key_controls(100, 1000, 300)",
            "attribute": "",
            "options": []
        }
    ]

    create_option_window(self, options_data, title)


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

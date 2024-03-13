import os
import pygame

from interface_graphique.button import Button
from interface_graphique.screen_renderer import ScreenRenderer


titles_data = [
            {"name": "ECRAN", "method": "self.options_screen()"},
            {"name": "CONTROLES", "method": "self.options_controls()"},
            {"name": "JEU", "method": "self.options_game()"}
        ]


class ScreenCreate:

    def __init__(self):
        self.render = ScreenRenderer()

    def create_option_window(self, screen, options_data, title_option, titles_data=titles_data, back_method="self.main_menu()"):
        screen.option = title_option
    
        # Ajout du fond d'écran du menu option à l'écran
        self.render.render_option_background(screen)
    
        # Espace des titres des options à
        title_spacing = int(screen.resolution[0] * 0.05)
    
        # Bouton Retour
        back_button = Button(None, (
            screen.resolution[0] // 2 - screen.font.size("Retour")[0] // 2, screen.resolution[1] - screen.margin_y), "RETOUR",
                             screen.font, screen.base_color, screen.hover_color, back_method)
    
        # Boutons d'options et des titres
        option_title_buttons = self.create_option_title_buttons(screen, title_spacing, titles_data)
        has_options = sum([len(option_data["options"]) for option_data in options_data]) > 0
    
        running = True
        buttons = []
        while running:
            if options_data and has_options:
                option_buttons = self.create_option_buttons(screen, options_data)
                buttons += option_buttons + option_title_buttons + [back_button]
                # Dessiner le texte des options
                self.render.draw_options_text(screen, options_data)
            elif options_data:
                y = 1
                for option_data in options_data:
                    button = Button(None, (screen.margin_x, screen.margin_y * y), option_data["desc text"], screen.font,
                                    screen.base_color, screen.hover_color, option_data["method"])
                    buttons.append(button)
                    y += 1
                buttons += option_title_buttons + [back_button]
            else:
                buttons += option_title_buttons + [back_button]
            # Gestion des événements
            screen.event_management(buttons)
    
            # Mise à jour des boutons
            screen.update_buttons(buttons)
    
            # Mise à jour de la surface d'affichage complète à l'écran
            pygame.display.flip()

    def create_option_buttons(self, screen, options_data):
        option_buttons = []
        for i, option_data in enumerate(options_data):
            # Calculer la taille de police optimale
            optimal_font_size = screen.calculate_font_size(option_data["options"], screen.min_spacing)
    
            # Créer une nouvelle police avec la taille optimale
            optimal_font = pygame.font.Font(screen.font_name, optimal_font_size)
    
            self.render.draw_text(screen, option_data["desc text"], screen.base_color, screen.font, screen.margin_x,
                           screen.margin_y + i * optimal_font.size(option_data["desc text"])[1])
    
            total_option_width = sum(optimal_font.size(option_text)[0] for option_text, _ in option_data["options"])
            available_space = screen.resolution[0] - 2 * screen.margin_x - optimal_font.size(option_data["desc text"])[
                0] - total_option_width
            equal_spacing = available_space / (len(option_data["options"]))
            option_x = screen.margin_x + optimal_font.size(option_data["desc text"])[0] + equal_spacing
    
            for option_text, option_value in option_data["options"]:
                is_selected = eval(option_data["attribute"]) == option_value
                color = screen.base_color if is_selected else (0, 0, 0)
                action_str = f"{option_data['method']}({option_value})"
                button = Button(None, (option_x, screen.margin_y + i * optimal_font.size(option_data["desc text"])[1]),
                                option_text, optimal_font, color,
                                screen.hover_color, action_str)
                option_buttons.append(button)
                option_x += optimal_font.size(option_text)[0] + equal_spacing
        return option_buttons

    @staticmethod
    def create_option_title_buttons(screen, title_spacing, titles_data):
        option_title_buttons = []
    
        # Calcul de l'espacement et la position initiale des boutons
        title_x = (screen.resolution[0] - sum(screen.font.size(action["name"])[0] for action in titles_data) -
                   (len(titles_data) - 1) * title_spacing) // 2
    
        # Création des boutons
        for action_data in titles_data:
            title = action_data["name"]
            is_selected = screen.option == title
            color = screen.base_color if is_selected else (0, 0, 0)
            action = action_data["method"]
    
            button = Button(None, (title_x, screen.margin_y // 8), title, screen.font, color, screen.hover_color, action)
            option_title_buttons.append(button)
            title_x += screen.font.size(title)[0] + title_spacing
    
        return option_title_buttons

    @staticmethod
    def create_buttons(screen, buttons_data, title_height, height_button_ratio, height_button_spacing):
        buttons = []
        button_height = int(screen.resolution[1] * height_button_ratio)
        button_spacing = int(screen.resolution[1] * height_button_spacing)
        y_position = screen.margin_y + title_height + button_spacing
    
        for button_data in buttons_data:
            button_text_width, _ = screen.font.size(button_data["text"])
            button_x = (screen.resolution[0] - button_text_width) // 2
            button = Button(None, (button_x, y_position), button_data["text"], screen.font,
                            screen.base_color, screen.hover_color, button_data["action"])
            buttons.append(button)
            y_position += button_height + button_spacing
    
        return buttons

    def create_menu_window(self, screen, title, buttons_data, main=False):
        if main:
            self.render.render_background(screen, "./assets/background.bmp")
        else:
            self.render.render_option_background(screen)
    
        title_font_size = screen.calculate_font_height(title, screen.resolution[1] * 0.15)
        title_font = pygame.font.Font(screen.font_name, title_font_size)
        title_width, title_height = title_font.size(title)
    
        # Création du titre et des boutons
        self.render.draw_text(screen, title, "#b68f40", title_font, screen.resolution[0] // 2 - title_width // 2, screen.margin_y // 1.5)
    
        # Calcul de la hauteur totale des boutons et des espacements
        total_buttons_height = len(buttons_data) * screen.resolution[1] * 0.25
        total_spacing_height = (len(buttons_data) - 1) * screen.resolution[1] * 0.01
        total_height = total_buttons_height + total_spacing_height
    
        # Ajustement de la hauteur des boutons et des espacements
        available_height = screen.resolution[1] - title_height - screen.margin_y
        height_button_ratio = (available_height * 0.25) / total_height
        height_button_spacing = (available_height * 0.01) / total_height
    
        buttons = self.create_buttons(screen, buttons_data, title_height, height_button_ratio, height_button_spacing)
    
        running = True
        while running:
            screen.update_buttons(buttons)
            screen.event_management(buttons)
    
            pygame.display.flip()

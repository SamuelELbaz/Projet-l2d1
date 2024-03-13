import pygame
import os


def refresh_buttons(screen, OPTIONS_MOUSE_POS, category: list) -> None:
    """
    Permet de rafraichir tous les boutons notamment leur couleur
    :return:
    """

    for options in category:
        for opt in options:
            opt.changeColor(OPTIONS_MOUSE_POS)
            opt.update(screen)


def refresh_background(Interface, background: str) -> None:
    """
    La méthode permet de rafraichir le fond d'écran dans les menus
    :param background: Le nom du fichier de l'image
    :return None:
    """

    image = pygame.image.load(background)
    image = pygame.transform.scale(image, Interface.resolution)
    Interface.SCREEN.blit(image, (0, 0))


def refresh_option_menu(Interface) -> None:
    """
    La méthode permet de rafraichir la fenêtre du menu d'options
    :return: None
    """

    pygame.init()
    Interface.refresh_background("/assets/background-options.bmp")

    # Dessiner le filtre semi-transparent noir sur l'image de fond
    overlay = pygame.Surface(Interface.resolution, pygame.SRCALPHA)
    pygame.draw.rect(overlay, (0, 0, 0, 200), (0, 0, Interface.resolution[0], Interface.resolution[1]))
    Interface.SCREEN.blit(overlay, (0, 0))
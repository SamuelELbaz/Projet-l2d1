import pygame

# Plusieurs couleurs définies
COLORS = {
    "BLACK": (0, 0, 0),
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "PURPLE": (255, 0, 255),
    "LIGHT_BLUE": (92, 225, 230)
}


def getColor(name: str) -> tuple:
    """
    :param name: Nom de la couleur
    :return tuple: Le tuple de la couleur
    """
    return COLORS[name]


def get_font(size: int) -> pygame.font.Font:
    """
    Récupère une police de caractères à partir de la taille spécifiée
    :param size: Taille de la police
    :return pygame.font.Font: La police de caractères
    """
    pygame.init()
    return pygame.font.Font("assets/font.ttf", size)


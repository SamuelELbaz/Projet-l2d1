
def read_file(file_path: str) -> list:
    """
    Lit file_path et retourne le contenu de chaque lignes
    @param file_path: le chemin d'un fichier
    @return la liste des lignes du fichier
    """
    # Ouvrir le fichier en mode lecture et enregistrer chaque ligne dans une liste
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines


def write_file(file_path: str, lines: list) -> None:
    """
    Ecrit sur file_path le contenu de lines
    @param file_path: le chemin d'un fichier
    @param lines: liste du contenu de chaque ligne
    """
    # Ouvrir le fichier en mode écriture et écrire chaque ligne modifiée dans le fichier
    with open(file_path, 'w') as file:
        file.writelines(lines)


def change_outputs(file_path: str, nb_outputs: int) -> None:
    """
    Modifie le paramètre outputs de file_path par nb_outputs
    @param file_path: le chemin d'un fichier config de neat
    @param nb_outputs: le nombre d'outputs
    """
    # Ouvrir le fichier en mode lecture et enregistrer chaque ligne dans une liste
    lines = read_file(file_path)

    nb_outputs = str(nb_outputs)
    # Modifier la ligne souhaitée
    lines[50] = 'num_outputs             = '+nb_outputs+'\n'  # Notez que les index des listes commencent à 0

    write_file(file_path, lines)


def change_pop_size(file_path: str, pop_size: int) -> None:
    """
    Modifie le paramètre de taille de la population de file_path par pop_size
    @param file_path: le chemin d'un fichier config de neat
    @param pop_size: le nombre d'individus d'une population neat
    """
    # Ouvrir le fichier en mode lecture et enregistrer chaque ligne dans une liste
    lines = read_file(file_path)

    pop_size = str(pop_size)
    # Modifier la ligne souhaitée
    lines[3] = 'pop_size              = '+pop_size+'\n'

    write_file(file_path, lines)

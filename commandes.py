import argparse
import os

def setFPS(fps):
    """
    Savoir si l'on joue avec FPS illimité ou à 60
    :param fps:
    :return True = FPS Bloqué à 60 ; False = FPS non bloqués :
    """
    if fps == "Unlimited":
        return False
    if fps == "60":
        return True
    else:
        return False


def setResolution(resolution: tuple):
    """
    Demande à l'utilisateur en quelle résolution il veut jouer
    :param resolution:
    :return:
    """
    print(resolution)
    if isinstance(resolution, tuple):
        # L'utilisateur a entré un argument pour --resolution
        return resolution
    else:
        while resolution not in [0, 1, 2]:
            # L'utilisateur n'a pas entré d'argument pour --resolution
            # Affichage des différentes résolutions possibles
            print("Tapez 0 pour 512x480")
            print("Tapez 1 pour 256x240")
            print("Tapez 2 pour 768x720")
            # Demande à l'utilisateur d'entrer un argument pour --resolution
            resolution = int(input("\n-> "))

    if resolution == 0:
        resolution = (512, 480)
    elif resolution == 1:
        resolution = (256, 240)
    elif resolution == 2:
        resolution = (768, 720)

    print("Résolution : " + str(resolution))
    return resolution

def get_file_step(level, type = 'speed'):
    
    ia_files = []
    for file in os.listdir('./game/show_evolution/'):
        if file.startswith(f'ia_{level}_{type}') and file.endswith(".pkl"):
            ia_files.append(file)

    step = -2

    while step < -1 or step > len(ia_files):
        # Affichage des différents fichiers disponibles
        for i, file in enumerate(ia_files):
            print(f"Tapez {i} pour charger le fichier {file}")
        # Demande à l'utilisateur d'entrer un argument pour --step
        print("Tapez -1 pour quitter la sélection")
        step = int(input("\n-> "))
    if step == -1:
        return None
    print(f"Le fichier {ia_files[step]} a été choisi")
    return ia_files[step]

def setType(type):
    if isinstance(type, str):
        # L'utilisateur a entré un argument pour --type
        return type
    else:
        while type not in [0, 1, 2, 3]:
            # L'utilisateur n'a pas entré d'argument pour --type
            # Affichage des différentes résolutions possibles
            print("Tapez 0 pour speed")
            print("Tapez 1 pour coins")
            print("Tapez 2 pour score")
            print("Tapez 3 pour nostop")
            # Demande à l'utilisateur d'entrer un argument pour --type
            type = int(input("\n-> "))

    if type == 0:
        type = "speed"
    elif type == 1:
        type = "coins"
    elif type == 2:
        type = "score"
    elif type == 3:
        type = "nostop"

    print("Type : " + type)
    return type

# TODO: fermer show step si aucun niveau fini et choisir le type et le mouvement
# TODO : charger genome/checkpoint avec le terminal
# Création de l'analyseur d'arguments
parser = argparse.ArgumentParser(description="IA qui apprend à jouer à Super Mario Bros")

# Définition des commandes disponibles
subparsers = parser.add_subparsers(title="Commandes disponibles", dest="command")

# Définition de la commande "ia"
ia_parser = subparsers.add_parser("ia", help="Lancer le jeu avec le mode IA")


ia_parser.add_argument("--resolution", "-r", nargs='?', type=lambda x: tuple(map(int, x.strip('()').split(','))), default=(512, 480),
                       help="Affiche différentes résolutions disponibles à choisir si entré sans argument sinon entrez un tuple valide (Ex: '(512, 480)')")
ia_parser.add_argument("--type", "-t", type=str, default='speed', nargs='?',
                       help="Choix de l'objectif de l'IA lors de sa création : speed par défaut | coins | score | nostop")
ia_parser.add_argument("--level", "-lv", type=str, default='1-1', nargs='?',
                       help="Choix du niveau : <world, 1 par défaut>-<level, 1 par défaut>")
ia_parser.add_argument("--fps", default="Unlimited", type=str, nargs='?', help="Nombre de FPS")
ia_parser.add_argument("--genomeload", "-gload", type=str, nargs='?',
                       help="Charger une IA qui est sauvegardée en renseignant le nom du fichier")

ia_parser.add_argument("--populationload", "-pload", type=str, nargs='?',
                       help="Recharger une IA pour continuer à l'entrainer en renseignant le nom du fichier")
ia_parser.add_argument("--movements", "-m", type=lambda x: list(map(str, x.strip('[]').split(','))), default=['left', 'right', 'up', 'down', 'A', 'B'], nargs='?',
                       help="Choix du nombre de mouvements utilisés pour la création d'une IA")

# Définition de la commande "show"
show_parser = subparsers.add_parser("show", help="Lancer l'IA pré-entraîné")
show_parser.add_argument("--resolution", "-r", nargs='?', type=lambda x: tuple(map(int, x.strip('()').split(','))), default=(512, 480),
                       help="Affiche différentes résolutions disponibles à choisir si entré sans argument sinon entrez un tuple valide (Ex: '(512, 480)')")
show_parser.add_argument("--type", "-t", type=str, default='speed', nargs='?',
                       help="Choix de l'objectif de l'IA lors de sa création : speed par défaut | coins | score | nostop")
show_parser.add_argument("--level", type=str, default='1-1', nargs='?',
                       help="Choix du niveau : <world, 1 par défaut>-<level, 1 par défaut>")
show_parser.add_argument("--step", action="store_true", help="Affiche l'IA à une étape d'apprentissage")
show_parser.add_argument("--movement", action="store_true", help="Mario utilise les différents contrôles du jeu")

# Définition de la commande "solo"
solo_parser = subparsers.add_parser("solo", help="Lance le jeu en avec le mode solo")
solo_parser.add_argument("--resolution", "-r", nargs='?', type=lambda x: tuple(map(int, x.strip('()').split(','))), default=(512, 480),
                       help="Affiche différentes résolutions disponibles à choisir si entré sans argument sinon entrez un tuple valide (Ex: '(512, 480)')")
solo_parser.add_argument("--level", "-l", type=str, default='1-1', nargs='?',
                         help="Choix du niveau : <world, 1 par défaut>-<level, 1 par défaut>")
solo_parser.add_argument("--fps", "-f", default="60", type=str, nargs='?', help="Nombre de FPS")
solo_parser.add_argument("--keyboard", "-kb", default=None, type=str, nargs='?', help="Configurer les touches du jeu")

# Analyse des arguments de la ligne de commande
args = parser.parse_args()

# Exécution de la commande sélectionnée
if args.command == "ia":
    print("Lancement du jeu avec le mode IA")
elif args.command == "show":
    print("Lancement du jeu en présentation")
elif args.command == "solo":
    print("Lancement du jeu avec le mode solo")
else:
    parser.print_help()

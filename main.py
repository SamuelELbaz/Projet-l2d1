import encodings
import commandes
from interface_graphique.screen import Screen
from game.ia import IA
from game.solo import Solo
from game.game import Game

ecran = Screen()

# Initialisation des options pour configurer le jeu
args = commandes.parser.parse_args()
mode = args.command

if mode is not None:
    resolution = commandes.setResolution(args.resolution)
    level = args.level
    ecran = Screen()

    # Initialisation de
    # l'objet Jeu de classe Game
    if mode == "ia":
        fps = commandes.setFPS(args.fps)
        type = commandes.setType(args.type)
        ecran.game_IA = IA(resolution=resolution, level=level, fps=fps, type=type)

        if args.genomeload is not None:
            ecran.game_IA.load_genome(args.genomeload)

        elif args.populationload is not None:
            ecran.game_IA.load_checkpoint(args.populationload)

        else:
            basic_movements = args.movements
            ecran.game_IA.movements.set_basic_movements(basic_movements)
            ecran.game_IA.play()

    if mode == "solo":
        if args.keyboard == "all":
            ecran.options_controls(onStart="all")
        ecran.game_solo = Solo(resolution=resolution, level=level)
        ecran.game_solo.play()
    
    if mode == "show":
        if args.step:
            type = commandes.setType(args.type)
            jeu = IA(resolution=resolution, level=level, fps=True, type=type)
            file = commandes.get_file_step(level, type)
            if file is not None:
                jeu.load_genome(file)
        else:
            jeu = Game(resolution=resolution, level=level, fps=True)
            jeu.show(movement=bool(args.movement))

else:
    ecran.main_menu()

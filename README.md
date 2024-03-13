v1 du README.md  

IA Super Mario Bros
=

Création d'une IA qui apprend à jouer d'elle-même à Super Mario Bros


## Installation des modules

``` bash
pip install -r requirements.txt
```

## Lancer le programme
Lancer le programme sans commande, lance l'interface graphique

``` bash
python main.py
```
## Paramètres et arguments :

- "**--resolution**" ou "**-r**" permet de choisir la résolution dans le terminal, si "**x, y**" est en argument, la resolution est (x,y)
- "**--fps**" ou "**-f** "pour choisir si les FPS sont limités ou non (Unlimited, par défaut | 60)
- "**--level**" ou "**-lv**" pour choisir le niveau à lancer dans le jeu "<world, 1 par défaut>-<level, 1 par défaut>" (Exemple: 1-1)


### ia :

- "**--type**" ou "**-t**" pour choisir l'objectif que l'IA aura d'accomplir (speed par défaut | coins | score | nostop)
- "**--genomeload**" ou "**-gload**" Charger une IA qui est sauvegardée en renseignant le nom du fichier (les sauvegardes sont dans game/best_ia/)
- "**--populationload**" ou "**-pload**" Recharger une IA pour continuer à l'entrainer en renseignant le nom du fichier (les sauvegardes sont dans game/neat-checkpoint/),
les fichiers .save.pkl sont des sauvegardes du meilleur génome d'une IA non fini, tandis que les .pkl sont des sauvegardes d'une IA fini 
- "**--movements**" ou "**-m**" Choisit les mouvements utilisés par l'IA parmi : left, right, up, down, A, B (par défaut : left, right, up, down, A, B)


### solo :

- "**--keyboard**" ou "**-k**" pour configurer les touches au lancement du programme

### show :

- "**--step**" Liste tous les génomes enregistrés au cours de l'entrainement et permet de choisir celui à afficher
- "**--movement**" Mario utilise les différents contrôles du jeu

## Sources 
### Ressources
- http://pom.tls.cena.fr/GA/FAG/ag.html
- https://gym.openai.com/
- https://pypi.org/project/gym-super-mario-bros/
- https://pypi.org/project/nes-py/
- https://github.com/healthpotionstudios/MarioWorldAI-NEAT
- https://github.com/Chrispresso/SuperMarioBros-AI
- https://github.com/vivek3141/super-mario-neat
- https://github.com/szmyty/OpenAI-Retro-SuperMarioWorld-SNES
- https://cx-freeze.readthedocs.io/en/latest/
- https://www.mariowiki.com/


### Annexes
- https://www.youtube.com/watch?v=2eeYqJ0uBKE
- https://www.youtube.com/watch?v=qv6UVOQ0F44
- https://ledatascientist.com/algorithme-genetique/
- https://fr.wikipedia.org/wiki/R%C3%A9seau_de_neurones_artificiels
- https://fr.wikipedia.org/wiki/Algorithme_g%C3%A9n%C3%A9tique

### Assets
- https://www.fontspace.com/super-plumber-brothers-font-f9287
- https://virtualbackgrounds.site/background/super-mario-bros-level-ending/
- https://u-paris.fr/charte-graphique-et-outils/
- https://github.com/baraltech/Menu-System-PyGame/blob/main/button.py
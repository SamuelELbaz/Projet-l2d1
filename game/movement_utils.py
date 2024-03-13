import itertools


class Movements:
    """
    La classe Movements permet de manipuler les mouvements utilisés sur Super Mario Bros
    """
    def __init__(self, basic_movements: list):
        """
        @param basic_movements: ['left', 'right', 'up', 'down', 'A', 'B']
        """
        self.basic_movements = basic_movements
        self.all_movements = self.create_all_movements()

    def create_all_movements(self) -> [[str]]:  # utile pour les deux
        """
        Renvoie une liste des combinaisons de touche à partir des mouvements de base
        @return all_movements: Liste des combinaisons de mouvements
        """
        # Liste des combinaisons de commandes de Mario
        all_movements = [['NOOP']]
        for i in range(1, len(self.basic_movements) + 1):
            for combo in itertools.combinations(self.basic_movements, i):
                all_movements.append(list(combo))

        return all_movements

    @staticmethod
    def translate_key_to_action(key: str) -> str:
        """
        Traduit une clé en son mouvement dans la liste des actions de gym super mario bros
        @param key:
        @return:
        """
        key_action = {"Haut": "up",
                      "Bas": "down",
                      "Gauche": "left",
                      "Droite": "right",
                      "A": "A",
                      "B": "B"}

        return key_action[key]

    def translate_movement_user(self, action) -> int:
        """
        Traduit un mouvement en un indice qui peut être utilisé dans env.step() de gym
        par rapport aux mouvements de l'environnement disponible
        @param action: liste des actions à faire
        @return indice: int pouvant être utilisé dans env.step()
        """

        # Si on appuie sur la touche droite ou gauche il faut quelle soit en premier dans la liste
        if "right" in action and action[0] != "right":
            while "right" in action:
                action.remove("right")
            action.insert(0, "right")

        if "left" in action and action[0] != "left":
            while "left" in action:
                action.remove("left")
            action.insert(0, "left")

        # Si on appuie sur la touche de course il faut quelle soit en dernier dans la liste
        if "B" in action and action[-1] != "B":
            while "B" in action:
                action.remove("B")
            action.append("B")

        if "up" in action:
            action = ["up"]

        if "down" in action:
            action = ["down"]

        # Si aucun bouton pressé alors Mario ne fait rien
        if len(action) == 0 or ["down", "up"] in action:
            action = ["NOOP"]

        # Trouver à quelle action correspond les touches pressées
        '''for i in range(len(movements)):
            if movements[i] == action:
                action = i
        '''
        action = self.translate_movement(action)
        return action

    def translate_outputs(self, output: [float]) -> [str]:
        """
        Traduit l'output de l'IA en indice comprehensible par le module gym
        @param output: liste de float
        @return: un indice entre 0 et la taille de all_movements
        """
        action = []
        for i in range(len(output)):
            if output[i] == 1.0:
                action.append(self.basic_movements[i])
        action = self.translate_movement(action)
        return action

    def translate_movement(self, action: [str]) -> int:
        """
        Traduit un mouvement en un indice qui peut être utilisé dans env.step() de gym
        par rapport aux mouvements de l'environnement disponible
        @param action: liste de mouvements
        @return: un indice entre 0 et la taille de all_movements
        """
        # Si aucun bouton pressé alors Mario ne fait rien
        if len(action) == 0:
            action = ["NOOP"]

        # Trouver à quelle action correspond les touches pressées
        for i in range(len(self.all_movements)):
            if self.all_movements[i] == action:
                action = i

        return action

    def translate_str_to_movements(self, action: str) -> None:
        """
        Set action sous la forme basic_movements et redéfinit all_basic_movements
        @param action: lettre en minuscule de chaque mouvement utilisé
        """
        self.basic_movements = []
        for c in action:
            if c == "r":
                self.basic_movements.append("right")
            elif c == "l":
                self.basic_movements.append("left")
            elif c == "u":
                self.basic_movements.append("up")
            elif c == "d":
                self.basic_movements.append("down")
            elif c == "a":
                self.basic_movements.append("A")
            elif c == "b":
                self.basic_movements.append("B")
        self.all_movements = self.create_all_movements()

    def translate_movements_to_str(self) -> str:
        """
        Traduit basic_movements en str
        @return: str des mouvements avec chaque mouvement traduit en sa 1ère lettre en minuscule
        """
        s = ""
        print(self.basic_movements)
        for a in self.basic_movements:
            s += a[0].lower()
        return s

    def has_movement(self, move: str):
        """
        @param move: un mouvement
        @return: si le mouvement est dans basic_movements return move sinon return None
        """
        return f"'{move}'" if move in self.basic_movements else None

    def add_movement(self, move: str) -> None:
        """
        Ajoute un mouvement dans basic_movements et redéfinit all_movements
        @param move: un mouvement
        """
        if self.has_movement(move):
            self.basic_movements.remove(move)
        else:
            self.basic_movements.append(move)
        self.basic_movements = self.organize_movements(self.basic_movements)
        self.all_movements = self.create_all_movements()

    @staticmethod
    def organize_movements(action: list) -> list:
        """
        Organise action pour être de la meme forme que basic_movements
        @param action: liste de mouvements
        @return: liste de mouvements
        """
        # Si on appuie sur la touche droite ou gauche il faut quelle soit en premier dans la liste
        if "right" in action and action[0] != "right":
            while "right" in action:
                action.remove("right")
            action.insert(0, "right")

        if "left" in action and action[0] != "left":
            while "left" in action:
                action.remove("left")
            action.insert(0, "left")

        if "A" in action and action[-1] != "A":
            while "A" in action:
                action.remove("A")
            action.append("A")

        # Si on appuie sur la touche de course il faut quelle soit en dernier dans la liste
        if "B" in action and action[-1] != "B":
            while "B" in action:
                action.remove("B")
            action.append("B")

        return action

    def set_basic_movements(self, basic_movements):
        self.basic_movements = basic_movements
        self.all_movements = self.create_all_movements()

    def get_basic_movements(self):
        return self.basic_movements

    def get_all_movements(self):
        return self.all_movements

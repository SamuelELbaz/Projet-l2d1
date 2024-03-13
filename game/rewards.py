
class Rewards:
    """
    Les informations utilisées pour récompenser l'IA
    """
    def __init__(self, type: str, level: str):
        """
        @param type: le type de l'IA (speed, coins, score, nostop)
        @param level: niveau du jeu [1~8-1~4]
        """
        self.type = type
        self.level = level
        # enregistrement d'informations pour le système de récompenses
        self.info_rewards = {}
        # le nombre total de pièces pour chaque niveau
        self.nb_coins = {
            '1-1': 39, '1-2': 68, '1-3': 23, '1-4': 6,
            '2-1': 89, '2-2': 28, '2-3': 35, '2-4': 6,
            '3-1': 80, '3-2': 62, '3-3': 22, '3-4': 5,
            '4-1': 62, '4-2': 45, '4-3': 27, '4-4': 0,
            '5-1': 20, '5-2': 87, '5-3': 23, '5-4': 6,
            '6-1': 31, '6-2': 103, '6-3': 24, '6-4': 6,
            '7-1': 33, '7-2': 28, '7-3': 35, '7-4': 0,
            '8-1': 53, '8-2': 34, '8-3': 10, '8-4': 1
        }

    def set_type(self, type: str) -> None:
        self.type = type

    def set_level(self, level: str) -> None:
        self.level = level

    def set_rewards(self) -> None:
        """
        Set les rewards en fonction du type
        """
        self.info_rewards['x_pos_previous'] = 0
        self.info_rewards['counter'] = 0
        self.info_rewards['fitness_current'] = 0

        if self.type == 'speed':
            self.info_rewards['y_pos_previous'] = 0

        # TODO: s'occuper des rewards -> reward pour des vies bonus, upgrade
        elif self.type == 'coins':
            self.info_rewards['coins'] = 0

        elif self.type == 'score':
            self.info_rewards['score'] = 0

    def calcul_rewards(self, info: {}, done: bool) -> bool:
        """
        Calcule la fitness de Mario en fonction du type d'IA choisi
        :param info: info actuel du jeu Mario
        :param done: état actuel du jeu Mario
        :return:  nouvel état du jeu Mario
        """
        # Récompense mario pour sa rapidite
        if self.type == 'speed':
            done = self.calcul_rewards_speed(info, done)

        if self.type == 'coins':
            done = self.calcul_rewards_coins(info, done)

        if self.type == 'score':
            done = self.calcul_rewards_score(info, done)

        if self.type == 'nostop':
            done = self.calcul_rewards_nostop(info, done)

        return done

    def calcul_rewards_speed(self, info: {}, done: bool) -> bool:
        """
        Calcule la fitness d'une IA de type speed, notamment en récompensant les sauts
        :param info: info actuel du jeu Mario
        :param done: état actuel du jeu Mario
        :return:  nouvel état du jeu Mario
        """
        x_pos = info['x_pos']
        y_pos = info['y_pos']
        flag_get = info['flag_get']

        reward_up_y = 3
        self.reward_y(y_pos, reward_up_y)

        reward_forward = (x_pos / 100)
        reset_counter_x_forward = True
        self.reward_x_forward(x_pos, reward_forward, reset_counter_x_forward)

        punish_back = 0.1
        inc_counter_back = 1
        self.punish_x_back(x_pos, punish_back, inc_counter_back)

        punish_static = 0.1
        inc_counter_static = 1
        self.punish_x_static(x_pos, punish_static, inc_counter_static)

        value_counter = 500
        value_punish_counter = 50
        done = self.punish_counter(value_counter, value_punish_counter, done)

        value_death = 100
        done = self.punish_death(value_death, done)

        value_finish = 1000000
        done = self.reward_flag(flag_get, value_finish, done)

        return done

    def calcul_rewards_nostop(self, info: {}, done: bool) -> bool:
        """
        Calcule la fitness d'une IA de type nostop, notamment en arretant chaque partie si mario n'avance pas
        @param info: info actuel du jeu Mario
        @param done: état actuel du jeu Mario
        @return: nouvel état du jeu Mario
        """
        x_pos = info['x_pos']
        flag_get = info['flag_get']

        reward_forward = (x_pos / 100)
        reset_counter_x_forward = True
        self.reward_x_forward(x_pos, reward_forward, reset_counter_x_forward)

        punish_back = 1
        inc_counter_back = 1
        self.punish_x_back(x_pos, punish_back, inc_counter_back)

        punish_static = 1
        inc_counter_static = 1
        self.punish_x_static(x_pos, punish_static, inc_counter_static)

        value_counter = 10
        value_punish_counter = 500
        done = self.punish_counter(value_counter, value_punish_counter, done)

        value_death = 100
        done = self.punish_death(value_death, done)

        value_finish = 1000000
        done = self.reward_flag(flag_get, value_finish, done)

        return done

    def calcul_rewards_coins(self, info:{}, done: bool) -> bool:
        """
        Calcule la fitness d'une IA de type coins, notamment en récompensant la prise de pièces
        @param info: info actuel du jeu Mario
        @param done: état actuel du jeu Mario
        @return: nouvel état du jeu Mario
        """
        coins = info['coins']
        x_pos = info['x_pos']
        flag_get = info['flag_get']

        value_coins = (1000000/(self.nb_coins[self.level]+1))
        value_coins = int(value_coins)+1
        self.reward_coins(coins, value_coins)

        reward_forward = (x_pos / 200)
        reset_counter_x_forward = True
        self.reward_x_forward(x_pos, reward_forward, reset_counter_x_forward)

        punish_back = 0.1
        inc_counter_back = 1
        self.punish_x_back(x_pos, punish_back, inc_counter_back)

        punish_static = 0.1
        inc_counter_static = 1
        self.punish_x_static(x_pos, punish_static, inc_counter_static)

        value_counter = 500
        value_punish_counter = 50
        done = self.punish_counter(value_counter, value_punish_counter, done)

        value_death = 100
        done = self.punish_death(value_death, done)

        value_finish = 1000000
        done = self.reward_flag(flag_get, value_finish, done)
        return done

    def calcul_rewards_score(self, info: {}, done: bool) -> bool:
        score = info['score']
        x_pos = info['x_pos']
        flag_get = info['flag_get']

        reward_score = 500
        self.reward_score(score, reward_score)

        reward_forward = (x_pos / 400)
        reset_counter_x_forward = True
        self.reward_x_forward(x_pos, reward_forward, reset_counter_x_forward)

        punish_back = 0
        inc_counter_back = 1
        self.punish_x_back(x_pos, punish_back, inc_counter_back)

        punish_static = 0.1
        inc_counter_static = 1
        self.punish_x_static(x_pos, punish_static, inc_counter_static)

        value_counter = 750
        value_punish_counter = 50
        done = self.punish_counter(value_counter, value_punish_counter, done)

        value_death = 100
        done = self.punish_death(value_death, done)

        value_finish = 1000000
        done = self.reward_flag(flag_get, value_finish, done)

        return done

    def reward_x_forward(self, x_pos: int, reward_forward: float, reset_counter: bool) -> None:
        """
        Récompense l'IA lorsque Mario avance
        @param x_pos: position x de Mario
        @param reward_forward: recompense pour avancer
        @param reset_counter: si Vrai on reset le counter sinon on ne fait rien
        """
        # Recompense mario pour aller à droite
        if x_pos > self.info_rewards['x_pos_previous']:
            self.info_rewards['fitness_current'] += reward_forward
            self.info_rewards['x_pos_previous'] = x_pos
            if reset_counter:
                self.info_rewards['counter'] = 0

    def reward_y(self, y_pos, reward_up) -> None:
        """
        Récompense l'iA lorsque la position y de Mario est plus élevée que précédemment
        @param y_pos: position y de Mario
        @param reward_up: récompense de hauteur
        """
        if y_pos > self.info_rewards['y_pos_previous']:
            self.info_rewards['fitness_current'] += reward_up
            self.info_rewards['y_pos_previous'] = y_pos

        elif y_pos < self.info_rewards['y_pos_previous']:
            self.info_rewards['y_pos_previous'] = y_pos

    def reward_coins(self, coins, value_reward) -> None:
        """
        Récompense l'IA lorsque Mario récupère une pièce
        @param coins: nombre de pièces récupérées
        @param value_reward: valeur de la récompense pour récupérer une pièce
        """
        if coins > self.info_rewards['coins']:
            self.info_rewards['fitness_current'] += value_reward
            self.info_rewards['coins'] = coins

    def reward_score(self, score, value_reward) -> None:
        """
        Recompense l'IA lorsque Mario augmente son score
        @param score: le score actuel de Mario
        @param value_reward:  valeur de la recompense pour une augmentation du score de 100
        """
        if score > self.info_rewards['score'] :
            diff_score = (score - self.info_rewards['score']) / 100
            self.info_rewards['fitness_current'] += diff_score * value_reward
            self.info_rewards['score'] = score

    def reward_flag(self, flag_get, reward_get, done):
        """
        Récompense l'IA si Mario finit le niveau et met fin à cette partie
        @param flag_get: Vrai si Mario a fini le niveau, Faux sinon
        @param reward_get: valeur de la récompense si Mario finit le niveau
        @param done: état actuel du jeu
        @return: nouvel état du jeu
        """
        # si mario touche le drapeau, gagner
        if flag_get == 1:
            self.info_rewards['fitness_current'] += reward_get
            done = True
        return done

    def punish_x_back(self, x_pos: int, punish_back: float, inc_counter: float or None) -> None:
        """
        Punit l'IA lorsque Mario recule
        @param x_pos: position x de Mario
        @param punish_back: punition pour aller en arrière
        @param inc_counter: si est un int augmente la valeur de counter sinon ne fais rien
        """
        if x_pos < self.info_rewards['x_pos_previous']:
            if inc_counter is not None:
                self.info_rewards['counter'] += inc_counter
            self.info_rewards['fitness_current'] -= punish_back

    def punish_x_static(self, x_pos: int, punish_static: float, inc_counter: float or None) -> None:
        """
        Punit l'IA lorsque Mario ne bouge pas
        @param x_pos: position x de Mario
        @param punish_static: punition pour ne pas bouger
        @param inc_counter: si est un int augmente la valeur de counter sinon ne fais rien
        """
        if x_pos == self.info_rewards['x_pos_previous']:
            if inc_counter is not None:
                self.info_rewards['counter'] += inc_counter
            self.info_rewards['fitness_current'] -= punish_static

    def punish_counter(self, value_counter: int, value_punish: float, done: bool) -> bool:
        """
        Punit l'IA lorque counter atteint value_counter cela à pour effet de mettre fin à la partie
        @param value_counter: valeur à laquelle le jeu s'arrête
        @param value_punish: valeur de la punition lorsque value_counter est atteint
        @param done: état actuel du jeu
        @return: nouvel état du jeu
        """
        # Si mario reste sans bouger ou a ete trop longtemps a gauche, le penalise et met fin a cet individu
        if self.info_rewards['counter'] == value_counter:
            self.info_rewards['fitness_current'] -= value_punish
            done = True
        return done

    def punish_death(self, value_death: float, done: bool) -> bool:
        """
        Punit l'IA si Mario meurt (tué par un monstre ou tombe dans le vide) et met fin à la partie
        @param value_death: valeur de punition en cas de mort
        @param done: état actuel du jeu
        @return: nouvel état du jeu
        """
        # fin de l'individu si mario meurt et le penalise
        if done :
            self.info_rewards['fitness_current'] -= value_death

        return done

    def get_info(self):
        return self.info_rewards

    def get_type(self):
        return self.type

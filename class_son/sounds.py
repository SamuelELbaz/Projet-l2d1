import pygame

# class qui importe les sons
class Sounds:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            
            'Start' : pygame.mixer.Sound("class_son/sounds/Start.ogg"),
            'click' : pygame.mixer.Sound("class_son/sounds/click.ogg"),
        }
        
    #fonction qui permet de jouer le son souhaiter
    def playsong(self,name):
        sound = self.sounds[name].play()
        sound.set_volume(0.1)
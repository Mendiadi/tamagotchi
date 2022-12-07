import functools
import pygame


pygame.mixer.init()




def load_images():
    _images_collection = {}
    _images_collection["bg"] = pygame.image.load("bg.png").convert()
    _images_collection["drink"] = pygame.image.load("drink.png").convert()
    _images_collection["food"] = pygame.image.load("food.png").convert()

    return _images_collection


class Sounds:
    def __init__(self):
        self._sounds_collection = {}

    def load_sounds(self):
        self._sounds_collection["button"] = pygame.mixer.Sound("button_sound_1.mp3")


    def button(self,func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            self._sounds_collection['button'].play()
            return func(*args,**kwargs)
        return inner

sound = Sounds()

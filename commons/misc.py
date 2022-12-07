import functools
import pygame


pygame.mixer.init()




def load_images():
    _images_collection = {}
    _images_collection["bg"] = pygame.image.load("assets/images/bg.png").convert()
    _images_collection["drink"] = pygame.image.load("assets/images/drink.png").convert()
    _images_collection["food"] = pygame.image.load("assets/images/food.png").convert()
    _images_collection['shop'] = pygame.image.load("assets/images/shop.jpg").convert()
    return _images_collection


class Sounds:
    def __init__(self):
        self._sounds_collection = {}


    def load_sounds(self):
        self._sounds_collection["button"] = pygame.mixer.Sound("assets/sounds/button_sound_1.mp3")



    def music(self,play=False):
        pygame.mixer.music.load("assets/sounds/music_bg.mp3")
        pygame.mixer.music.set_volume(0.2)
        if play:
            pygame.mixer.music.play(10)
        else:
            pygame.mixer.music.pause()

    def button(self,func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            self._sounds_collection['button'].play()
            return func(*args,**kwargs)
        return inner

sound = Sounds()
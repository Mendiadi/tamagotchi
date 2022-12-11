import functools
import pygame

pygame.mixer.init()


def load_images():
    _images_collection = {}
    _images_collection["bg"] = pygame.image.load("assets/images/bg.png").convert()
    _images_collection["drink"] = pygame.image.load("assets/images/drink.png").convert()
    _images_collection["food"] = pygame.image.load("assets/images/food.png").convert()
    _images_collection['shop'] = pygame.image.load("assets/images/shop.jpg").convert()
    _images_collection["shop_btn"] = pygame.image.load("assets/images/shop_btn.png").convert()
    _images_collection['medic'] = pygame.image.load("assets/images/medic.png").convert()
    return _images_collection


class Sounds:
    def __init__(self):
        self._sounds_collection = {}

    def load_sounds(self):
        self._sounds_collection["button"] = pygame.mixer.Sound("assets/sounds/button_sound_1.mp3")
        self._sounds_collection['eat'] = pygame.mixer.Sound("assets/sounds/eat.mp3")
        self._sounds_collection['buy'] = pygame.mixer.Sound("assets/sounds/buy.mp3")

    def music(self, play=False):
        pygame.mixer.music.load("assets/sounds/music_bg.mp3")
        pygame.mixer.music.set_volume(0.2)
        if play:
            pygame.mixer.music.play(25)
        else:
            pygame.mixer.music.pause()

    def buy(self):
        self._sounds_collection['buy'].play()

    def eat(self):
        self._sounds_collection['eat'].play()

    def button(self, func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            self._sounds_collection['button'].play()
            return func(*args, **kwargs)

        return inner


sound = Sounds()

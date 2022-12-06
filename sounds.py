import pygame
from decorator import decorator

pygame.mixer.init()

_sounds_collection = {}

def load_sounds():
    _sounds_collection["button"] = pygame.mixer.Sound("button_sound_1.mp3")

@decorator
def button(func,*args,**kwargs):
    _sounds_collection['button'].play()
    return func(*args,**kwargs)




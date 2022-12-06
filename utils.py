from enum import Enum
import pygame

class GameState(Enum):
    MAIN = 0
    MENU = 1

class RGBColors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PINK = (255, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    SKIN_COLOR = (160,160,160)


def print_text_to_screen(text, win, x=100, y=500, size=30,color=None):
    """
    this function just print text to the surface
    :param text: string to show
    :param win: surface
    :return:
    """
    if not color:
        color = (0,0,0)
    font = pygame.font.SysFont("arial", size)
    render = font.render(text, False, color)
    for i in range(10):
        win.blit(render, (x+(i*0.3), y+(i * 0.5) - i))

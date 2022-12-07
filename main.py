import pygame

import game



def main():
    pygame.init()
    tamagochi = game.Tamagotchi()
    win = pygame.display.set_mode((tamagochi.HEIGHT, tamagochi.WIDTH))
    tamagochi.load(win)
    tamagochi.mainloop()


if __name__ == '__main__':
    main()



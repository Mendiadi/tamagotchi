import time

import pygame
from PIL import Image

import animator
from character import Character
from button import Button
from utils import RGBColors

move_command = ["left", "right", "l_init", "r_init"]

s = (Character.Actions.FLIP,Character.Actions.MOVE,Character.Actions.INVERT,Character.Actions.INVERT)

HEIGHT, WIDTH = 800,800

def print_text_to_screen(text, win, x=100, y=500, size=30):
    """
    this function just print text to the surface
    :param text: string to show
    :param win: surface
    :return:
    """
    font = pygame.font.SysFont("arial", size)
    render = font.render(text, False, (0, 0, 0))
    win.blit(render, (x, y))

class Tamagotchi:

    def __init__(self, character_):
        self.character = character_
        self.animate = animator.Animator(self.character.skeleton)

        self.btn_flip = Button((10, 10), RGBColors.SKIN_COLOR, "flip",font_color=RGBColors.BLACK)
        self.btn_dead = Button((200, 10), RGBColors.SKIN_COLOR, "dead",font_color=RGBColors.BLACK)

        self.btn_flip.set_onclick_function(self.make_flip)
        self.btn_dead.set_onclick_function(self.dead)
        self.btn_turnaround = Button((400, 10), RGBColors.SKIN_COLOR, "turn",font_color=RGBColors.BLACK)
        self.btn_turnaround.set_onclick_function(self.turnaround)
        self.btn_move_legs =  Button((600, 10), RGBColors.SKIN_COLOR, "legs",font_color=RGBColors.BLACK)
        self.btn_move_legs.set_onclick_function(self.move_legs)
        self.grow_up_btn = Button((700,10),RGBColors.SKIN_COLOR,"grow",font_color=RGBColors.BLACK)
        self.grow_up_btn.set_onclick_function(  self.character.grow_up)

    def move_legs(self):
        self.animate.execute(self.character.Actions.MOVE,move_command)

    def make_flip(self):
        self.animate.compile(self.character.skeleton)
        self.animate.execute(self.character.Actions.FLIP)

    def load_bg(self,win):
        image = pygame.image.load("Template.png")

        win.blit(image.convert(),(0,0))

    def show_stats(self,win):
        print_text_to_screen(f"Lives: {self.character.life_bar}%",
                             win,100,600)
        print_text_to_screen(f"Food: {self.character.food_bar}%",
                             win, 300, 600)
        print_text_to_screen(f"Happy: {self.character.happy}%",
                             win, 500, 600)
        print_text_to_screen(f"EVOLUTION RATE: {int(self.character.evolution)}%",
                             win, 250, 680)


    def dead(self):
        self.animate.compile(self.character.skeleton)
        self.animate.execute(self.character.Actions.DEAD)

    def turnaround(self):
        self.animate.compile(self.character.skeleton)
        self.animate.execute(self.character.Actions.INVERT)

    def idle(self):
        self.animate.compile(self.character.skeleton)


    def render(self, win):
        win.fill("white")
        self.load_bg(win)
        self.animate.render(win,size=self.character.age,
                            pad=self.character.age//2,
                            angel=self.character.age/self.character.angel)
        self.btn_flip.draw(win)
        self.btn_dead.draw(win)
        self.btn_move_legs.draw(win)
        self.btn_turnaround.draw(win)
        self.grow_up_btn.draw(win)
        self.show_stats(win)

        pygame.display.flip()

    def update(self, dt,ev):
        self.btn_dead.update(ev)
        self.btn_flip.update(ev)
        self.btn_turnaround.update(ev)
        self.btn_move_legs.update(ev)
        self.grow_up_btn.update(ev)
        self.animate(rate=12 / dt)
        if not self.animate._active and not self.animate._inverted:
            self.idle()




def main():
    pygame.init()
    fps = 60
    win = pygame.display.set_mode((HEIGHT, WIDTH))
    character = Character()
    game = Tamagotchi(character)
    run = True
    clock = pygame.time.Clock()
    dt = fps
    while run:
        pygame.display.set_caption(f"FPS {int(clock.get_fps())}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            game.update(dt,event)
            # if event.type == pygame.MOUSEMOTION:
            #     print(pygame.mouse.get_pos())
        game.render(win)
        dt = clock.tick(fps)

    pygame.quit()

main()


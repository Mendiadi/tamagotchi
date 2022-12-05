import time

import pygame
import animator
from character import Character
from button import Button, RGBColors

move_command = ["left", "right", "l_init", "r_init"]

s = (Character.Actions.FLIP,Character.Actions.MOVE,Character.Actions.INVERT,Character.Actions.INVERT)


class Tamagotchi:

    def __init__(self, character_):
        self.character = character_
        self.animate = animator.Animator(self.character.skeleton)

        self.btn_flip = Button((10, 10), RGBColors.BLACK, "flip")
        self.btn_dead = Button((200, 10), RGBColors.BLACK, "dead")
        self.btn_flip.set_onclick_function(self.make_flip)
        self.btn_dead.set_onclick_function(self.dead)
        self.btn_turnaround = Button((400, 10), RGBColors.BLACK, "turn")
        self.btn_turnaround.set_onclick_function(self.turnaround)
        self.btn_move_legs =  Button((600, 10), RGBColors.BLACK, "legs")
        self.btn_move_legs.set_onclick_function(self.move_legs)
        self.grow_up_btn = Button((700,10),RGBColors.BLACK,"grow")
        self.grow_up_btn.set_onclick_function(  self.character.grow_up)

    def move_legs(self):
        self.animate.compile(self.character.skeleton)
        self.animate.execute(self.character.Actions.MOVE,move_command)

    def make_flip(self):
        self.animate.compile(self.character.skeleton)
        self.animate.execute(self.character.Actions.FLIP)



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
        self.animate.render(win,size=self.character.age,
                            pad=self.character.age//2,
                            angel=self.character.age/self.character.angel)
        self.btn_flip.draw(win)
        self.btn_dead.draw(win)
        self.btn_move_legs.draw(win)
        self.btn_turnaround.draw(win)
        self.grow_up_btn.draw(win)
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
    win = pygame.display.set_mode((800, 800))
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
        game.render(win)
        dt = clock.tick(fps)

    pygame.quit()

main()


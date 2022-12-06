import abc
import pygame

from utils import RGBColors, print_text_to_screen
from button import Button


class Screen(abc.ABC):
    def __init__(self, win):
        self.win = win

    @abc.abstractmethod
    def render(self):
        ...

    @abc.abstractmethod
    def update(self, delta_t, event):
        ...


class MainGame(Screen):
    """
    class for manage and render the main game screen
    """

    def __init__(self, win, tamagochi):
        super().__init__(win)
        # init content
        self.game = tamagochi
        self.background = pygame.image.load("Template.png")

        # init buttons
        self.btn_flip = Button((10, 10), RGBColors.SKIN_COLOR, "flip", font_color=RGBColors.BLACK)
        self.btn_dead = Button((200, 10), RGBColors.SKIN_COLOR, "dead", font_color=RGBColors.BLACK)
        self.btn_animation = Button((550, 10), RGBColors.SKIN_COLOR, "animation", font_color=RGBColors.BLACK)
        self.grow_up_btn = Button((700, 10), RGBColors.SKIN_COLOR, "grow", font_color=RGBColors.BLACK)
        # set onclick methods
        self.grow_up_btn.set_onclick_function(self.game.character.grow_up)
        self.btn_flip.set_onclick_function(self.make_flip)
        self.btn_dead.set_onclick_function(self.dead)
        self.btn_animation.set_onclick_function(self.animation1)
        self.buttons = (self.btn_flip, self.btn_dead, self.grow_up_btn, self.btn_animation)

    def show_stats(self, win):
        print_text_to_screen(f"Lives: {self.game.character.life_bar}%",
                             win, 100, 600)
        print_text_to_screen(f"Food: {self.game.character.food_bar}%",
                             win, 300, 600)
        print_text_to_screen(f"Happy: {self.game.character.happy}%",
                             win, 500, 600)
        print_text_to_screen(f"EVOLUTION RATE: {int(self.game.character.evolution)}%",
                             win, 250, 680)
        if self.game.is_paused:
            print_text_to_screen("PAUSED (ESC) to cancel",
                                 self.win, 150, 200, 30, RGBColors.WHITE.value)

    def render(self):
        self.win.fill(RGBColors.WHITE.value)
        self.win.blit(self.background.convert(), (0, 0))
        for button in self.buttons:
            button.draw(self.win)
        self.game.animate.render(self.win, size=self.game.character.age,
                            pad=self.game.character.age // 2,
                            angel=self.game.character.angel)
        self.show_stats(self.win)
        pygame.display.flip()

    def update(self, delta_t, event):
        if self.game.is_paused:
            return
        for button in self.buttons:
            button.update(event)
        self.game.animate(rate=7 / delta_t)
        if not self.game.animate._active and not self.game.animate._inverted:
            self.idle()

    def animation1(self):
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.ANIMATION1)

    def make_flip(self):
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.FLIP)

    def dead(self):
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.DEAD)

    def idle(self):
        self.game.animate.compile(self.game.character.skeleton)


class MainMenu(Screen):
    """class for manage the main menu screen"""
    ...


class SplashScreen(Screen):
    """
    perform the splash screen
    """
    ...

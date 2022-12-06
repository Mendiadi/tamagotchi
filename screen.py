import abc
import threading

import pygame

from utils import RGBColors, print_text_to_screen, GameState
from button import Button


class Screen(abc.ABC):
    """Abstract screen class"""
    def __init__(self, win, tamagochi):
        self.win = win
        self.game = tamagochi

    @abc.abstractmethod
    def render(self):
        """
        virtual pure func rendering all the entities to the screen
        """
        ...

    @abc.abstractmethod
    def _on_leave(self):
        """virtual pure describe action for leaving screen"""
        ...

    @abc.abstractmethod
    def update(self, delta_t, event):
        """virtual pure func Updating all the data of the game"""
        ...


class MainGame(Screen):
    """
    class for manage and render the main game screen
    """

    def __init__(self, win, tamagochi):
        super().__init__(win,tamagochi)

        # init bg
        self.background = pygame.image.load("Template.png")

        # init buttons
        self.btn_flip = Button((10, 10), RGBColors.SKIN_COLOR, "flip", font_color=RGBColors.BLACK)
        self.btn_sleep = Button((200, 10), RGBColors.SKIN_COLOR, "sleep", font_color=RGBColors.BLACK)
        self.btn_animation = Button((550, 10), RGBColors.SKIN_COLOR, "animation", font_color=RGBColors.BLACK)
        self.grow_up_btn = Button((700, 10), RGBColors.SKIN_COLOR, "grow", font_color=RGBColors.BLACK)
        self.back_btn = Button((400, 10), RGBColors.SKIN_COLOR, "back", font_color=RGBColors.BLACK)
        # set onclick methods
        self.back_btn.set_onclick_function(self._on_leave)
        self.grow_up_btn.set_onclick_function(self.game.character.grow_up)
        self.btn_flip.set_onclick_function(self.make_flip)
        self.btn_sleep.set_onclick_function(self.sleep)
        self.btn_animation.set_onclick_function(self.animation1)
        self.buttons = (self.btn_flip, self.btn_sleep, self.grow_up_btn, self.btn_animation, self.back_btn)

    def show_stats(self):
        """
        Rendering the stats and texts to the target
        """
        print_text_to_screen(f"Lives: {self.game.character.life_bar}%",
                             self.win, 100, 600)
        print_text_to_screen(f"Food: {self.game.character.food_bar}%",
                             self.win, 300, 600)
        print_text_to_screen(f"Happy: {self.game.character.happy}%",
                             self.win, 500, 600)
        print_text_to_screen(f"EVOLUTION RATE: {int(self.game.character.evolution)}%",
                             self.win, 250, 680)
        if self.game.is_paused:
            print_text_to_screen("PAUSED (ESC) to cancel",
                                 self.win, 150, 200, 30, RGBColors.WHITE.value)

    def render(self):
        """
        main rendering point handle all the entities
        texts objects that need to be rendered
        """
        self.win.fill(RGBColors.WHITE.value)
        self.win.blit(self.background.convert(), (0, 0))
        for button in self.buttons:
            button.draw(self.win)
        self.game.animate.render(self.win, size=self.game.character.age,
                            pad=self.game.character.age // 2,
                            angel=self.game.character.angel)
        self.show_stats()
        pygame.display.flip()

    def _on_leave(self):
        # todo  saves records
        self.game.update_state(GameState.MENU)

    def update(self, delta_t, event):
        """
        update the game attributes and the entities
        by the delta time or event
        :param delta_t: delta time is speed of updating
        :param event: pygame event

        """
        if self.game.is_paused:
            return
        for button in self.buttons:
            button.update(event)
        self.game.animate(rate=7 / delta_t)
        if not self.game.animate._active and not self.game.animate._inverted:
            self.idle()

    def animation1(self):
        """
        perform animation 1

        """
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.ANIMATION1)

    def make_flip(self):
        """
        perform flip
        :return:
        """
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.FLIP)

    def sleep(self):
        """
        perform dead
        :return:
        """
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.SLEEP)

    def idle(self):
        """
        idle animation
        :return:
        """
        self.game.animate.compile(self.game.character.skeleton)


class MainMenu(Screen):
    """class for manage the main menu screen"""

    def __init__(self, win, tamagochi):
        super().__init__(win, tamagochi)
        self.start_btn = Button((100,500),RGBColors.BLACK,"START")
        self.start_btn.set_onclick_function(self._on_leave)
        self.buttons = (self.start_btn,)

    def _on_leave(self):
        # todo load saves
        self.game.start_game()
        self.game.update_state(GameState.MAIN)

    def render(self):
        self.win.fill(RGBColors.WHITE.value)
        for button in self.buttons:
            button.draw(self.win)
        print_text_to_screen("THIS IS MAIN MENU", self.win, 100, 100)
        pygame.display.flip()

    def update(self, delta_t, event):
        for button in self.buttons:
            button.update(event)


class SplashScreen(Screen):
    """
    perform the splash screen
    """

    def __init__(self, win, tamagochi):
        super().__init__(win, tamagochi)
        self.timer = threading.Timer(3,self._on_leave)
        self.timer.setDaemon(True)
        self.timer.name = "timer"
        self.timer.start()

    def _on_leave(self):
        self.game.update_state(GameState.MENU)
        self.timer.cancel()

    def render(self):
        self.win.fill(RGBColors.WHITE.value)
        print_text_to_screen("THIS IS SPLASH SCREEN",self.win,100,100)
        pygame.display.flip()

    def update(self, delta_t, event):...
import abc
import threading
import pygame

from utils import RGBColors, print_text_to_screen, GameState
from button import Button
from misc import load_images


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
        super().__init__(win, tamagochi)

        images = self.game.images
        # init bg
        self.background = images['bg']
        self.drink_image = images['drink']
        self.food_image = images['food']

        # init buttons
        self.button_food = Button((300, 535), image=self.food_image,
                                  width=self.food_image.get_width(), height=self.food_image.get_height(),
                                  txt=str(len(self.game.character.inventory['pizza'])), font_size=18
                                  )
        self.button_food.set_onclick_function(lambda: self.change_amount_food(self.button_food,
                                                                              self.game.shop['pizza']))
        self.drink_button = Button((350, 535), image=self.drink_image,
                                   width=self.drink_image.get_width(), height=self.drink_image.get_height(),
                                   txt=str(len(self.game.character.inventory['drink'])), font_size=18)
        self.drink_button.set_onclick_function(lambda: self.change_amount_food(self.drink_button,
                                                                               self.game.shop['drink']))
        self.btn_flip = Button((10, 10), RGBColors.SKIN_COLOR, "flip", font_color=RGBColors.BLACK)
        self.btn_sleep = Button((200, 10), RGBColors.SKIN_COLOR, "sleep", font_color=RGBColors.BLACK)
        self.btn_animation = Button((550, 10), RGBColors.SKIN_COLOR, "animation", font_color=RGBColors.BLACK)
        self.grow_up_btn = Button((700, 10), RGBColors.SKIN_COLOR, "grow", font_color=RGBColors.BLACK)
        self.back_btn = Button((400, 10), RGBColors.SKIN_COLOR, "back", font_color=RGBColors.BLACK)
        self.shop_btn = Button((300, 10), RGBColors.SKIN_COLOR, "shop", font_color=RGBColors.BLACK)
        # set onclick methods
        self.shop_btn.set_onclick_function(self._on_shop)
        self.back_btn.set_onclick_function(self._on_leave)
        self.grow_up_btn.set_onclick_function(self.game.character.grow_up)
        self.btn_flip.set_onclick_function(self.make_flip)
        self.btn_sleep.set_onclick_function(self.sleep)
        self.btn_animation.set_onclick_function(self.animation1)
        self.buttons = (self.btn_flip, self.btn_sleep, self.grow_up_btn,
                        self.btn_animation, self.back_btn, self.button_food, self.drink_button, self.shop_btn)

    def _on_shop(self):
        self.game.update_state(GameState.SHOP)

    def change_amount_food(self, btn, food):
        self.game.character.eat(food)
        btn.txt = str(len((self.game.character.inventory[food.name])))

    def show_stats(self):
        """
        Rendering the stats and texts to the target
        """

        print_text_to_screen(f"Lives: {self.game.character.life_bar}%",
                             self.win, 100, 600)
        print_text_to_screen(f"Food: {self.game.character.food_bar}%",
                             self.win, 300, 600)
        print_text_to_screen(f"ENERGY: {self.game.character.energy}%",
                             self.win, 300, 640)
        print_text_to_screen(f"Happy: {self.game.character.happy}%",
                             self.win, 500, 600)
        print_text_to_screen(f"EVOLUTION RATE: {int(self.game.character.level)}%",
                             self.win, 250, 680)
        print_text_to_screen(f"POINTS: {int(self.game.character.points)}",
                             self.win, 250, 720)
        if self.game.is_paused:
            print_text_to_screen("PAUSED (ESC) to cancel",
                                 self.win, 150, 200, 30, RGBColors.WHITE.value)

    def render(self):
        """
        main rendering point handle all the entities
        texts objects that need to be rendered
        """
        self.win.fill(RGBColors.WHITE.value)
        self.win.blit(self.background, (0, 0))
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
        if not self.game.character.set_flip():
            return
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.FLIP)

    def sleep(self):
        """
        perform dead
        :return:
        """
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.SLEEP)
        self.game.character.set_sleep()

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
        self.start_btn = Button((100, 500), RGBColors.BLACK, "START")
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
        self.timer = threading.Timer(3, self._on_leave)
        self.timer.setDaemon(True)
        self.timer.name = "timer"
        self.timer.start()

    def _on_leave(self):
        self.game.update_state(GameState.MENU)
        self.timer.cancel()

    def render(self):
        self.win.fill(RGBColors.WHITE.value)
        print_text_to_screen("THIS IS SPLASH SCREEN", self.win, 100, 100)
        pygame.display.flip()

    def update(self, delta_t, event): ...


class ShopScreen(Screen):
    def __init__(self, win, tamagochi):
        super().__init__(win, tamagochi)

        images = self.game.images
        # init bg
        self.background = images['shop']
        self.drink_image = images['drink']
        self.food_image = images['food']

        # init buttons
        self.button_food = Button((300, 180), image=self.food_image,
                                  width=self.food_image.get_width(), height=self.food_image.get_height())
        self.button_food.set_onclick_function(lambda: self.game.character.buy(self.game.shop['pizza']))
        self.drink_button = Button((400, 180), image=self.drink_image,
                                   width=self.drink_image.get_width(), height=self.drink_image.get_height())
        self.drink_button.set_onclick_function(lambda: self.game.character.buy(self.game.shop['drink']))

        self.back_btn = Button((400, 10), RGBColors.SKIN_COLOR, "back", font_color=RGBColors.BLACK)
        self.back_btn.set_onclick_function(self._on_leave)
        self.buttons = (self.drink_button, self.button_food, self.back_btn)

    def _on_leave(self):
        self.game.update_state(GameState.MAIN)

    def render(self):
        self.win.fill(RGBColors.BLACK.value)
        self.win.blit(self.background,(0,0))
        for btn in self.buttons:
            btn.draw(self.win)
        print_text_to_screen("SHOP", self.win, 100, 100,color=RGBColors.WHITE.value)
        print_text_to_screen(f"your points : {self.game.character.points}",
                             self.win, 300, 100,color=RGBColors.WHITE.value)
        print_text_to_screen(f"pizza price : {self.game.shop['pizza'].price}",
                             self.win, 270, 240,size=15,vertical=False,color=RGBColors.WHITE.value)
        print_text_to_screen(f"drink price : {self.game.shop['drink'].price}",
                             self.win, 400, 240,size=15,vertical=False,color=RGBColors.WHITE.value)
        pygame.display.flip()

    def update(self, delta_t, event):
        for btn in self.buttons:
            btn.update(event)

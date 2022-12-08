import pygame

from commons import misc
from .screen import Screen
from entities import Button
from commons.utils import (
    GameState,
    RGBColors,
    print_text_to_screen
)


class MainGame(Screen):
    """
    class for manage and render the main game screen
    """

    def __init__(self, win, tamagochi):
        super().__init__(win, tamagochi)

        images = self.game.images
        # init bg
        self.background = images['bg']




        # init buttons
        self.button_food = Button((300, 535), image=   images['food'],
                                  width=   images['food'].get_width(), height=   images['food'].get_height(),
                                  txt=str(len(self.game.character.inventory['pizza'])), font_size=18
                                  )
        self.button_food.set_onclick_function(lambda: self.change_amount_food(self.button_food,
                                                                              self.game.shop['pizza']))
        self.drink_button = Button((350, 535), image=  images['drink'],
                                   width=  images['drink'].get_width(), height=images['drink'].get_height(),
                                   txt=str(len(self.game.character.inventory['drink'])), font_size=18)
        self.drink_button.set_onclick_function(lambda: self.change_amount_food(self.drink_button,
                                                                               self.game.shop['drink']))
        self.btn_flip = Button((10, 10), RGBColors.SKIN_COLOR, "flip", font_color=RGBColors.BLACK)
        self.btn_sleep = Button((200, 10), RGBColors.SKIN_COLOR, "sleep", font_color=RGBColors.BLACK)
        self.btn_animation = Button((550, 10), RGBColors.SKIN_COLOR, "dance", font_color=RGBColors.BLACK)
        self.grow_up_btn = Button((700, 10), RGBColors.SKIN_COLOR, "grow", font_color=RGBColors.BLACK)
        self.back_btn = Button((400, 10), RGBColors.SKIN_COLOR, "back", font_color=RGBColors.BLACK)
        self.shop_btn = Button((300, 10), RGBColors.SKIN_COLOR, image=images['shop_btn'],
                               txt="shop",font_size=15)

        # set onclick methods

        self.shop_btn.set_onclick_function(self._on_shop)
        self.back_btn.set_onclick_function(self._on_leave)
        self.grow_up_btn.set_onclick_function(self.game.character.grow_up)
        self.btn_flip.set_onclick_function(self.make_flip)
        self.btn_sleep.set_onclick_function(self.sleep)
        self.btn_animation.set_onclick_function(self.dance)
        self.buttons = (self.btn_flip, self.btn_sleep, self.grow_up_btn,
                        self.btn_animation, self.back_btn, self.button_food,
                        self.drink_button, self.shop_btn)

        self._is_start = False

    @misc.sound.button
    def _on_shop(self):
        self.game.update_state(GameState.SHOP)

    def change_amount_food(self, btn, food):
        self.game.character.eat(food)
        btn.txt = str(len((self.game.character.inventory[food.name])))

    def show_stats(self):
        """
        Rendering the stats and texts to the target
        """

        print_text_to_screen(f"health: {self.game.character.life_bar}%",
                             self.win, 150, 200,color=RGBColors.GREEN.value,
                             vertical=False,size=16)
        print_text_to_screen(f"hanger: {self.game.character.food_bar}%",
                             self.win, 250, 200,color=RGBColors.GREEN.value,
                             vertical=False,size=16)
        print_text_to_screen(f"energy: {self.game.character.energy}%",
                             self.win, 350, 200,color=RGBColors.GREEN.value,
                             vertical=False,size=16)
        print_text_to_screen(f"happy: {self.game.character.happy}%",
                             self.win, 450, 200,color=RGBColors.GREEN.value,
                             vertical=False,size=16)
        print_text_to_screen(f"EVOLUTION RATE: {int(self.game.character.level)}%",
                             self.win, 300, 640)
        print_text_to_screen(f"Coins: {int(self.game.character.coins)}",
                             self.win, 500, 600)
        if self.game.is_paused:
            print_text_to_screen("PAUSED (ESC) to cancel",
                                 self.win, 150, 200, 30, RGBColors.WHITE.value)

    def render(self):
        """
        main rendering point handle all the entities
        texts objects that need to be rendered
        """

        if self.game.animate.birth:
            self.win.fill(RGBColors.WHITE.value)
            self.win.blit(self.background, (0, 0))
            for button in self.buttons:
                button.draw(self.win)
            self.game.animate.render(self.win, size=self.game.character.age,
                                     pad=self.game.character.age // 2,
                                     angel=self.game.character.angel)
            self.show_stats()
        else:

            if not self._is_start:
                self.win.blit(self.background, (0, 0))
                self.game.animate.compile(self.game.character.skeleton)
                self.game.animate.render_starting_animation(self.win)
                self._is_start = True

        pygame.display.flip()

    @misc.sound.button
    def _on_leave(self):
        # todo  saves records
        self.game.update_state(GameState.MENU)
        self.game.save()
        self.game.reset()

    def update(self, delta_t, event):
        """
        update the game attributes and the entities
        by the delta time or _event
        :param delta_t: delta time is speed of updating
        :param event: pygame _event

        """
        print("moshe")
        if self.game.is_paused:
            return
        for button in self.buttons:
            button.update(event)
        self.game.animate(rate=7 / delta_t)
        if not self.game.animate.active and not self.game.animate._inverted:
            self.idle()

    @misc.sound.button
    def dance(self):
        """
        perform dancing

        """
        if self.game.is_freezed:
            return
        self.game.freeze_auto_reducing(self.btn_animation)
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.ANIMATION1)

    @misc.sound.button
    def make_flip(self):
        """
        perform flip
        :return:
        """
        if not self.game.character.set_flip(self.game.animate.active):
            return
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.FLIP)

    @misc.sound.button
    def sleep(self):
        """
        perform dead
        :return:
        """
        self.game.animate.compile(self.game.character.skeleton)
        self.game.animate.execute(self.game.character.Actions.SLEEP)
        self.game.character.set_sleep(self.game.animate.active)

    def idle(self):
        """
        idle animation
        :return:
        """
        self.game.animate.compile(self.game.character.skeleton)

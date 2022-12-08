import pygame


from commons import misc
from .screen import Screen
from entities import Button
from commons.utils import (
    RGBColors,
    GameState,
    print_text_to_screen
)


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

    @misc.sound.button
    def _on_leave(self):
        self.game.update_state(GameState.MAIN)


    def render(self):
        self.win.fill(RGBColors.BLACK.value)
        self.win.blit(self.background, (0, 0))
        for btn in self.buttons:
            btn.draw(self.win)
        print_text_to_screen("SHOP", self.win, 100, 100, color=RGBColors.WHITE.value)
        print_text_to_screen(f"your coins : {self.game.character.coins}",
                             self.win, 300, 100, color=RGBColors.WHITE.value)
        print_text_to_screen(f"pizza price : {self.game.shop['pizza'].price}",
                             self.win, 270, 240, size=15, vertical=False, color=RGBColors.WHITE.value)
        print_text_to_screen(f"drink price : {self.game.shop['drink'].price}",
                             self.win, 400, 240, size=15, vertical=False, color=RGBColors.WHITE.value)
        pygame.display.flip()

    def update(self, delta_t, event):
        for btn in self.buttons:
            btn.update(event)

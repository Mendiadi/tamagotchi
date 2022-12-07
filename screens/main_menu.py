import pygame


from .screen import Screen
from entities import Button
from commons.utils import (
        RGBColors,
        GameState,
        print_text_to_screen
)

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


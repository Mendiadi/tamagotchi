import threading
import pygame


from .screen import Screen
from commons.utils import (
    GameState,
    RGBColors,
    print_text_to_screen
)

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
        print_text_to_screen("TAMAGOCHI", self.win, 100, 100)
        pygame.display.flip()

    def update(self, delta_t, event): ...


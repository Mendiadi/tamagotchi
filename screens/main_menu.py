import pygame


from commons import misc
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
        self._state = "main"
        # main layer buttons
        self.start_btn = Button((100, 300), RGBColors.BLACK, "START")
        self.start_btn.set_onclick_function(self._on_leave)
        self.option_btn = Button((100, 500), RGBColors.BLACK, "OPTIONS")
        self.option_btn.set_onclick_function(self._on_options)
        self.about_btn = Button((100, 700), RGBColors.BLACK, "ABOUT")
        self.about_btn.set_onclick_function(self._on_about)
        self.buttons = (self.start_btn,self.option_btn,self.about_btn)
        # option layer buttons
        self.mute_btn = Button((100, 200), RGBColors.BLACK, "mute")
        self.mute_btn.set_onclick_function(self._mute)
        self.back_option_btn = Button((100, 500), RGBColors.BLACK, "back")
        self.back_option_btn.set_onclick_function(self._on_main)

        self.option_buttons = (self.mute_btn,self.back_option_btn)

        # about buttons

        self.back_about_btn = Button((100, 200), RGBColors.BLACK, "back")
        self.back_about_btn.set_onclick_function(self._on_main)
        self.buttons_about = (self.back_about_btn,)

        self._states = {
        "main":(self.buttons,"THIS IS MAIN MENU"),
        "options":(self.option_buttons,"OPTIONS"),
        "about":(self.buttons_about,"ABOUT")
        }
    @misc.sound.button
    def _on_main(self):
        self._state = "main"
    @misc.sound.button
    def _on_about(self):
        self._state = "about"
    @misc.sound.button
    def _mute(self):
        if not self.game.is_muted:
            misc.sound.music()
            self.mute_btn.txt = "unmute"
            self.mute_btn.update_rect()
            self.game.is_muted = True
        else:
            misc.sound.music(True)
            self.mute_btn.txt = "mute"
            self.mute_btn.update_rect()
            self.game.is_muted =False
    @misc.sound.button
    def _on_leave(self):
        # todo load saves
        self.game.start_game()
        self.game.update_state(GameState.MAIN)
    @misc.sound.button
    def _on_options(self):
        self._state = "options"


    def render(self):
        buttons,msg = self._states[self._state]
        self.win.fill(RGBColors.WHITE.value)
        for button in buttons:
            button.draw(self.win)
        print_text_to_screen(msg, self.win, 100, 100)
        pygame.display.flip()

    def update(self, delta_t, event):
        buttons, _ = self._states[self._state]
        for button in buttons:
            button.update(event)


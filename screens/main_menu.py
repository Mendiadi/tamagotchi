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
        self.start_btn = Button((300, 200), RGBColors.BLACK, "NEW GAME")
        self.start_btn.set_onclick_function(self._on_leave)
        self.load_btn = Button((300, 400), RGBColors.BLACK, "LOAD SAVES")
        self.load_btn.set_onclick_function(self._on_load_saves)
        self.option_btn = Button((300, 500), RGBColors.BLACK, "OPTIONS")
        self.option_btn.set_onclick_function(self._on_options)
        self.about_btn = Button((300, 600), RGBColors.BLACK, "ABOUT")
        self.about_btn.set_onclick_function(self._on_about)
        self.buttons = (self.start_btn, self.option_btn,
                        self.about_btn,self.load_btn)
        # load saves layer
        self.back_load_btn = Button((300, 500), RGBColors.BLACK, "back")
        self.back_load_btn.set_onclick_function(self._on_main)

        # option layer buttons
        self.mute_btn = Button((300, 200), RGBColors.BLACK, "mute")
        self.mute_btn.set_onclick_function(self._mute)
        self.back_option_btn = Button((300, 500), RGBColors.BLACK, "back")
        self.back_option_btn.set_onclick_function(self._on_main)

        self.option_buttons = (self.mute_btn, self.back_option_btn)

        # about buttons

        self.back_about_btn = Button((300, 200), RGBColors.BLACK, "back")
        self.back_about_btn.set_onclick_function(self._on_main)
        self.buttons_about = (self.back_about_btn,)

        self._states = {
            "main": (self.buttons, "THIS IS MAIN MENU"),
            "options": (self.option_buttons, "OPTIONS"),
            "about": (self.buttons_about, "ABOUT"),
            "load":(self._create_saves_buttons(),"LOAD SAVES")
        }

    def _create_saves_buttons(self):
        saves = self.game.db.get_all_saves()
        print(saves)
        buttons = []
        if saves:
            for i,save in enumerate(saves):
                btn = Button((300, 200 + ((10+i) * 10)), RGBColors.BLACK, save.name)
                btn.set_onclick_function(lambda :self._on_leave(save))
                buttons.append(btn)
        buttons.append(self.back_load_btn)
        print(buttons)
        return buttons

    @misc.sound.button
    def _on_load_saves(self):
        self._state = "load"


    @misc.sound.button
    def _on_main(self):
        self._state = "main"

    @misc.sound.button
    def _on_about(self):
        self._state = "about"

    @misc.sound.button
    def _mute(self):
        """
        muted/unmute the music theme
        change the button to mute/unmute
        :return:
        """
        if not self.game.is_muted:
            misc.sound.music()
            self.mute_btn.txt = "unmute"
            self.mute_btn.update_rect()
            self.game.is_muted = True
        else:
            misc.sound.music(True)
            self.mute_btn.txt = "mute"
            self.mute_btn.update_rect()
            self.game.is_muted = False

    @misc.sound.button
    def _on_leave(self,save=None):
        self.game.start_game(save)
        self.game.update_state(GameState.MAIN)

    @misc.sound.button
    def _on_options(self):
        self._state = "options"

    def render(self):
        buttons, msg = self._states[self._state]
        self.win.fill(RGBColors.WHITE.value)

        if buttons:
            for button in buttons:
                button.draw(self.win)
        print_text_to_screen(msg, self.win, 100, 100)
        pygame.display.flip()

    def update(self, delta_t, event):
        buttons, _ = self._states[self._state]

        if buttons:
            for button in buttons:
                button.update(event)

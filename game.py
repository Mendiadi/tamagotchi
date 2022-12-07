import threading
import time
import pygame

from characters.demogordan2 import Demogordan2
from characters.demogordan3 import Demogordan3
from commons import misc, animator
from commons.utils import GameState
from characters import Demogordan
from commons.food import Pizza, Drink
from screens import (
    MainGame,
    MainMenu,
    SplashScreen,
    ShopScreen
)


class Tamagotchi:
    HEIGHT, WIDTH = 800, 800
    FPS = 60

    def __init__(self):
        self.character = None
        self.event_thread = threading.Event()
        self.animate = None
        self.is_paused = False
        self.screen = None
        self.run = True
        self.db = None
        self.images = None
        self.shop = {"pizza": Pizza(), "drink": Drink()}
        self.is_muted = False

    def reduce_params(self):
        """REDUCING VALUES BY X TIME RUNS IN THREAD"""
        time.sleep(5)
        start = time.time()
        end = 0
        while True:
            time.sleep(5)
            if self.character.food_bar > 0:
                self.character.food_bar -= 2
            if end - start > 15: # if 3 secs passed
                if self.character.happy > 0:
                    if not self.character.food_bar < 50:
                        self.character.happy -= 5
                    else:
                        self.character.happy -= 10
                    start = time.time()
                    end = 0
                    continue
            if self.character.energy > 0:
                self.character.energy -= 2
            end = time.time()

    def start_game(self):
        """init new game """
        self.character = Demogordan2()
        self.animate = animator.Animator(self.character.skeleton, self.event_thread)
        threading.Thread(target=self.reduce_params,daemon=True).start()


    def load(self, win):
        """"""
        # todo bring back the splash screen
        # db call for load saves
        self.images = misc.load_images()
        misc.sound.load_sounds()
        self.screen = SplashScreen(win, self)
        # self.start_game()
        # self.screen = MainGame(win,self)

    def update_state(self, state):
        """updating game state"""
        if state == GameState.MAIN:
            if not self.is_muted:
                misc.sound.music(True)
            self.screen = MainGame(self.screen.win, self)
        elif state == GameState.MENU:
            self.screen = MainMenu(self.screen.win, self)
        elif state == GameState.SHOP:
            self.screen = ShopScreen(self.screen.win, self)

    def update_content(self):
        """Updating the content of the game"""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            time.sleep(0.0125)
            self.pause()

    def pause(self):
        """pause the game and the music"""
        self.is_paused = not self.is_paused
        if self.is_paused:
            misc.sound.music()
            self.event_thread.clear()
        else:
            self.event_thread.set()
            if not self.is_muted:
                misc.sound.music(True)



    def mainloop(self):
        threading.main_thread().name = "mainloop"
        clock = pygame.time.Clock()
        dt = self.FPS
        while self.run:
            pygame.display.set_caption(f"FPS {int(clock.get_fps())}")
            temp_event = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    break
                temp_event = event
                self.update_content()
            self.screen.update(dt, temp_event)
            self.screen.render()
            dt = clock.tick(self.FPS)

        pygame.quit()

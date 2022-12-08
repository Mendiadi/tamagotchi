import threading
import time
import pygame


from commons import misc, animator
from commons.utils import GameState
from characters import (
    Demogordan,
    Demogordan2,
    Demogordan3,
    Demogordan4,
    Demogordan5,
    Demogordan6,
    Demogordan7
)
from commons.food import Pizza, Drink
from screens import (
    MainGame,
    MainMenu,
    SplashScreen,
    ShopScreen
)
from DB.db import DB


class Tamagotchi:
    HEIGHT, WIDTH = 800, 800
    FPS = 60

    def __init__(self):
        self.characters_collection = {  1:Demogordan,
                                        2:Demogordan2,
                                        3:Demogordan3,
                                        4:Demogordan4,
                                        5:Demogordan5,
                                        6:Demogordan6,
                                        7:Demogordan7}
        self.character = None
        self.event_thread = threading.Event()
        self.animate = None
        self.is_paused = False
        self.screen = None
        self.run = True
        self.db = DB()
        self.images = None
        self.shop = {"pizza": Pizza(), "drink": Drink()}
        self.is_muted = False
        self.evolution = None # means demogordan upgrade
        self.is_freezed = False
        self.current_save = None


    def reset(self):...

    def reduce_params(self):
        """REDUCING VALUES BY X TIME RUNS IN THREAD"""
        time.sleep(5)
        start = time.time()
        freeze_start = 0
        freeze_end = 0
        end = 0
        while True:

            time.sleep(5)
            if self.is_paused:
                continue
            if self.is_freezed:
                if freeze_end - freeze_start >= 10:
                    self.is_freezed = False
                    freeze_start = 0
                    freeze_end = 0
                    continue
                if not freeze_start:
                    freeze_start = time.time()
                freeze_end = time.time()
                continue
            if self.character.food_bar > 0:
                self.character.food_bar -= 2
            if end - start > 15:  # if 3 secs passed
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

    def freeze_auto_reducing(self,btn_dance):
        """
        freeze the auto reducing stats runs a thread
        timer after 10 seconds, calls when user hits dance button
        make the button disabled
        :param btn_dance: the button reference
        :return:
        """
        btn_dance.hide()
        self.is_freezed = True
        def unfreezed():
            btn_dance.show()
            timer.cancel()
        timer = threading.Timer(90,unfreezed)
        timer.setDaemon(True)
        timer.start()



    def start_game(self,save=None):
        """
            init new game if you pass save it will init game with
            save data otherwise it will start new game
            :param save: a user saved game
        """
        if not save:
            self.character = Demogordan2()
        else:
            self.current_save = save
            self.character = self.characters_collection[self.current_save.evolution]()
            self.evolution = self.current_save.evolution
            self.character.coins = self.current_save.coins
            self.character.level = self.current_save.level
            self.character.inventory = self.current_save.inventory
        self.animate = animator.Animator(self.character.skeleton, self.event_thread)
        threading.Thread(target=self.reduce_params, daemon=True).start()

    def change_evolution(self, evo):
        """
        Change the evolution to the given one
        save the progress and start new level
        :param evo:
        :return:
        """
        #todo make character collections and implement level up
        self.character = self.characters_collection[evo]
        self.save()
        self.start_game()

    def save(self):
        """
        save the recent progress
        call the sqlite3 database
        if save already in it will update it
        :return:
        """
        save = self.db.get_save(self.current_save)
        if not save:
            self.db.add_save(self.current_save)
        else:
            # change save
            self.db.update_save(self.current_save)



    def load(self, win):
        """
        loading the game assets and data
        :param win:
        :return:
        """
        self.images = misc.load_images()
        misc.sound.load_sounds()
        self.screen = SplashScreen(win, self)



    def update_state(self, state):
        """updating game state"""
        if state == GameState.MAIN:
            if not self.is_muted:
                misc.sound.music(True)
            # issue todo bug while btn dance still visible after shop
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

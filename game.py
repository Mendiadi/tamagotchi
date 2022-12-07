import enum
import threading
import time
import pygame


import misc
import animator
from utils import GameState
from character import Character
from food import Pizza,Drink
from screen import (
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
        self.shop = {"pizza":Pizza(),"drink":Drink()}


    def start_game(self):
        self.character = Character()
        self.animate = animator.Animator(self.character.skeleton, self.event_thread)


    def load(self,win):
        #todo bring back the splash screen
        # db call for load saves
        self.images = misc.load_images()
        misc.sound.load_sounds()
        self.screen = SplashScreen(win,self)
        # self.start_game()
        # self.screen = MainGame(win,self)


    def update_state(self,state):
        if state == GameState.MAIN:
            self.screen = MainGame(self.screen.win,self)
        elif state == GameState.MENU:
            self.screen = MainMenu(self.screen.win,self)
        elif state == GameState.SHOP:
            self.screen = ShopScreen(self.screen.win,self)

    def update_content(self):
        """Updating the content of the game"""

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            time.sleep(0.0125)
            self.pause()


    def pause(self):
        if self.is_paused:
            self.event_thread.clear()
        else:
            self.event_thread.set()
        self.is_paused = not self.is_paused
        print("pause",self.is_paused)


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
            self.screen.update(dt,temp_event)
            self.screen.render()
            dt = clock.tick(self.FPS)

        pygame.quit()




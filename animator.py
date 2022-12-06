import threading
import typing

import pygame
import time
import numpy as np

from utils import RGBColors



class Animator:

    def __init__(self, board):
        self._inverted = False
        self._rate = None
        self._board = board

        self._commands = {
            "dead": self._dead,
            "flip": self._flip,
            "invert": self._invert
        }
        self._exec = None
        self.init_rect_pos = (180,190)
        self._active = False
        self.ready = False
        self.surface = pygame.Surface((450,350))
        self.rect = self.surface.get_rect()
        self.rect.x,self.rect.y = self.init_rect_pos
        self.event = threading.Event()
        self.animate_x = self.rect.x
        threading.Thread(target=self.animate_moves,daemon=True).start()

    def animate_moves(self):
        while 1:
            self.event.wait()

            self.execute('move', ["left", "right", "l_init", "r_init"])
            for i in range(6):
                time.sleep(0.4)

                self.move_surface(self.animate_x - (i*2.5),self.rect.y)

            threading.Thread(target=self._invert, daemon=True).start()

            self.execute('move', ["left", "right", "l_init", "r_init"])
            for i in range(6):
                time.sleep(0.4)
                self.move_surface(self.animate_x + (i*2.5), self.rect.y)
            threading.Thread(target=self._invert, daemon=True).start()



    def render(self, win:pygame.Surface, pad=30, angel=4.5, size=45):

        win.blit(self.surface,(self.rect.x,self.rect.y))
        self.surface.fill("black")
        for i in range(10):
            for j in range(10):
                if self._board[i][j] == 1:
                    pygame.draw.rect(self.surface, RGBColors.SKIN_COLOR.value,
                                     ((j + angel) * pad, (angel + i) * pad, size, size))
                elif self._board[i][j] == 0:
                    pygame.draw.rect(self.surface, RGBColors.BLACK.value,
                                     ((j + angel) * pad, (angel + i) * pad, size, size))
                elif self._board[i][j] == 2:
                    pygame.draw.rect(self.surface,RGBColors.PINK.value,
                                     ((j + angel) * pad, (angel + i) * pad, size, size))

    def move_surface(self,x,y):

        self.rect.x = x
        self.rect.y = y

    def _invert(self):
        print("invert")
        self._inverted = not self._inverted
        new_matrix = []
        for i, row in enumerate(self._board):
            a = list(row).copy()
            a.reverse()
            new_matrix.append(a)
        self._board = new_matrix
        self._perform()

    def _flip(self):
        time.sleep(self._rate)
        self._board = np.flip(self._board, axis=0)
        time.sleep(self._rate)
        self._board = np.flip(self._board, axis=1)
        time.sleep(self._rate)
        self._board = np.flip(self._board, axis=0)
        time.sleep(self._rate)

    def _dead(self):
        self.event.clear()

        time.sleep(self._rate)
        if self._inverted:
            self._inverted = False
            self._board = list(zip(*self._board[::]))
        else:
            self._board = list(zip(*self._board[::-1]))

        time.sleep(3)


    def compile(self, board):
        self._board = board
        size_row = len(self._board) - 1  # 9
        size_col = len(self._board[0]) - 1  # 9
        leg_right_pos = size_col - 1  # 9
        leg_left_pos = leg_right_pos - 5  # 4
        left_leg = (size_row, leg_left_pos), (size_row, leg_left_pos - 1)
        left_leg_init = left_leg[1], left_leg[0]
        right_leg = (size_row, leg_right_pos), (size_row, leg_right_pos - 1)
        right_leg_init = right_leg[1], right_leg[0]
        right_leg_inverted = (size_row, leg_left_pos - 2), (size_row, leg_left_pos - 1)
        right_leg_init_inverted = right_leg_inverted[1], right_leg_inverted[0]
        left_leg_inverted = (size_row, leg_right_pos - 2), (size_row, leg_right_pos - 1)
        left_leg_inverted_init = left_leg_inverted[1], left_leg_inverted[0]
        self._legs = {
            "left": lambda: self._move(*left_leg)
            , "right": lambda: self._move(*right_leg),
            "r_init": lambda: self._move(*right_leg_init),
            "l_init": lambda: self._move(*left_leg_init)
        }
        self._legs_invert = {
            "left": lambda: self._move(*left_leg_inverted)
            , "right": lambda: self._move(*right_leg_inverted),
            "r_init": lambda: self._move(*right_leg_init_inverted),
            "l_init": lambda: self._move(*left_leg_inverted_init)
        }

    def _move_legs(self, moves):
        print("move legs")
        for move in moves:
            time.sleep(self._rate)
            if not self._inverted:
                self._legs[move]()
            else:
                self._legs_invert[move]()

    def execute(self, command: typing.Literal['flip', 'dead', 'invert', 'move','animation'], moves=None):
        if command == 'move' and moves:
            self._exec = lambda: self._move_legs(moves)
        elif command == "animation":
            self.event.set()
        else:
            self._exec = self._commands[command]
        self.ready = True

    def __call__(self, rate, *args, **kwargs):
        self._rate = rate
        if not self._active and self.ready:
            threading.Thread(target=self._perform,daemon=True).start()
            self._active = True

    def _perform(self):
        if self._exec:
            self._exec()
        self._active = False
        self.ready = False

    def _move(self, src, dest):
        if type(self._board[0]) == tuple:
            return

        self._board[src[0]][src[1]] = 0
        self._board[dest[0]][dest[1]] = 1

import threading
import typing
import pygame
import time
import numpy as np


from commons.utils import RGBColors,print_text_to_screen


class Animator:
    """
    class to manage and performing the animations
    of the main character
    """

    def __init__(self, board,event_thread):
        self._inverted = False
        self._rate = None
        self._board = board

        self._commands = {
            "animation": self.animation_1,
            "sleep": self._sleep,
            "flip": self._flip,

        }
        self._exec = None
        self.init_rect_pos = (180, 190)
        self._active = False
        self.ready = False
        self.surface = pygame.Surface((450, 350))
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = self.init_rect_pos
        self.event = event_thread
        self.animate_x = self.rect.x
        self.need_to_move_surface = False
        self.birth = False #todo set build False

        threading.Thread(target=self.move_sub_surface, daemon=True, name="move_surface").start()

    # **************** Animations ******************************

    def _start_animation(self,win):

        self._active = True
        cmd = "for ( int i = 0; i < count; i++ ) % {%"  \
              "    if ( td4 != 0 || td4 >= x )%" \
              "        return success_building_your_pet;%" \
              "    else%" \
              "        return 0;% }"
        y = 200
        i = 0
        for  c in (cmd):
            i += 1
            if c == "%":
                y += 20
                i = 1
                continue
            print(c)
            time.sleep(0.02)
            print_text_to_screen(c, win, x=130 + (i*9),
                                 y=y, size=20, color=RGBColors.GREEN.value, vertical=False)
        time.sleep(2)

        sep=True
        size=20
        pad=10
        angel=12

        self.render(win,pad+7,angel+6,size,sep)
        self.birth = True
        self.stop()


    def render_starting_animation(self,win):
        if not self._active:
            threading.Thread(target=self._start_animation,
                             daemon=True,args=(win,),name="code").start()

    def move_sub_surface(self):
        """
        performing the surface moves
        runs in thread
        :return:
        """
        while 1:
            self.event.wait()
            if not self.need_to_move_surface:
                continue
            for i in range(5):
                time.sleep(0.5)
                self._move_surface(self.animate_x - (i * 3), self.rect.y)
            for i in range(5):
                time.sleep(0.5)
                self._move_surface(self.animate_x + (i * 3), self.rect.y)



    def animation_1(self):
        """
        animation 1 performing
        :return:
        """
        start = time.time()
        end = 0
        max_time = 10
        while end - start < max_time:
            self.event.wait()
            self._move_legs(["left", "right", "l_init", "r_init"])
            self._invert()
            self._move_legs(["left", "right", "l_init", "r_init"])
            self._invert()
            time.sleep(self._rate)
            end = time.time()

        self.stop()

    # *********************** Operations Methods **************************

    def render(self, win, pad=30, angel=4.5, size=45,sep=False):
        """
        render the matrix to the target surface
        :param win: surface
        :param pad: number to know how much distance between pixels
        :param angel: number to figure out position to render
        :param size: size of each pixel (rect)
        :return:
        """
        print(threading.current_thread().name)

        if sep:
            target = win

        else:
            target = self.surface
            win.blit(target, (self.rect.x, self.rect.y))
            target.fill(RGBColors.BLACK.value)
        for i in range(10):
            for j in range(10):
                if sep:
                    time.sleep(0.05)
                if self._board[i][j] == 1:
                    pygame.draw.rect(target, RGBColors.SKIN_COLOR.value,
                                     ((j + angel) * pad, (angel + i) * pad, size, size))
                elif self._board[i][j] == 0:
                    pygame.draw.rect(target, RGBColors.BLACK.value,
                                     ((j + angel) * pad, (angel + i) * pad, size, size))
                elif self._board[i][j] == 2:
                    pygame.draw.rect(target, RGBColors.PINK.value,
                                     ((j + angel) * pad, (angel + i) * pad, size, size))

    def compile(self, board):
        """
        take the board and load the new state of the board
        used to restart or update the board
        :param board: character board
        :return:
        """
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

    def execute(self, command: typing.Literal['flip', 'dead', 'animation']):
        """
        executing animation by type of animation ,
        this method not start the animation its just update
        the class to know witch animation needs to be performed
        :param command: animation key
        :return:
        """
        self._exec = self._commands[command]
        self.ready = True

    def stop(self):
        """
        stopping the animation
        :return:
        """
        self.event.clear()
        self._active = False
        self.ready = False

    def __call__(self, rate, *args, **kwargs):
        """
        start performing the animation that executed
        on the compiled board
        :param rate: how much time between each frame
        usualy its some small number devided by delta time
        :param args:
        :param kwargs:
        :return:
        """
        self._rate = rate
        if not self._active and self.ready:
            threading.Thread(target=self._exec, daemon=True,name="animation").start()
            self._active = True
            self.event.set()

    # ************************* MISC MOVES *******************************

    def _move_legs(self, moves):
        """
        move character legs
        :param moves: list of moves [left,tight,etc]
        :return:
        """
        for move in moves:
            time.sleep(self._rate)
            if not self._inverted:
                self._legs[move]()
            else:
                self._legs_invert[move]()

    def _move(self, src, dest):
        """
        move / swap pixels
        :param src:
        :param dest:
        :return:
        """
        if type(self._board[0]) == tuple:
            return
        self._board[src[0]][src[1]] = 0
        self._board[dest[0]][dest[1]] = 1

    def _flip(self):
        """
        make a flip
        :return:
        """
        time.sleep(self._rate)
        self._board = np.flip(self._board, axis=0)
        time.sleep(self._rate)
        self._board = np.flip(self._board, axis=1)
        time.sleep(self._rate)
        self._board = np.flip(self._board, axis=0)
        time.sleep(self._rate)
        self.stop()

    def _sleep(self):
        """
        perform dead
        :return:
        """
        self.event.clear()
        time.sleep(self._rate)
        if self._inverted:
            self._inverted = False
            self._board = list(zip(*self._board[::]))
        else:
            self._board = list(zip(*self._board[::-1]))
        time.sleep(1)
        self.stop()

    def _invert(self):
        """
        invert the character
        :return:
        """
        self._inverted = not self._inverted
        new_matrix = []
        for i, row in enumerate(self._board):
            a = list(row).copy()
            a.reverse()
            new_matrix.append(a)
        self._board = new_matrix

    def _move_surface(self, x, y):
        """
        move the sub surface
        :param x:
        :param y:
        :return:
        """
        self.rect.x = x
        self.rect.y = y

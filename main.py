
import threading
import time
import numpy as np

import pygame

pygame.init()
win = pygame.display.set_mode((800, 800))


def invert_matrices(matrix):
    new_matrix = []
    for i, row in enumerate(matrix):
        a = list(row).copy()
        a.reverse()
        new_matrix.append(a)

    return new_matrix


class Animate:

    def __init__(self):
        self.rate = 0.12
        self.board = None
        self.init_board()

        size_row = len(self.board) - 1  # 10
        size_col = len(self.board[0]) - 1  # 9
        if size_row != size_col:
            size_col += abs(size_row - size_col)  # 10

        leg_right_pos = size_col - 1  # 9
        leg_left_pos = leg_right_pos - 5  # 4

        self.left_leg = (size_row, leg_left_pos), (size_row, leg_left_pos - 1)
        self.left_leg_init = self.left_leg[1], self.left_leg[0]
        self.right_leg = (size_row, leg_right_pos), (size_row, leg_right_pos - 1)
        self.right_leg_init = self.right_leg[1], self.right_leg[0]
        self.a1 = (size_row, leg_left_pos - 2), (size_row, leg_left_pos - 1)
        self.a2 = self.a1[1], self.a1[0]
        self.b1 = (size_row, leg_right_pos - 2), (size_row, leg_right_pos - 1)
        self.b2 = self.b1[1], self.b1[0]
        self.command_dict = {
            "left": lambda: self.move(*self.left_leg)
            , "right": lambda: self.move(*self.right_leg),
            "r_init": lambda: self.move(*self.right_leg_init),
            "l_init": lambda: self.move(*self.left_leg_init)
        }
        self.command_dict1 = {
            "left": lambda: self.move(*self.b1)
            , "right": lambda: self.move(*self.a1),
            "r_init": lambda: self.move(*self.a2),
            "l_init": lambda: self.move(*self.b2)
        }

        self.temp = None

    def init_board(self):
        self.board = [
            [0, 0, 0, 2, 2, 2, 2, 2, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 1, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0]]

    def invert(self):
        self.board = invert_matrices(self.board)
        time.sleep(self.rate)
        self.board = invert_matrices(self.board)
        time.sleep(self.rate)

    def flip(self):

        time.sleep(self.rate)
        self.board = np.flip(self.board, axis=0)

        time.sleep(self.rate)
        self.board = np.flip(self.board, axis=1)

        time.sleep(self.rate)
        self.board = np.flip(self.board, axis=0)

        time.sleep(self.rate)

    def move_legs(self, commands, dict):
        for command in commands:
            time.sleep(self.rate)
            dict[command]()

    def dead(self):
        self.board = list(zip(*self.board[::-1]))
        time.sleep(3)

    def __call__(self, commands, *args, **kwargs):
        self.init_board()
        self.move_legs(commands, self.command_dict)
        self.flip()
        self.move_legs(commands, self.command_dict1)
        self.invert()
        self.move_legs(commands, self.command_dict1)
        self.invert()
        self.flip()
        self.dead()

    def move(self, src, dest):
        if type(self.board[0]) == tuple:
            print(self.board[src[0]][src[1]])
            return

        self.board[src[0]][src[1]] = 0
        self.board[dest[0]][dest[1]] = 1


def animate(callable_obj):
    callable_obj(["left", "right", "l_init", "r_init"])
    callable_obj(["right", "left", "r_init", "l_init"])


def draw_animate(animator, pad=30, angel=4.5, size=45):
    for i in range(10):
        for j in range(10):
            if animator.board[i][j] == 1:
                pygame.draw.rect(win, (0, 0, 0), ((j + angel) * pad, (angel + i) * pad, size, size))
            elif animator.board[i][j] == 0:
                pygame.draw.rect(win, (255, 255, 255), ((j + angel) * pad, (angel + i) * pad, size, size))
            elif animator.board[i][j] == 2:
                pygame.draw.rect(win, (255, 100, 255), ((j + angel) * pad, (angel + i) * pad, size, size))


def redraw(win):
    win.fill("white")
    pad = 30  # is the distance between two rect
    angel = 3  # is the position rate
    angel2 = 15
    size = 45  # size of rect
    draw_animate(animator, pad, angel, size)
    draw_animate(animator2, pad, angel2, 10)

    draw_animate(animator3, 6, 65, 5)
    draw_animate(animator4, 6, 4.5)

    pygame.display.flip()


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        pygame.display.set_caption(f"FPS {int(clock.get_fps())}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        redraw(win)

    pygame.quit()


if __name__ == '__main__':
    animator = Animate()
    animator2 = Animate()
    animator3 = Animate()
    animator4 = Animate()
    threading.Thread(target=animate, args=(animator,), daemon=True).start()
    threading.Thread(target=animate, args=(animator2,), daemon=True).start()
    threading.Thread(target=animate, args=(animator3,), daemon=True).start()
    threading.Thread(target=animate, args=(animator4,), daemon=True).start()
    main()

import tkinter

import pygame
import os
from tkinter import messagebox

import game

def verify_files():
    if os.getcwd()[::-1][:9:][::-1] != "tamagutsi":
        os.chdir("tamagutsi")
    if "assets" not in os.listdir():
        return False, "assets"
    assets_dirs = os.listdir("assets")
    print(assets_dirs)
    if "images" not in assets_dirs:
        return False, "images"
    if "sounds" not in assets_dirs:
        return False, "sounds"
    for img in os.listdir("assets/images"):
        if img[:-4:] not in ("food","drink","bg","shop"):

            return False, img
    for sound in os.listdir("assets/sounds"):
        if sound[:-4:] not in ("button_sound_1","music_bg"):
            return False,sound
    return True,None



def main():
    is_success, info = verify_files()
    if not is_success:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showerror(title="TAMAGOCHI ERROR",
        message=f"Error Cannot find {info} in game files\nplease reinstall the game")
        root.destroy()
        return
    pygame.init()
    tamagochi = game.Tamagotchi()
    win = pygame.display.set_mode((tamagochi.HEIGHT, tamagochi.WIDTH))
    tamagochi.load(win)
    tamagochi.mainloop()


if __name__ == '__main__':
    print(os.getcwd())
    main()



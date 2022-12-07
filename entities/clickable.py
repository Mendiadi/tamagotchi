import pygame


from commons.utils import RGBColors
from .entity import Entity



class Clickable(Entity):
    """
    clickable is an entity that can clicked
    """
    def __init__(self, pos: tuple[int, int], color: RGBColors, width: [float, int] = 50,
                 height: [float, int] = 110):
        super().__init__(pos, color, width, height)
        self.onclick_function = None
        self.onclick_function_args = None
        self.is_clicked = False


    def onrelease(self):
        self.is_clicked = False


    def onclick(self):
        self.is_clicked = True
        if self.onclick_function_args:
            self.onclick_function(*self.onclick_function_args)
        self.onclick_function()

    def event(self,event):

        if not event:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.onclick()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.onrelease()

    def set_onclick_function(self, func, *args):
        self.onclick_function = func
        self.onclick_function_args = args

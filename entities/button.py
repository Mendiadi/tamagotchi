import pygame


from commons.utils import RGBColors
from .clickable import Clickable





class Button(Clickable):
    """
    button is a clickable that provides you highlights colors
    and more buttons actions like text , update rect by text size
    """
    def __init__(self, pos: tuple[int, int],
                 color: RGBColors=RGBColors.WHITE, txt: str="", height: [float, int] = 50,
                 width: [float, int] = 110,font_color:RGBColors=RGBColors.WHITE,
                 hover_color:RGBColors=RGBColors.PINK,image =None,font_size=30):
        super().__init__(pos, color, width, height)

        self.image = image
        self.font_color = font_color.value
        self.txt = txt
        self.font = pygame.font.SysFont("arial", font_size)
        self.hover_color = hover_color.value
        self.render_font = self.font.render(self.txt, True, font_color.value)
        self.rect = (self._x, self._y, self.render_font.get_width() + 10,
                     self.render_font.get_height() + 10)\
        if not self.image else self.image.get_rect(topleft=self.get_pos())
        self.base_color = self.color


    def update_rect(self):
        self.render_font = self.font.render(self.txt, True, self.font_color)
        self.rect = (self._x, self._y, self.render_font.get_width() + 10,
                     self.render_font.get_height() + 10) \
            if not self.image else self.image.get_rect(topleft=self.get_pos())

    def draw(self, win):
        if self.image:
            win.blit(self.image,self.get_pos())
        else:
            super().draw(win)
        self.render_font = self.font.render(self.txt, True, self.font_color)
        win.blit(self.render_font, (self._x, self._y))

    def _on_mark_style(self):
        self.color = self.hover_color

    def _on_leave(self):
        self.color = self.base_color

    def update(self,event):
        if self.mouse_is_over():
            self.event(event)
            self._on_mark_style()
        else:
            self._on_leave()


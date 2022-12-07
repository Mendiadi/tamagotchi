import pygame


from utils import RGBColors
import misc


class Entity:
    def __init__(self, pos, color, width, height):
        self._x, self._y = pos
        self.height = height
        self.width = width
        self.rect = None
        self.color = color.value
        self.is_hide = False

    def mouse_is_over(self) -> bool:
        return pygame.Rect(self.rect).collidepoint(pygame.mouse.get_pos())

    def show(self):
        self.is_hide = False

    def hide(self):
        self.is_hide = True

    def draw(self, win):
        if not self.is_hide:

            pygame.draw.rect(win, self.color, self.rect)

    def to_json(self):
        ...

    def get_pos(self):
        return self._x, self._y


class Clickable(Entity):
    def __init__(self, pos: tuple[int, int], color: RGBColors, width: [float, int] = 50,
                 height: [float, int] = 110):
        super().__init__(pos, color, width, height)
        self.onclick_function = None
        self.onclick_function_args = None
        self.is_clicked = False


    def onrelease(self):
        self.is_clicked = False

    @misc.sound.button
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


class Button(Clickable):

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
        if not image else image.get_rect(topleft=self.get_pos())
        self.base_color = self.color


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


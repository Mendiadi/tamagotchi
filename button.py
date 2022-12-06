import pygame


from utils import RGBColors
import sounds


class Entity:
    def __init__(self, pos, color, width, height):
        self._x, self._y = pos
        self.height = height
        self.width = width
        self.rect = None
        self.color = color.value
        self.is_hide = False

    def mouse_is_over(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.entity_is_over((mouse_x, mouse_y))

    def entity_is_over(self, entity_pos):
        x, y = entity_pos
        if x not in range(self._x, self._x + self.width):
            return False
        if y not in range(self._y, self._y + self.height):
            return False
        return True

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

    @sounds.button
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

    def __init__(self, pos: tuple[int, int], color: RGBColors, txt: str, height: [float, int] = 50,
                 width: [float, int] = 110,font_color:RGBColors=RGBColors.WHITE,
                 hover_color:RGBColors=RGBColors.PINK):
        super().__init__(pos, color, width, height)

        self.txt = txt
        self.font = pygame.font.SysFont("arial", 30)
        self.hover_color = hover_color.value
        self.render_font = self.font.render(self.txt, True, font_color.value)
        self.rect = (self._x, self._y, self.render_font.get_width() + 10,
                     self.render_font.get_height() + 10)
        self.base_color = self.color
    def draw(self, win):
        super().draw(win)
        win.blit(self.render_font, (self._x, self._y))

    def _on_mark_style(self):
        self.color = self.hover_color

    def _on_leave(self):
        self.color = self.base_color

    def update(self,event):

        if self.mouse_is_over():
            self.event(event)
        if self.mouse_is_over():
            self._on_mark_style()
        else:
            self._on_leave()


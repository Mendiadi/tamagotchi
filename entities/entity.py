import pygame

class Entity:
    """
    Entity is objects that can be rendered to the surface
    and player can interact them
    """
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
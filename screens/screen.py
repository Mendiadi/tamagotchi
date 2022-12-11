import abc


class Screen(abc.ABC):
    """Abstract screen class"""

    def __init__(self, win, tamagochi):
        self.win = win
        self.game = tamagochi

    @abc.abstractmethod
    def render(self):
        """
        virtual pure func rendering all the entities to the screen
        """
        ...

    @abc.abstractmethod
    def _on_leave(self):
        """virtual pure describe action for leaving screen"""
        ...

    @abc.abstractmethod
    def update(self, delta_t, event):
        """virtual pure func Updating all the data of the game"""
        ...


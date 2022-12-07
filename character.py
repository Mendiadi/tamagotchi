



class Character:
    class Actions:
        FLIP = "flip"
        ANIMATION1 = "animation"
        SLEEP = "sleep"


    def __init__(self):
        self.skeleton = [
            [0, 0, 0, 2, 2, 2, 2, 2, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 1, 0, 1, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 1, 1],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0]]
        self.rate = {
            20: 12,
            25: 11,
            30: 6,
            35: 4
            , 40: 2,
            45: 1,
            50: 0.5
        }
        self.life_bar = 100
        self.food_bar= 50
        self.happy = 100
        self.age = 20
        self.angel = self.rate[self.age]
        self.evolution = 0


    def grow_up(self):
        """
        make the character grow up

        :return:
        """
        if self.age == 50:
            return
        self.age += 5
        self.angel = self.rate[self.age]
        self.evolution += 16.6666
        if self.age < 50:
            self.evolution += 0.1


    def set_sleep(self):
        ...

    def set_awake(self):
        ...

    def eat(self,food):
        self.food_bar += food

    def add_life(self,ratio):
        ...

    def reduce_life(self,ratio):
        ...

    def calculate_happy(self):
        ...
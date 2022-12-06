



class Character:
    class Actions:
        FLIP = "flip"
        MOVE = "move"
        INVERT = "invert"
        DEAD = "dead"


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

        self.life_bar = 100
        self.food_bar= 100
        self.happy = 100
        self.age = 20
        self.angel = 0.6
        self.angel_ratio_2 = 0.15
        self.angel_ratio_3 = 0.3
        self.evolution = 0


    def grow_up(self):
        # 20 -> 10 -> 0.6
        # 25 -> 12 -> 0.9
        # 30 -> 15 -> 1.5
        # 35 -> 17 -> 2.0
        # 40 -> 20 -> 3.0
        # 45 -> 22 -> 4.0
        # 50 -> 25 -> 6.0
        if self.age == 50:
            return
        if ((self.age + 5) //2) - (self.age // 2) == 2:
             self.angel_ratio_2 *= 2
             self.angel += self.angel_ratio_2
        else:
            self.angel_ratio_3 *= 2
            self.angel += self.angel_ratio_3
        if self.angel > 2:
            self.angel = int(self.angel)
        self.age += 5
        self.evolution += 16.6666
        if self.age < 50:
            self.evolution += 0.1




    def eat(self,food):
        ...

    def add_life(self,ratio):
        ...

    def reduce_life(self,ratio):
        ...

    def calculate_happy(self):
        ...
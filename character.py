from food import Pizza, Drink


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
        self.points = 100
        self.inventory = {"pizza":[Pizza(),Pizza(),Pizza()],"drink":[Drink(),Drink()]}
        self.energy = 0

    def buy(self,food):
        if food.price > self.points:
            return
        self.inventory[food.name].append(food)
        self.points -= food.price

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

    def set_flip(self) -> bool:
        if self.energy < 5:
            return False
        if self.food_bar < 1:
            return False

        self.energy -= 5
        self.food_bar -= 1
        self.points += 5
        return True


    def set_sleep(self):
        if self.energy > 80:
            return

        self.points += 5
        self.energy += 20




    def eat(self,food__):
        food_count = self.inventory[food__.name]
        if not food_count:
            return
        if self.points <= 0:
            return
        if self.energy < 1:
            return
        food = food_count.pop()

        self.food_bar += food.rate
        self.points -= food.price
        self.happy += 2
        self.life_bar += 1
        self.energy -= 1

    def add_life(self,ratio):
        ...

    def reduce_life(self,ratio):
        ...

    def calculate_happy(self):
        ...
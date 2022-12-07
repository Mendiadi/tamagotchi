


class Character:
    class Actions:
        FLIP = "flip"
        ANIMATION1 = "animation"
        SLEEP = "sleep"

    def __init__(self):
        self.skeleton = None
        self.rate = None
        self.life_bar = 100
        self.food_bar = 50
        self.happy = 100
        self.age = 20
        self.angel = None
        self.level = 0
        self.points = 100
        self.inventory = {"pizza": [], "drink": []}
        self.energy = 0

    def buy(self, food):
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
        self.level += 16.6666
        if self.age < 50:
            self.level += 1

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

    def eat(self, food__):
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

    def add_life(self, ratio):
        ...

    def reduce_life(self, ratio):
        ...

    def calculate_happy(self):
        ...


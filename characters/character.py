from commons.misc import sound


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
        self.level = 0 # means grow up rate
        self.coins = 100
        self.inventory = {"pizza": [], "drink": []}
        self.energy = 50

    def buy(self, food):
        if food.price > self.coins:
            return
        sound.buy()
        self.inventory[food.name].append(food)
        self.coins -= food.price

    def grow_up(self):
        """
        make the character grow up

        :return:
        """
        if not (self.food_bar == 100 and self.happy == 100 and self.energy == 100):
            return
        if self.age == 50:
            return
        self.age += 5
        self.angel = self.rate[self.age]
        self.level += 16.6666
        if self.age < 50:
            self.level += 1
        self.energy = 50
        self.food_bar = 50

    def set_flip(self, active) -> bool:
        if active:
            return False
        if self.energy < 5:
            return False
        if self.food_bar < 1:
            return False
        self.energy -= 5
        self.food_bar -= 1
        self.coins += 10
        self.happy += 2
        if self.happy > 100:
            self.happy = 100
        return True

    def set_sleep(self, active):
        """
        update the stats of character
        calls from the button only if animation not active
        :param active:
        :return:
        """
        if active:
            return
        self.happy += 2
        self.coins += 5
        self.energy += 20
        if self.happy > 100:
            self.happy = 100
        if self.energy > 100:
            self.energy = 100

    def eat(self, food__):
        food_count = self.inventory[food__.name]
        if not food_count:
            return
        if self.energy < 1:
            return
        food = food_count.pop()
        self.food_bar += food.rate
        if self.food_bar > 100:
            self.food_bar = 100
        self.happy += 2
        if self.happy > 100:
            self.happy = 100
        self.life_bar += 1
        self.energy -= 1
        sound.eat()

    def add_life(self, ratio):
        ...

    def reduce_life(self, ratio):
        ...

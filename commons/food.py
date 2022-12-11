class Item:
    def __init__(self, price, rate, name):
        self.price = price
        self.rate = rate
        self.name = name

class Food(Item):
    """Provide the basic information about general food"""

    def __init__(self, price, rate, name):
        super().__init__(price,rate,name)


class Pizza(Food):

    def __init__(self):
        super().__init__(10, 5, "pizza")


class Drink(Food):
    def __init__(self):
        super().__init__(5, 2, "drink")


class Medic(Item):
    def __init__(self):
        super().__init__(15,3, "medic")
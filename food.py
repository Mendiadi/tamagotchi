

class Food:
    """Provide the basic information about general food"""
    def __init__(self,price,rate,name):
        self.price = price
        self.rate = rate
        self.name = name


class Pizza(Food):

    def __init__(self):
        super().__init__(10,5,"pizza")


class Drink(Food):
    def __init__(self):
        super().__init__(5,2,"drink")

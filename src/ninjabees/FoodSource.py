class FoodSource:
    def __init__(self, name, nutritional_val, x, y):
        self.name = name
        self.nutritional_val = nutritional_val
        self.amount = 100
        self.x = x
        self.y = y

    def get_amount(self):
        return self.amount

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

from .environment.Entity import Entity, EntityType


class FoodSource(Entity):
    def __init__(self, name, nutritional_val, x, y):
        super().__init__(x, y, EntityType.Food)
        self.nutritional_val = nutritional_val
        self.amount = 100

    def get_amount(self):
        return self.amount

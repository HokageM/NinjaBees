from .environment.Entity import Entity, EntityType


class FoodSource(Entity):
    """
    This class represents a food source.
    """

    def __init__(self, name, nutritional_val, x, y):
        super().__init__(x, y, EntityType.Food)
        self.nutritional_val = nutritional_val
        self.amount = 100

    def get_amount(self):
        """
        Get the amount of food in the food source.
        :return:
        """
        return self.amount

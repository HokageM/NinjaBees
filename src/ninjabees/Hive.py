import random

from .Animator import Animator
from .Bee import Bee

class Hive:
    def __init__(self, name, num_onlooker_bees, x=0, y=0):
        self.name = name
        self.num_onlooker_bees = num_onlooker_bees

        self.food_sources = []
        self.found_food_sources = []

        self.x = x
        self.y = y

        self.bee_population = [Bee("Bee", self),
                               Bee("Bee", self),
                               Bee("Bee", self),
                               Bee("Bee", self),
                               Bee("BeeScout", self, is_scout=True),
                               Bee("BeeScout", self, is_scout=True),
                               Bee("BeeScout", self, is_scout=True),
                               Bee("BeeScout", self, is_scout=True),
                               Bee("BeeScout", self, is_scout=True),
                               Bee("BeeScout", self, is_scout=True),
                               Bee("BeeScout", self, is_scout=True),
                               Bee("BeeScout", self, is_scout=True)
                               ]

        self.map = [['-' for _ in range(200)] for _ in range(90)]
        self.map[self.x][self.y] = 'H'

        Animator.print_hive_status(self)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def add_food_source(self, food_source):
        while food_source.x == self.x and food_source.y == self.y:
            food_source.x = int(random.uniform(0, 89))
            food_source.y = int(random.uniform(0, 199))
        self.food_sources.append(food_source)

    def add_found_food_source(self, food_source):
        self.found_food_sources.append(food_source)

    def calculate_food_source_quality(self, food_source):
        # Calculate the quality of a food source based on its distance from the hive and the nutritional_val of the food
        distance = ((self.x - food_source.x) ** 2 + (self.y - food_source.y) ** 2) ** 0.5
        return food_source.nutritional_val / distance

    def forage(self, max_iterations):
        for iteration in range(max_iterations):
            self.employed_bees_phase()
            self.onlooker_bees_phase()

            for bee in self.bee_population:
                if bee.x != 0 or bee.y != 0:
                    if bee.found_food:
                        self.map[bee.x][bee.y] = 'B'
                    else:
                        self.map[bee.x][bee.y] = 'b'
            for source in self.found_food_sources:
                if source.x != 0 or source.y != 0:
                    self.map[source.x][source.y] = 'F'

            Animator.print_hive_status(self)

    def employed_bees_phase(self):
        for bee in self.bee_population:
            if bee.found_food:
                bee.return_home()
            else:
                bee.explore(self.food_sources)

    def onlooker_bees_phase(self):
        if len(self.found_food_sources) == 0:
            return
        if len(self.found_food_sources) < self.num_onlooker_bees:
            selected_sources = self.found_food_sources
        else:
            selected_sources = random.choices(self.found_food_sources,
                                          weights=[self.calculate_food_source_quality(source) for source in
                                                   self.found_food_sources],
                                          k=self.num_onlooker_bees)

        for bee in self.bee_population:
            if bee.is_scout:
                continue
            if bee.x == 0 and bee.y == 0:
                bee.exploration_goal = random.choice(selected_sources)
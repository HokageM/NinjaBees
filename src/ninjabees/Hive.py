import random

from .Animator import Animator
from .Bee import Bee, BeeJob


class Hive:
    def __init__(self, name, num_onlooker_bees, max_cnt_foraging_bees=100, x=0, y=0):
        self.name = name
        self.num_onlooker_bees = num_onlooker_bees

        self.food_sources = []
        self.found_food_sources = []

        self.x = x
        self.y = y

        self.__current_foraging = 0
        self.max_cnt_foraging_bees = max_cnt_foraging_bees
        self.bee_population = [Bee("Bee", self) for _ in range(200)]

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

            # Update the map
            for bee in self.bee_population:
                if bee.x != 0 or bee.y != 0:
                    if bee.has_found_food():
                        self.map[bee.x][bee.y] = 'S' if bee.get_job() == BeeJob.Scout else 'B'
                    else:
                        self.map[bee.x][bee.y] = 's' if bee.get_job() == BeeJob.Scout else 'b'
            for source in self.found_food_sources:
                if source.x != 0 or source.y != 0:
                    self.map[source.x][source.y] = 'F'

            Animator.print_hive_status(self)

            if len(self.found_food_sources) == len(self.food_sources):
                print(f'All food sources found! In {iteration} iterations')
                return

    def employed_bees_phase(self):
        for bee in self.bee_population:
            if bee.has_found_food():
                bee.return_home()
            else:
                bee.explore(self.food_sources)

    def onlooker_bees_phase(self):
        if len(self.found_food_sources) == 0:
            return

        for bee in self.bee_population:
            if self.__current_foraging < self.max_cnt_foraging_bees:
                # For every bee in population which is currently a scout bee and has not found food,
                # set its food goal random where the probability of
                # selecting a food source is proportional to its quality.
                if bee.get_job() == BeeJob.Scout and not bee.has_found_food():
                    bee.set_food_goal(random.choices(self.found_food_sources,
                                                     weights=[self.calculate_food_source_quality(source) for source in
                                                              self.found_food_sources],
                                                     k=self.num_onlooker_bees)[0])
                    bee.set_job(BeeJob.Forager)
                    self.__current_foraging += 1

            if bee.get_job() == BeeJob.Forager and bee.get_food_goal() is None:
                bee.set_food_goal(random.choices(self.found_food_sources,
                                                 weights=[self.calculate_food_source_quality(source) for source in
                                                          self.found_food_sources],
                                                 k=self.num_onlooker_bees)[0])

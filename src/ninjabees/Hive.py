import random

from .Bee import Bee, BeeJob
from .environment.Entity import Entity, EntityType


class Hive(Entity):
    def __init__(self, name, num_onlooker_bees, max_cnt_foraging_bees=100, x=0, y=0, world=None):
        super().__init__(x, y, EntityType.Hive)

        self.name = name
        self.num_onlooker_bees = num_onlooker_bees
        self.world = world

        self.food_sources = []
        self.found_food_sources = []

        self.__current_foraging = 0
        self.max_cnt_foraging_bees = max_cnt_foraging_bees
        self.bee_population = [Bee("Bee", self, world) for _ in range(200)]

    def add_found_food_source(self, food_source):
        self.found_food_sources.append(food_source)

    def calculate_food_source_quality(self, food_source):
        # Calculate the quality of a food source based on its distance from the hive and the nutritional_val of the food
        distance = ((self.get_x() - food_source.get_x()) ** 2 + (self.get_x() - food_source.get_y()) ** 2) ** 0.5
        return food_source.nutritional_val / distance

    def forage(self):
        self.employed_bees_phase()
        self.onlooker_bees_phase()
        for food_source in self.found_food_sources:
            if food_source not in self.food_sources:
                self.world.add_entity(food_source)
                self.food_sources.append(food_source)

    def employed_bees_phase(self):
        for bee in self.bee_population:
            if bee.has_found_food():
                bee.return_home()
            else:
                bee.explore()

    def onlooker_bees_phase(self):
        if len(self.food_sources) == 0:
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

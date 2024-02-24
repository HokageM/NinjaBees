import random

from .Bee import Bee, BeeJob
from .environment.Entity import Entity, EntityType


class Hive(Entity):
    """
    This class represents a hive.
    """

    def __init__(self, name, num_onlooker_bees, max_cnt_foraging_bees=300, x=0, y=0, world=None):
        super().__init__(x, y, EntityType.Hive)

        self.name = name
        self.num_onlooker_bees = num_onlooker_bees
        self.world = world

        self.food_at_hive = 0
        self.food_sources = []
        self.found_food_sources = {}

        self.__current_foraging = 0
        self.max_cnt_foraging_bees = max_cnt_foraging_bees
        self.bee_population = [Bee("Bee", self, world) for _ in range(600)]

    def add_found_food_source(self, food_source, path_to_food):
        """
        Add a found food source.
        :param food_source:
        :param path_to_food:
        :return:
        """
        index = 0
        x, y = int(self.get_x()), int(self.get_y())
        for step in path_to_food:
            move = path_to_food[index]
            x += move[0]
            y += move[1]
            index += 1
        if x != food_source.get_x() or y != food_source.get_y():  # not a correct path
            raise Exception("Invalid path to food source")
            while True:
                pass

        if food_source not in self.found_food_sources:
            self.found_food_sources[food_source] = list(path_to_food)
        if len(path_to_food) < len(self.found_food_sources[food_source]):
            self.found_food_sources[food_source] = list(path_to_food)

    def calculate_food_source_quality(self, food_source):
        """
        Calculate the quality of a food source.
        :param food_source:
        :return:
        """
        # Calculate the quality of a food source based on its distance from the hive and the nutritional_val of the food
        distance = ((self.get_x() - food_source.get_x()) ** 2 + (self.get_x() - food_source.get_y()) ** 2) ** 0.5
        return food_source.nutritional_val / distance

    def forage(self):
        """
        Forage for food.
        :return:
        """
        self.employed_bees_phase()
        self.onlooker_bees_phase()
        list_food_sources = list(self.found_food_sources)
        for found_food_source in list_food_sources:
            if found_food_source not in self.food_sources:
                self.world.add_entity(found_food_source)
                self.food_sources.append(found_food_source)

    def employed_bees_phase(self):
        """
        Employed bees phase.
        :return:
        """
        for bee in self.bee_population:
            try:
                if bee.has_found_food():
                    bee.return_home()
                else:
                    bee.explore()
            except Exception as e:
                print(e)

    def onlooker_bees_phase(self):
        """
        Onlooker bees phase.
        :return:
        """
        if len(self.found_food_sources) == 0:
            for bee in self.bee_population:
                if bee.wait_for_instructions:
                    bee.wait_for_instructions = False
                    bee.reset()
            return

        for bee in self.bee_population:
            # For every bee in population which is currently a scout bee and has not found food,
            # set its food goal random where the probability of
            # selecting a food source is proportional to its quality.
            if bee.get_job() == BeeJob.Scout and bee.get_x() == self.get_x() and bee.get_y() == self.get_y():
                if bee.has_found_food():
                    self.food_at_hive += 1
                    if bee.get_found_food_source() not in self.found_food_sources:
                        self.add_found_food_source(bee.get_found_food_source(), bee.get_flying_path())
                    if len(bee.get_flying_path()) < len(self.found_food_sources[bee.get_found_food_source()]):
                        self.add_found_food_source(bee.get_found_food_source(), bee.get_flying_path())
                bee.reset()
                if self.__current_foraging < self.max_cnt_foraging_bees:
                    food_source_qualities = [self.calculate_food_source_quality(source) for source in
                                             self.found_food_sources]
                    list_food_sources = list(self.found_food_sources)
                    food_goal = random.choices(list_food_sources,
                                               weights=food_source_qualities, k=self.num_onlooker_bees)[0]
                    path_to_goal = self.found_food_sources[food_goal]

                    bee.set_food_goal(food_goal, list(path_to_goal))
                    bee.set_job(BeeJob.Forager)
                    self.__current_foraging += 1
                    continue
            is_bee_home = bee.get_x() == self.get_x() and bee.get_y() == self.get_y()
            if bee.get_job() == BeeJob.Forager and is_bee_home and bee.wait_for_instructions:
                bee.wait_for_instructions = False
                if bee.has_found_food():
                    self.food_at_hive += 1
                bee.reset()

                food_source_qualities = [self.calculate_food_source_quality(source) for source in
                                         self.found_food_sources]
                list_food_sources = list(self.found_food_sources)
                food_goal = random.choices(list_food_sources,
                                           weights=food_source_qualities, k=self.num_onlooker_bees)[0]
                path_to_goal = self.found_food_sources[food_goal]

                bee.set_food_goal(food_goal, list(path_to_goal))
                continue

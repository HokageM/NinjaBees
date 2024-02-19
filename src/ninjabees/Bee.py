import random
from enum import Enum

from .environment.Entity import Entity, EntityType


class BeeJob(Enum):
    Scout = 0
    Forager = 1


class Bee(Entity):
    def __init__(self, name, hive, world, exploration_radius=1, move_range=5):
        super().__init__(hive.get_x(), hive.get_y(), EntityType.Bee)

        self.name = name
        self.hive = hive
        self.world = world

        # Initially no food source is known
        self.__job = BeeJob.Scout
        self.__food_goal = None

        self.__exploration_radius = exploration_radius
        self.__move_range = move_range

        self.__found_food = False
        self.__found_food_source = None

    def has_found_food(self):
        return self.__found_food

    def get_food_goal(self):
        return self.__food_goal

    def get_found_food_source(self):
        return self.__found_food_source

    def get_job(self):
        return self.__job

    def set_job(self, job):
        self.__job = job

    def set_food_goal(self, food_goal):
        self.__food_goal = food_goal

    def explore(self):
        if self.__food_goal and self.__job != BeeJob.Scout:
            self.move_towards_exploration_goal()
            return
        nearby_sources = [source for source in self.world.get_unclaimed_food_sources() if self.is_within_radius(source)]
        if nearby_sources:
            selected_source = random.choice(nearby_sources)
            self.__found_food = True
            self.__found_food_source = selected_source
        else:
            self.move()

    def is_within_radius(self, food_source):
        distance = ((self.get_x() - food_source.get_x()) ** 2 + (self.get_y() - food_source.get_y()) ** 2) ** 0.5
        return distance <= self.__exploration_radius

    def return_home(self):
        x = self.get_x()
        y = self.get_y()

        if x == self.hive.get_x() and y == self.hive.get_y():
            if self.__found_food_source not in self.hive.food_sources:
                self.hive.add_found_food_source(self.__found_food_source)
            self.__found_food = False
            self.__found_food_source = None
            self.__food_goal = None
        else:
            if x != self.hive.get_x():
                if (x - self.hive.get_x()) > 0:
                    self.set_x(x - 1)
                else:
                    self.set_x(x + 1)
            if y != self.hive.get_y():
                if (y - self.hive.get_y()) > 0:
                    self.set_y(y - 1)
                else:
                    self.set_y(y + 1)

    def move_towards_exploration_goal(self):
        x = self.get_x()
        y = self.get_y()

        if x == self.__food_goal.get_x() and y == self.__food_goal.get_y():
            self.__found_food = True
            self.__found_food_source = self.__food_goal
            self.__food_goal = None
        else:
            if x != self.__food_goal.get_x():
                if (x - self.__food_goal.get_x()) > 0:
                    self.set_x(x - 1)
                else:
                    self.set_x(x + 1)
            if y != self.__food_goal.get_y():
                if (y - self.__food_goal.get_y()) > 0:
                    self.set_y(y - 1)
                else:
                    self.set_y(y + 1)

    def move(self):
        x = self.get_x()
        y = self.get_y()

        x += int(random.uniform(-self.__move_range, self.__move_range))
        y += int(random.uniform(-self.__move_range, self.__move_range))

        self.set_x(x)
        self.set_y(y)

        if x < 0:
            self.set_x(0)
        if y < 0:
            self.set_y(0)
        if x > 89:
            self.set_x(89)
        if y > 199:
            self.set_y(199)

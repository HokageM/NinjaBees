import random

from enum import Enum


class BeeJob(Enum):
    Scout = 0
    Forager = 1


class Bee:
    def __init__(self, name, hive, exploration_radius=1, move_range=5):
        self.name = name
        self.hive = hive
        self.x = self.hive.get_x()
        self.y = self.hive.get_y()

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

    def explore(self, food_sources):
        if self.__food_goal and self.__job != BeeJob.Scout:
            self.move_towards_exploration_goal()
            return
        nearby_sources = [source for source in food_sources if self.is_within_radius(source)]
        if nearby_sources:
            selected_source = random.choice(nearby_sources)
            self.__found_food = True
            self.__found_food_source = selected_source
        else:
            self.move()

    def is_within_radius(self, food_source):
        distance = ((self.x - food_source.x) ** 2 + (self.y - food_source.y) ** 2) ** 0.5
        return distance <= self.__exploration_radius

    def return_home(self):
        if self.x == self.hive.get_x() and self.y == self.hive.get_y():
            if self.__found_food_source not in self.hive.found_food_sources:
                self.hive.add_found_food_source(self.__found_food_source)
            self.__found_food = False
            self.__found_food_source = None
            self.__food_goal = None
        else:
            if self.x != self.hive.get_x():
                if (self.x - self.hive.x) > 0:
                    self.x -= 1
                else:
                    self.x += 1
            if self.y != self.hive.get_y():
                if (self.y - self.hive.y) > 0:
                    self.y -= 1
                else:
                    self.y += 1

    def move_towards_exploration_goal(self):
        if self.x == self.__food_goal.x and self.y == self.__food_goal.y:
            self.__found_food = True
            self.__found_food_source = self.__food_goal
            self.__food_goal = None
        else:
            if self.x != self.__food_goal.x:
                if (self.x - self.__food_goal.x) > 0:
                    self.x -= 1
                else:
                    self.x += 1
            if self.y != self.__food_goal.y:
                if (self.y - self.__food_goal.y) > 0:
                    self.y -= 1
                else:
                    self.y += 1

    def move(self):
        self.x += int(random.uniform(-self.__move_range, self.__move_range))
        self.y += int(random.uniform(-self.__move_range, self.__move_range))

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > 89:
            self.x = 89
        if self.y > 199:
            self.y = 199

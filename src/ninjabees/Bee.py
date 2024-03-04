import random
from enum import Enum

from .environment.Entity import Entity, EntityType


class BeeJob(Enum):
    """
    This class represents the job of a bee.
    """
    Scout = 0
    Forager = 1


class Bee(Entity):
    """
    This class represents a bee.
    """

    ENERGY = 600

    def __init__(self, hive, world, exploration_radius=0):
        super().__init__(hive.get_x(), hive.get_y(), EntityType.Bee)

        self.hive = hive
        self.world = world

        self.__energy = Bee.ENERGY

        # Initially no food source is known
        self.__job = BeeJob.Scout
        self.__food_goal = None

        self.__exploration_radius = exploration_radius

        self.__found_food = False
        self.__found_food_source = None

        self.__home_path = []
        self.__home_path_index = 0
        self.__flying_path = []
        self.__flying_index = 0
        self.__is_path_set_to_hive = False

        self.wait_for_instructions = False

    def has_found_food(self):
        """
        Check if the bee has found food.
        :return:
        """
        return self.__found_food

    def get_food_goal(self):
        """
        Get the food goal for the bee.
        :return:
        """
        return self.__food_goal

    def get_found_food_source(self):
        """
        Get the found food source.
        :return:
        """
        return self.__found_food_source

    def get_job(self):
        """
        Get the job of the bee.
        :return:
        """
        return self.__job

    def set_job(self, job):
        """
        Set the job for the bee.
        :param job:
        :return:
        """
        self.__job = job

    def get_flying_path(self):
        """
        Get the flying path.
        :return:
        """
        return self.__flying_path

    def get_flying_index(self):
        """
        Get the flying index.
        :return:
        """
        return self.__flying_index

    def set_flying_path(self, path):
        """
        Set the flying path.
        :param path:
        :return:
        """
        self.__flying_path = path

    def set_food_goal(self, food_goal, path_to_food):
        """
        Set the food goal for the bee.
        :param food_goal:
        :param path_to_food:
        :return:
        """
        self.__food_goal = food_goal
        self.__flying_path = path_to_food

    def explore(self):
        """
        Explore the environment to find food sources.
        :return:
        """
        if self.__energy == 0 or self.__found_food:
            self.return_home()
            return
        self.__energy -= 1

        if self.__job == BeeJob.Scout:
            food_source = self.world.get_unclaimed_food_source_at(self.get_x(), self.get_y())
            if food_source:
                self.__found_food = True
                self.__found_food_source = food_source
            else:
                self.move()
            return

        self.move_towards_exploration_goal()
        return

    def is_within_radius(self, food_source):
        """
        Check if the bee is within the exploration radius of a food source.
        :param food_source:
        :return:
        """
        return self.get_x() == food_source.get_x() and self.get_y() == food_source.get_y()

    def return_home(self):
        """
        Move the bee back to the hive.
        :return:
        """
        x = self.get_x()
        y = self.get_y()

        if x == self.hive.get_x() and y == self.hive.get_y():
            if self.__found_food:
                self.__is_path_set_to_hive = False
                if self.__job == BeeJob.Scout:
                    self.hive.add_found_food_source(self.__found_food_source, list(self.__flying_path))
            self.wait_for_instructions = True
            return

        if not self.__is_path_set_to_hive:
            self.__is_path_set_to_hive = True
            self.reverse_flying_path()

        move = self.__home_path[self.__home_path_index]
        self.__home_path_index += 1
        x += move[0]
        y += move[1]
        self.set_x(x)
        self.set_y(y)

    def move_towards_exploration_goal(self):
        """
        Move the bee towards the food goal.
        :return:
        """
        x = self.get_x()
        y = self.get_y()

        if x == self.__food_goal.get_x() and y == self.__food_goal.get_y():
            self.__found_food_source = self.__food_goal
            self.__found_food = True
            self.__food_goal = None
            self.__flying_index = 0
            return

        move = self.__flying_path[self.__flying_index]
        self.__flying_index += 1
        x += move[0]
        y += move[1]
        self.set_x(x)
        self.set_y(y)

    def move(self):
        """
        Move the bee in a random direction within a certain range.
        :return:
        """
        x = self.get_x()
        y = self.get_y()

        hive_x = self.hive.get_x()
        hive_y = self.hive.get_y()

        dist_x_r = abs(hive_x - (x + 1)) + 1
        dist_x_l = abs(hive_x - (x - 1)) + 1
        dist_x_n = abs(hive_x - x) + 1
        dist_y_u = abs(hive_y - (y - 1)) + 1
        dist_y_d = abs(hive_y - (y + 1)) + 1
        dist_y_n = abs(hive_y - y) + 1

        move_xy = random.choices([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0),
                                  (1, 1)],
                                 weights=[max(dist_x_l, dist_y_u), max(dist_x_l, 0), max(dist_x_l, dist_y_d),
                                          max(dist_y_u, 0), max(dist_x_n, dist_y_n), max(dist_y_d, 0),
                                          max(dist_x_r, dist_y_u), max(dist_x_r, 0), max(dist_x_r, dist_y_d)],
                                 k=1)[0]

        move_x = move_xy[0]
        move_y = move_xy[1]

        x += move_x
        y += move_y

        if x < 0:
            x = 0
            move_x = 0
        if y < 0:
            y = 0
            move_y = 0
        if x > self.world.get_width() - 1:
            x = self.world.get_width() - 1
            move_x = 0
        if y > self.world.get_height() - 1:
            y = self.world.get_height() - 1
            move_y = 0

        if move_x == 0 and move_y == 0:
            self.move()
            return

        self.set_x(x)
        self.set_y(y)

        self.__flying_path.append((move_x, move_y))

    def reset(self):
        """
        Reset the bee.
        :return:
        """
        self.set_x(self.hive.get_x())
        self.set_y(self.hive.get_y())

        self.__found_food = False
        self.__found_food_source = None
        self.__food_goal = None
        self.__is_path_set_to_hive = False
        self.__energy = Bee.ENERGY

        self.__home_path = []
        self.__home_path_index = 0
        self.__flying_path = []
        self.__flying_index = 0

    def reverse_flying_path(self):
        """
        Reverse the flying path.
        :return:
        """
        reverse_path = []
        for move in self.__flying_path:
            reverse_path.append((-move[0], -move[1]))
        reverse_path.reverse()
        self.__home_path = list(reverse_path)

from ..Animator import Animator
from ..Bee import BeeJob
from .Entity import EntityType


class World:
    """
    This class represents the world of the bee simulation.
    """

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__entities = []

        self.__hive = None
        self.__food_sources = []

        self.__unclaimed_food_sources = []
        self.__n_food_sources = 0

        self.__world_map = [['-' for _ in range(width)] for _ in range(height)]

    def add_food_source(self, food_source):
        """
        Add a food source to the world.
        :param food_source:
        :return:
        """
        self.__unclaimed_food_sources.append(food_source)
        self.__n_food_sources += 1

    def get_unclaimed_food_source_at(self, x, y):
        """
        Get the unclaimed food sources.
        :return:
        """
        for food_source in self.__unclaimed_food_sources:
            if food_source.get_x() == x and food_source.get_y() == y:
                return food_source
        return None

    def add_entity(self, entity):
        """
        Add an entity to the world.
        :param entity:
        :return:
        """
        self.__entities.append(entity)
        if entity.get_type() == EntityType.Hive:
            self.__hive = entity
        elif entity.get_type() == EntityType.Food:
            if entity not in self.__food_sources:
                self.__food_sources.append(entity)

    def is_position_blocked(self, x, y):
        """
        Check if the position is blocked by an entity.
        :param x:
        :param y:
        :return:
        """
        for entity in self.__entities:
            if entity.x == x and entity.y == y:
                return True
        return False

    def update_world_map(self):
        """
        Update the world map with the current entities.
        :return:
        """
        for food in self.__unclaimed_food_sources:
            self.__world_map[food.get_y()][food.get_x()] = 'u'
        for entity in self.__entities:
            entity_type = entity.get_type()
            entity_x = entity.get_x()
            entity_y = entity.get_y()
            if entity_type == EntityType.Bee:
                if entity.has_found_food():
                    self.__world_map[entity_y][entity_x] = 'S' if entity.get_job() == BeeJob.Scout else 'B'
                else:
                    self.__world_map[entity_y][entity_x] = 's' if entity.get_job() == BeeJob.Scout else 'b'
            elif entity_type == EntityType.Food:
                self.__world_map[entity_y][entity_x] = 'F'
            elif entity_type == EntityType.Hive:
                self.__world_map[entity_y][entity_x] = 'H'
            else:
                raise ValueError("Unknown entity type")

    def run(self, max_iterations):
        """
        Run the simulation for a given number of iterations.
        :param max_iterations:
        :return:
        """
        for iteration in range(max_iterations):
            self.__hive.forage()

            self.update_world_map()
            Animator.print_world_status(world_map=self.__world_map, found=len(self.__hive.found_food_sources),
                                        total=self.__n_food_sources, food_at_hive=self.__hive.food_at_hive)

            self.__world_map = [['-' for _ in range(self.__width)] for _ in range(self.__height)]

            if len(self.__hive.found_food_sources) == self.__n_food_sources:
                print(f'All food sources found! In {iteration} iterations')

from ..Animator import Animator
from ..Bee import BeeJob
from .Entity import EntityType


class World:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__entities = []

        self.__hive = None
        self.__food_sources = []

        self.__unclaimed_food_sources = []
        self.__n_fod_sources = 0

        self.__world_map = [['-' for _ in range(width)] for _ in range(height)]

    def add_food_source(self, food_source):
        self.__unclaimed_food_sources.append(food_source)
        self.__n_fod_sources += 1

    def get_unclaimed_food_sources(self):
        return self.__unclaimed_food_sources

    def add_entity(self, entity):
        self.__entities.append(entity)
        if entity.get_type() == EntityType.Hive:
            self.__hive = entity
        elif entity.get_type() == EntityType.Food:
            if entity not in self.__food_sources:
                self.__food_sources.append(entity)

    def is_position_blocked(self, x, y):
        for entity in self.__entities:
            if entity.x == x and entity.y == y:
                return True
        return False

    def update_world_map(self):
        for entity in self.__entities:
            entity_type = entity.get_type()
            entity_x = entity.get_x()
            entity_y = entity.get_y()
            if entity_type == EntityType.Bee:
                if entity.has_found_food():
                    self.__world_map[entity_x][entity_y] = 'S' if entity.get_job() == BeeJob.Scout else 'B'
                else:
                    self.__world_map[entity_x][entity_y] = 's' if entity.get_job() == BeeJob.Scout else 'b'
            elif entity_type == EntityType.Food:
                self.__world_map[entity_x][entity_y] = 'F'
            elif entity_type == EntityType.Hive:
                self.__world_map[entity_x][entity_y] = 'H'
            else:
                raise ValueError("Unknown entity type")

    def run(self, max_iterations):
        for iteration in range(max_iterations):
            self.__hive.forage()

            self.update_world_map()
            Animator.print_world_status(world_map=self.__world_map, found=len(self.__hive.found_food_sources),
                                        total=self.__n_fod_sources)

            self.__world_map = [['-' for _ in range(self.__width)] for _ in range(self.__height)]

            if len(self.__hive.found_food_sources) == self.__n_fod_sources:
                print(f'All food sources found! In {iteration} iterations')
                return

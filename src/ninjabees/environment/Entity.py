from enum import Enum


class EntityType(Enum):
    Bee = 0
    Hive = 1
    Food = 2


class Entity:

    def __init__(self, x, y, type):
        self.__x = x
        self.__y = y
        self.__type = type

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_type(self):
        return self.__type

    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

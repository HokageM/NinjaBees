from enum import Enum


class EntityType(Enum):
    Bee = 0
    Hive = 1
    Food = 2


class Entity:
    """
    This class represents an entity in the world.
    """

    def __init__(self, x, y, type):
        self.__x = x
        self.__y = y
        self.__type = type

    def get_x(self):
        """
        Get the x coordinate of the entity.
        :return:
        """
        return int(self.__x)

    def get_y(self):
        """
        Get the y coordinate of the entity.
        :return:
        """
        return int(self.__y)

    def get_type(self):
        """
        Get the type of the entity.
        :return:
        """
        return self.__type

    def set_x(self, x):
        """
        Set the x coordinate of the entity.
        :param x:
        :return:
        """
        self.__x = x

    def set_y(self, y):
        """
        Set the y coordinate of the entity.
        :param y:
        :return:
        """
        self.__y = y

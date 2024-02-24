import os
import time


class Animator:
    """
    Class to handle the animation of the world map.
    """

    def __init__(self):
        pass

    @staticmethod
    def clear_terminal():
        """
        Clear the terminal.
        :return:
        """
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def print_world_status(world_map, found, total, food_at_hive):
        """
        Print the status of the world map.
        :param world_map:
        :param found:
        :param total:
        :return:
        """
        Animator.clear_terminal()
        for row in world_map:
            print(''.join(row))

        print(f'Found Food Sources: {found} of {total}')
        print(f'Food at Hive: {food_at_hive}')
        time.sleep(0.09)

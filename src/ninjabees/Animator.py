import os
import time


class Animator:
    def __init__(self):
        pass

    @staticmethod
    def clear_terminal():
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def print_hive_status(hive):
        Animator.clear_terminal()
        for row in hive.map:
            print(''.join(row))
        print(f'Found Food Sources: {len(hive.found_food_sources)} of {len(hive.food_sources)}')

        hive.map = [['-' for _ in range(200)] for _ in range(90)]
        hive.map[hive.x][hive.y] = 'H'
        time.sleep(0.09)
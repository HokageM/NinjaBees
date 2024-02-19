import os
import time


class Animator:
    def __init__(self):
        pass

    @staticmethod
    def clear_terminal():
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def print_world_status(world_map, found, total):
        Animator.clear_terminal()
        for row in world_map:
            print(''.join(row))

        print(f'Found Food Sources: {found} of {total}')
        time.sleep(0.09)

import argparse
import sys
import random

from .environment.World import World
from .Hive import Hive
from .FoodSource import FoodSource

from ninjabees import __version__

__author__ = "HokageM"
__copyright__ = "HokageM"
__license__ = "MIT"


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Simulation of a bee colony using the bee colony optimization algorithm.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"NinjaBees {__version__}",
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)

    food1 = FoodSource("Flower", 80, int(random.uniform(0, 89)), int(random.uniform(0, 199)))
    food2 = FoodSource("Tree", 10, int(random.uniform(0, 89)), int(random.uniform(0, 199)))
    food3 = FoodSource("Garden", 100, int(random.uniform(0, 89)), int(random.uniform(0, 199)))
    food4 = FoodSource("Flower 2", 88, int(random.uniform(0, 89)), int(random.uniform(0, 199)))
    food5 = FoodSource("Tree 2", 77, int(random.uniform(0, 89)), int(random.uniform(0, 199)))
    food6 = FoodSource("Garden 2", 300, int(random.uniform(0, 89)), int(random.uniform(0, 199)))

    world = World(200, 90)

    world.add_food_source(food1)
    world.add_food_source(food2)
    world.add_food_source(food3)
    world.add_food_source(food4)
    world.add_food_source(food5)
    world.add_food_source(food6)

    hive = Hive("MyHive", num_onlooker_bees=1, x=int(random.uniform(0, 89)), y=int(random.uniform(0, 199)), world=world)
    world.add_entity(hive)
    for bee in hive.bee_population:
        world.add_entity(bee)

    world.run(1000000)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

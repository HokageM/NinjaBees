import argparse
import sys
import random

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

    # Example usage
    hive = Hive("MyHive", num_onlooker_bees=1, x=int(random.uniform(0, 89)), y=int(random.uniform(0, 199)))

    food1 = FoodSource("Flower", 80, int(random.uniform(0, 89)), int(random.uniform(0, 199)))
    food2 = FoodSource("Tree", 10, int(random.uniform(0, 89)), int(random.uniform(0, 199)))
    food3 = FoodSource("Garden", 100, int(random.uniform(0, 89)), int(random.uniform(0, 199)))
    food4 = FoodSource("Flower 2", 88, int(random.uniform(0, 89)), int(random.uniform(0, 199)))
    food5 = FoodSource("Tree 2", 77, int(random.uniform(0, 89)), int(random.uniform(0, 199)))
    food6 = FoodSource("Garden 2", 300, int(random.uniform(0, 89)), int(random.uniform(0, 199)))

    # random int in range [a, b]: int(random.uniform(a, b))
    x = int(random.uniform(0, 199))

    hive.add_food_source(food1)
    hive.add_food_source(food2)
    hive.add_food_source(food3)
    hive.add_food_source(food4)
    hive.add_food_source(food5)
    hive.add_food_source(food6)

    hive.forage(max_iterations=10000)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

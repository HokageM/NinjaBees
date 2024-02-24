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

    foods = [FoodSource("Food", int(random.uniform(0, 300)), int(random.uniform(0, 199)),
                        int(random.uniform(0, 89))) for _ in range(30)]

    world = World(200, 90)

    for food in foods:
        world.add_food_source(food)

    hive = Hive("MyHive", num_onlooker_bees=1, x=int(random.uniform(0, 199)), y=int(random.uniform(0, 89)), world=world)
    world.add_entity(hive)
    for bee in hive.bee_population:
        world.add_entity(bee)

    world.run(1000000)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

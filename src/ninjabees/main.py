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
    parser.add_argument('--world-width',
                        type=int,
                        default=200,
                        help='Width of the environment.')
    parser.add_argument('--world-height',
                        type=int,
                        default=90,
                        help='Height of the environment.')
    parser.add_argument('--number-bees',
                        type=int,
                        default=900,
                        help='Number of bees in the environment.')
    parser.add_argument('--max-cnt-foraging-bees',
                        type=int,
                        default=700,
                        help='The maximum count of foraging bees.')
    parser.add_argument('--number-food-sources',
                        type=int,
                        default=30,
                        help='Number of food sources in the environment.')
    parser.add_argument('--best-nutrition-score',
                        type=int,
                        default=300,
                        help='The best nutrition score in the environment.')
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)

    foods = [FoodSource(int(random.uniform(0, args.best_nutrition_score)),
                        int(random.uniform(0, args.world_width - 1)),
                        int(random.uniform(0, args.world_height - 1))) for _ in range(args.number_food_sources)]

    world = World(args.world_width, args.world_height)

    for food in foods:
        world.add_food_source(food)

    hive_x = int(random.uniform(0, args.world_width - 1))
    hive_y = int(random.uniform(0, args.world_height - 1))
    hive = Hive(num_bees=args.number_bees,
                max_cnt_foraging_bees=args.max_cnt_foraging_bees,
                x=hive_x,
                y=hive_y,
                world=world)

    world.add_entity(hive)
    for bee in hive.bee_population:
        world.add_entity(bee)

    world.run(1000000)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

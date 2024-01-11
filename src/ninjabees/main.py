import argparse
import sys

from BeeColony import BeeColony

#from ninjabees import __version__

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
    parser = argparse.ArgumentParser(description="Implementation of the Bee Colony Algorithm.")
    parser.add_argument(
        "--version",
        action="version",
        #version=f"NinjaBees {__version__}",
    )
    return parser.parse_args(args)


def main(args):
    args = parse_args(args)

    # Example usage
    num_iterations = 10000
    num_bees = 50
    solution_size = 2
    learning_rate = 0.6  # Adjusted learning_rate for exploration
    max_trials = 10

    bee_colony = BeeColony(max_trials=max_trials, learning_rate=learning_rate)

    best_solution, best_fitness = bee_colony.optimization(num_iterations, num_bees, solution_size)

    print("\nOptimal Solution:", best_solution)
    print("Optimal Fitness:", best_fitness)


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

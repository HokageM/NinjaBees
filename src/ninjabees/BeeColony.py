from Bee import Bee

import numpy as np


class BeeColony:
    def __init__(self, max_trials, learning_rate):
        self.__population = []
        self.__max_trials = max_trials
        self.__learning_rate = learning_rate

    def initialize_population(self, num_bees, solution_size):
        for _ in range(num_bees):
            solution = np.random.rand(solution_size)
            fitness = BeeColony.evaluate_solution(solution)
            bee = Bee(solution, fitness)
            self.__population.append(bee)

    def employed_bee_phase(self, bee):
        # Choose another employed bee randomly
        other_bee = np.random.choice([other for other in self.__population if other != bee])
        new_solution = bee.solution + self.__learning_rate * (
                bee.solution - other_bee.solution)  # Update based on another employed bee
        new_solution_fitness = BeeColony.evaluate_solution(new_solution)

        # Allow the bee to update its solution based on the other bee's information
        if new_solution_fitness < bee.fitness:
            bee.solution = new_solution
            bee.fitness = new_solution_fitness

    def onlooker_bee_phase(self):
        # Calculate probabilities for onlooker bees
        probabilities = np.array([1 / (1 + bee.fitness) for bee in self.__population])
        probabilities /= probabilities.sum()

        # Onlooker bee phase
        selected_bees_indices = np.random.choice(range(len(self.__population)), len(self.__population), p=probabilities)
        selected_bees = [self.__population[i] for i in selected_bees_indices]
        for bee in selected_bees:
            self.employed_bee_phase(bee)

    def scout_bee_phase(self, bee):
        # If a bee's solution hasn't improved for a certain number of trials, scout and explore a new solution
        if bee.fitness <= 0.0001:
            return
        if bee.trials > self.__max_trials:
            bee.solution = np.random.rand(len(bee.solution))
            bee.fitness = BeeColony.evaluate_solution(bee.solution)
            bee.trials = 0
        else:
            bee.trials += 1

    def optimization(self, num_iterations, num_bees, solution_size):
        self.initialize_population(num_bees, solution_size)

        for iteration in range(num_iterations):
            # Employed bee phase
            for bee in self.__population:
                self.employed_bee_phase(bee)

            # Onlooker bee phase
            self.onlooker_bee_phase()

            # Scout bee phase
            for bee in self.__population:
                self.scout_bee_phase(bee)

            # Display the best fitness in each iteration
            best_solution = min(self.__population, key=lambda x: x.fitness)
            print(f"Iteration {iteration + 1}: Best Solution = {best_solution.solution} "
                  f"Best Fitness = {best_solution.fitness}")

        # Return the best solution found
        best_solution = min(self.__population, key=lambda x: x.fitness)
        return best_solution.solution, best_solution.fitness

    @staticmethod
    def evaluate_solution(solution):
        # Rosenbrock's Function parameters
        a = 1
        b = 100

        x = solution[0]
        y = solution[1]

        # Rosenbrock's Function formula
        value = (a - x) ** 2 + b * (y - x ** 2) ** 2

        return value

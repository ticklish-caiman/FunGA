import numpy as np

from utils.genetic.operators import mutation, tournament_selection, crossover, calculate_fitness_stats, apply_elitism


def evolve(population, generations=300, elitism_rate=0.5):
    for _ in range(generations):

        num_elites = int(elitism_rate * len(population))
        new_population = apply_elitism(population, num_elites)

        # Generate the rest of the new population (crossover/mutation)
        for _ in range(len(population) - num_elites):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            offspring = crossover(parent1, parent2)
            new_population.append(mutation(offspring))

        population = new_population  # Replace old population

        print(calculate_fitness_stats(population))
    return population

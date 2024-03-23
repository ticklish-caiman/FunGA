import numpy as np

from utils.genetic.operators import mutation, tournament_selection, crossover, calculate_fitness_stats, apply_elitism, \
    roulette_selection


def evolve(population, generations=600, elitism_rate=0.1):
    for _ in range(generations):

        num_elites = int(elitism_rate * len(population))
        new_population = apply_elitism(population, num_elites)

        # Generate the rest of the new population (crossover/mutation)
        for _ in range(len(population) - num_elites):
            # parent1 = tournament_selection(population)
            # parent2 = tournament_selection(population)
            parent1 = roulette_selection(population)
            parent2 = roulette_selection(population)
            offspring = crossover(parent1, parent2)
            new_population.append(mutation(offspring))

        population = new_population  # Replace old population

        print(calculate_fitness_stats(population))
    return population

# Best so far: 0.09291720443317986

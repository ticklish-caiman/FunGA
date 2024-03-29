import random

import numpy as np


def calculate_population_fitness(population):
    for i, biomorph in enumerate(population):
        if biomorph.chosen_one:
            chosen_one_index = i
    for biomorph in population:
        if not biomorph.chosen_one:
            fitness_scores = []
            total_difference = 0
            for gene_name, gene_value in biomorph.genes.items():
                if type(gene_value) is int:
                    # print('gene_name:', gene_name, 'gene_value:', gene_value)
                    total_difference += abs(gene_value - population[chosen_one_index].genes[gene_name])
                    try:
                        fitness_scores.append(1 / total_difference)  # Lower difference -> higher fitness
                    except ZeroDivisionError:
                        fitness_scores.append(1)
            biomorph.fitness = sum(fitness_scores) / len(fitness_scores)
        else:
            biomorph.fitness = 1.0
    return population


def apply_elitism(population, num_elites=1):
    # Evaluate fitness and find elites
    fitness_scores = [calculate_population_fitness(x) for x in population]
    elite_indices = np.argsort(fitness_scores)[-num_elites:]

    # Create a new population, starting with the elites
    new_population = [population[i] for i in elite_indices]

    return new_population


def tournament_selection(population, tournament_size=9):
    if population[0].fitness is None:
        population = calculate_population_fitness(population)
    # Sample indices of participants
    participant_indices = random.sample(range(len(population)), tournament_size)
    print('participant_indices', participant_indices)
    # Get fitness scores of participants
    fitness_scores = [population[i].fitness for i in participant_indices]
    print('fitness scores: ', fitness_scores)
    # Index of the winner (the highest fitness)
    winner_index = participant_indices[np.argmax(fitness_scores)]
    print('winner_index: ', winner_index)
    return population[winner_index]


def roulette_selection(population):
    fitness_scores = [calculate_population_fitness(x) for x in population]
    score_sum = np.sum(fitness_scores)  # Use NumPy's sum for efficiency
    wheel_sum = 0.0
    choice = np.random.uniform(0.0, 1.0)

    for i, individual in enumerate(population):
        wheel_sum += (fitness_scores[i] / score_sum)
        if wheel_sum >= choice:
            return individual

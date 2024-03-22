import random
import scipy.stats
import numpy as np


def calculate_fitness(array):
    entropy = scipy.stats.entropy(array.flatten())
    fitness = 1 / (entropy + 1)  # Lower entropy -> higher fitness
    return fitness


def calculate_average_fitness(population):
    total_fitness = sum(calculate_fitness(array) for array in population)
    return total_fitness / len(population)


def tournament_selection(population, tournament_size=10):
    # Sample indices of participants
    participant_indices = random.sample(range(len(population)), tournament_size)

    # Get fitness scores of participants
    fitness_scores = [calculate_fitness(population[i]) for i in participant_indices]

    # Index of the winner (the highest fitness)
    winner_index = np.argmax(fitness_scores)
    return population[winner_index]


def mutation(array, mutation_rate=0.01):
    # Create a mutation mask
    mutation_mask = np.random.rand(*array.shape) < mutation_rate

    # Invert pixels based on the mask
    array[mutation_mask] = ~array[mutation_mask]

    return array


def crossover(individual1, individual2):
    # Ensure arrays have the same shape
    assert individual1.shape == individual2.shape

    # Choose a random crossover point
    crossover_point_x = random.randint(0, individual1.shape[0] - 1)
    crossover_point_y = random.randint(0, individual1.shape[1] - 1)

    # Create offspring
    offspring = np.copy(individual1)  # Start with a copy of individual1

    # Perform crossover (swap portions of the arrays)
    offspring[:crossover_point_x, :crossover_point_y] = individual2[:crossover_point_x, :crossover_point_y]

    return offspring

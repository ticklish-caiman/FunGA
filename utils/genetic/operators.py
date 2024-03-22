import random
import scipy.stats
import numpy as np


def calculate_fitness(array):
    entropy = scipy.stats.entropy(array.flatten())
    fitness = 1 / (entropy + 1)  # Lower entropy -> higher fitness
    print(fitness)
    return fitness


def tournament_selection(population, tournament_size=10):
    # Sample indices of participants
    participant_indices = random.sample(range(len(population)), tournament_size)

    # Get fitness scores of participants
    fitness_scores = [calculate_fitness(population[i]) for i in participant_indices]

    # Index of the winner (the highest fitness)
    winner_index = np.argmax(fitness_scores)
    return population[winner_index]


def mutation(array, mutation_rate=0.1):
    # Create a mutation mask
    mutation_mask = np.random.rand(*array.shape) < mutation_rate

    # Invert pixels based on the mask
    array[mutation_mask] = ~array[mutation_mask]

    return array


def crossover(individual1, individual2):
    # Ensure arrays have the same shape
    assert individual1.shape == individual2.shape

    # Create a crossover mask
    crossover_mask = np.random.rand(*individual1.shape) < 0.5

    # Extract indices where the mask is True
    crossover_indices = np.where(crossover_mask)

    # Perform crossover using the indices
    for x, y in zip(*crossover_indices):  # Unpacking indices
        individual1[x][y] = individual2[x][y]

    return individual1

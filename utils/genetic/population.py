import random
import numpy as np

from utils.genetic.genes import get_binary_array_circle_cutout, get_binary_array_circle, get_binary_biased_array_random


def init_population(population_size):
    population = []
    for _ in range(population_size - 2):
        array = get_binary_biased_array_random([0.25, 0.5, 0.75])

        population.append(array)
    population.append(np.array(get_binary_array_circle_cutout(), dtype=bool))
    population.append(np.array(get_binary_array_circle(), dtype=bool))
    return population

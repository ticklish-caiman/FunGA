import random
import numpy as np


def init_population(population_size):
    population = []
    for _ in range(population_size):
        array = np.array([[random.randint(0, 1) for x in range(200)]
                          for y in range(200)], dtype=bool)  # Create the 2D array directly
        population.append(array)
    return population

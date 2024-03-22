import random


def init_population(population_size):
    # init population
    arrays = [None] * population_size
    for x in range(population_size):
        arrays[x] = [[random.randint(0, 1) for x in range(200)]  # Random 0s and 1s
                     for y in range(200)]
    return arrays

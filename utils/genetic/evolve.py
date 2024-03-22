import random

from utils.genetic.operators import mutation
from utils.genetic.population import init_population


def evolve(population, generations=30):
    arrays = population
    # evolve
    for _ in range(generations):
        for x in population:
            random.shuffle(arrays)
            x = mutation(x)
    return arrays

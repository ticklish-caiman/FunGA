import random

from utils.genetic.operators import mutation
from utils.genetic.population import init_population


def evolve(population, generations=30):
    # evolve
    for _ in range(generations):
        for x in population:
            random.shuffle(population)
            mutation(x)
    return population

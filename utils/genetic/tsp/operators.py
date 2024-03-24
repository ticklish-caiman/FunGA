import math
import random
from utils.genetic.tsp.genes import cities


# Fitness function: total distance
def route_distance(route):
    distance = 0
    for i in range(len(route)):
        c1 = cities[route[i]]
        c2 = cities[route[i - 1]]
        distance += math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
    return distance


# Selection (tournament)
def tournament_selection(population, tournament_size):
    parents = []
    for _ in range(2):  # Select two parents
        tournament = random.sample(population, tournament_size)
        parents.append(min(tournament, key=route_distance))
    return parents


# Crossover (Order Crossover)
def order_crossover(parent1, parent2):
    p1_slice = random.sample(range(len(parent1)), 2)
    start, end = min(p1_slice), max(p1_slice)

    child = parent1[start:end]
    remaining = [city for city in parent2 if city not in child]
    child = remaining[:start] + child + remaining[start:]
    return child


# Mutation (swap)
def swap_mutation(route, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]

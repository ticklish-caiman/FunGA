import math
import random


# Fitness function: total distance
def route_distance(route: list, cities: list) -> float:
    distance = 0
    for i in range(len(route)):
        c1 = cities[route[i]]
        c2 = cities[route[i - 1]]
        distance += math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)
    return distance


# Selection (tournament)
def tournament_selection(population: list, tournament_size: int, cities: list) -> list:
    parents = []
    for _ in range(2):  # Select two parents
        tournament = random.sample(population, tournament_size)
        parents.append(min(tournament, key=lambda route: route_distance(route, cities)))
    return parents


# Crossover (Order Crossover)
def order_crossover(parent1: list, parent2: list) -> list:
    p1_slice = random.sample(range(len(parent1)), 2)
    start, end = min(p1_slice), max(p1_slice)

    child = parent1[start:end]
    remaining = [city for city in parent2 if city not in child]
    child = remaining[:start] + child + remaining[start:]
    return child


# Mutation (swap)
def swap_mutation(route: list, mutation_rate: float):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]


def coordinates_to_permutation(user_roads, cities):
    permutation = []
    for segment in user_roads:
        start_city_index = cities.index(segment[0])  # Find index directly
        end_city_index = cities.index(segment[1])

        # Check if a city appears twice
        if start_city_index not in permutation:
            permutation.append(start_city_index)
        if end_city_index not in permutation:
            permutation.append(end_city_index)

    return permutation

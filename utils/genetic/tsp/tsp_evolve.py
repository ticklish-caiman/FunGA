import random
from typing import List

from utils.genetic.tsp.tsp_genes import cities
from utils.genetic.tsp.tsp_operators import tournament_selection, order_crossover, swap_mutation, route_distance
from utils.genetic.tsp.tsp_phenotype import plot_route


# Initialize population
def create_population(pop_size: int, city_count: int) -> List:
    pop = []
    # Generate a random permutations (travel routes)
    for _ in range(pop_size):
        pop.append(random.sample(range(city_count), city_count))
    return pop


def evolve(population: list, generations: int = 1000, tournament_size: int = 5, mutation_rate: float = 0.5) -> List:
    best_distance = float('inf')
    population_size = len(population)
    for i in range(generations):
        new_population = []
        for _ in range(int(population_size / 2)):  # Create offspring
            parents = tournament_selection(population, tournament_size)
            child1 = order_crossover(*parents)
            child2 = order_crossover(*parents)
            swap_mutation(child1, mutation_rate)
            swap_mutation(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population
        best_route = min(population, key=route_distance)
        current_distance = route_distance(best_route)
        # Plot at the end
        if i == generations - 1:
            best_route = min(population, key=route_distance)
            plot_route(best_route, i, cities)
            print("Plotting progress at iteration:", i, " (", round(i / generations * 100, 1),
                  "% )")  # Show progress percentage

        # Plot and update if there's an improvement, but not more often than 5% of total progress
        if (i % (generations // 20) == 0) and (current_distance < best_distance):
            best_distance = current_distance
            plot_route(best_route, i, cities)
            print("Plotting progress at iteration:", i, " (", round(i / generations * 100, 1),
                  "% )")  # Show progress percentage

    best_route = min(population, key=route_distance)
    print(f"Best route: {best_route}")
    print(f"Distance: {route_distance(best_route)}")

    return population


evolve(create_population(50, len(cities)), 1000)

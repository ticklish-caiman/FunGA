import random

from utils.genetic.tsp.tsp_operators import tournament_selection, order_crossover, swap_mutation, route_distance
from utils.genetic.tsp.tsp_phenotype import plot_route


# Initialize population
def create_population(pop_size: int, city_count: int) -> list:
    pop = []
    # Generate a random permutations (travel routes)
    for _ in range(pop_size):
        pop.append(random.sample(range(city_count), city_count))
    return pop


def evolve(population: list, cities: list = None, generations: int = 1000, tournament_size: int = 5,
           mutation_rate: float = 0.5) -> tuple[list, list]:
    best_distance = float('inf')
    population_size = len(population)
    progress_plot_img = []
    for i in range(generations):
        new_population = []
        for _ in range(int(population_size / 2)):  # Create offspring
            parents = tournament_selection(population, tournament_size, cities)
            child1 = order_crossover(*parents)
            child2 = order_crossover(*parents)
            swap_mutation(child1, mutation_rate)
            swap_mutation(child2, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population
        best_route = min(population, key=lambda route: route_distance(route, cities))
        current_distance = route_distance(best_route, cities)
        # Plot at the end
        if i == generations - 1:
            best_route = min(population, key=lambda route: route_distance(route, cities))
            progress_plot_img.append(plot_route(best_route, i, cities))
            print("Plotting progress at iteration:", i, " (", round(i / generations * 100, 1),
                  "% )")  # Show progress percentage

        # Plot and update if there's an improvement, but not more often than 5% of total progress
        if (i % (generations // 20) == 0) and (current_distance < best_distance):
            best_distance = current_distance
            progress_plot_img.append(plot_route(best_route, i, cities))
            print("Plotting progress at iteration:", i, " (", round(i / generations * 100, 1),
                  "% )")  # Show progress percentage

    best_route = min(population, key=lambda route: route_distance(route, cities))
    print(f"Best route: {best_route}")
    print(f"Distance: {route_distance(best_route, cities)}")

    return population, progress_plot_img

import random
from utils.genetic.tsp.tsp_genes import cities
from utils.genetic.tsp.tsp_operators import tournament_selection, order_crossover, swap_mutation, route_distance
from utils.genetic.tsp.tsp_phenotype import plot_route


# Initialize population
def create_population(pop_size, city_count):
    pop = []
    for _ in range(pop_size):
        pop.append(random.sample(range(city_count), city_count))
    return pop


# Main GA loop
population_size = 50
generations = 10000
tournament_size = 3
mutation_rate = 0.1

population = create_population(population_size, len(cities))

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
    # Plotting
    if i % 300 == 0:  # Plot every 300 iterations
        best_route = min(population, key=route_distance)
        plot_route(best_route, i, cities)

best_route = min(population, key=route_distance)
print(f"Best route: {best_route}")
print(f"Distance: {route_distance(best_route)}")

from utils.genetic.shapevo.operators import tournament_selection, calculate_fitness_stats, apply_elitism, \
    multi_point_crossover, burst_mutation, \
    rotation_mutation, row_based_crossover, row_column_swap_mutation, diagonal_reflection_mutation


def evolve(population, generations=200, elitism_rate=0.1):
    for _ in range(generations):

        num_elites = int(elitism_rate * len(population))
        new_population = apply_elitism(population, num_elites)

        # Generate the rest of the new population (crossover/mutation)
        for _ in range(len(population) - num_elites):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            # parent1 = roulette_selection(population)
            # parent2 = roulette_selection(population)
            offspring = multi_point_crossover(parent1, parent2)
            new_population.append(
                diagonal_reflection_mutation(row_column_swap_mutation(rotation_mutation(burst_mutation(offspring)))))
            # new_population.append(offspring)

        population = new_population  # Replace old population

        print(calculate_fitness_stats(population))
    return population

# Best so far: 0.09291720443317986

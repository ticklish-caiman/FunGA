from utils.genetic.operators import mutation, tournament_selection, crossover, calculate_average_fitness, apply_elitism


def evolve(population, generations=4000):
    for _ in range(generations):
        for i in range(len(population)):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            offspring = crossover(parent1, parent2)
            population[i] = mutation(offspring)

        # Perform elitism after the regular generation cycle
        population = apply_elitism(population, elitism_rate=0.1)

        print(_, calculate_average_fitness(population))
    return population

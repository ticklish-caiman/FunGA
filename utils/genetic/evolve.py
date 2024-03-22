from utils.genetic.operators import mutation, tournament_selection, crossover


def evolve(population, generations=200):
    for _ in range(generations):
        for i in range(len(population)):  # Iterate over indices
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            offspring = crossover(parent1, parent2)
            population[i] = mutation(offspring)  # Replace old individual
    return population


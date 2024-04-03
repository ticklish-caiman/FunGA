from utils.genetic.shapevo_alternative.alt_shapevo_operators import tournament_selection, crossover, \
    mutate
from utils.genetic.shapevo_alternative.alt_shapevo_population import create_population


def evolve(population, generations=200, elitism_rate=0.1):
    for _ in range(generations):

        new_population = []
        fitness_scores = []
        for shape in population:
            if shape.genome is None:
                shape.generate_genome()
            if shape.rendered_image is None:
                shape.render_shape()
            if shape.fitness is None:
                shape.calculate_fitness()
            fitness_scores.append(shape.fitness)
        # Generate the rest of the new population (crossover/mutation)
        for _ in range(len(population)):
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)

            offspring = crossover(parent1, parent2)
            print("Offspring:", offspring)
            new_population.append(mutate(offspring))
            # new_population.append(offspring)

        population = new_population  # Replace old population

    return population


pop = create_population(6, 500, 500)
for individual in pop:
    individual.generate_genome()
    individual.render_shape()
    individual.display()

evolve(pop)

for individual in pop:
    individual.display()

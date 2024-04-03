from utils.genetic.shapevo_alternative.alt_shapevo_genes import Shape


def create_population(population_size, image_width, image_height):
    population = []
    for _ in range(population_size):
        shape = Shape(image_width, image_height)
        population.append(shape)
    return population

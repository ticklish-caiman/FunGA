import random

from utils.genetic.shapevo.genes import get_binary_array_circle_cutout, get_binary_array_circle, get_binary_biased_array_random, \
    get_binary_array_alternating_squares, get_array_and_not_array


def init_population(population_size):
    min_gene_generator = [get_binary_array_alternating_squares()]
    basic_gene_generator = [get_binary_array_circle_cutout(), get_binary_array_circle(),
                            get_binary_biased_array_random([0.25, 0.5, 0.75]), get_binary_array_alternating_squares()]
    advanced_gene_generator = [get_binary_array_circle_cutout(), get_binary_array_circle(),
                               get_binary_biased_array_random([0.25, 0.5, 0.75]),
                               get_binary_array_alternating_squares(),
                               get_array_and_not_array(random.choice(basic_gene_generator),
                                                       random.choice(basic_gene_generator))]
    population = []
    for _ in range(population_size):
        array = random.choice(advanced_gene_generator)
        #array = get_binary_array_alternating_squares()

        population.append(array)
    return population

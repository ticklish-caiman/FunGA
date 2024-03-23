import random
import numpy as np

from utils.genetic.genes import get_binary_array_circle_cutout, get_binary_array_circle


def init_population(population_size):
    population = []
    for _ in range(population_size - 2):
        # Determine a random white pixel ratio
        white_pixel_ratio = random.choice([0.25, 0.5, 0.75])

        # Biased array generation
        array = np.zeros((200, 200), dtype=bool)  # Start with all zeros (black)
        num_white_pixels = int(white_pixel_ratio * 200 * 200)  # Desired number
        white_indices = random.sample(range(40000), num_white_pixels)  # Unique indices
        array.flat[white_indices] = True  # Efficiently set as white

        population.append(array)
    population.append(np.array(get_binary_array_circle_cutout(), dtype=bool))
    population.append(np.array(get_binary_array_circle(), dtype=bool))
    return population

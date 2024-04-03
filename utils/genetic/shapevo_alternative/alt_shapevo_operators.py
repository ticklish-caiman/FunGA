import logging
import random

import cv2
import numpy as np

from utils.genetic.shapevo_alternative.alt_shapevo_genes import Shape

logging.basicConfig(level=logging.INFO)



def tournament_selection(population, fitness_scores, tournament_size=3):
    # Select `tournament_size` random participants
    logging.info("Tournament selection")
    logging.info("Population size:" + str(len(population)))
    logging.info("Touching tournament size: " + str(tournament_size))
    participants = random.sample(range(len(population)), tournament_size)

    # Find the index of the fittest participant
    best_index = np.argmax([fitness_scores[i] for i in participants])

    # Return the best genome
    return population[participants[best_index]]


def crossover(parent1: Shape, parent2: Shape):
    genome1 = parent1.genome
    genome2 = parent2.genome
    # Two-point crossover
    if len(genome1) <= 2 or len(genome2) <= 2:
        logging.warning("Genomes are too small for a safe crossover; just return parent")
        return parent1

        # Ensure crossover points allow at least one shape from each parent to be exchanged
    max_crossover_point1 = max(1, min(len(genome1) - 2, len(genome2) - 2))
    min_crossover_point2 = min(len(genome1) - 1, len(genome2) - 1)

    crossover_point1 = random.randint(1, max_crossover_point1)
    crossover_point2 = random.randint(crossover_point1 + 1, min_crossover_point2)

    # Perform the crossover
    if random.random() < 0.5:
        offspring_genome = genome1[:crossover_point1] + genome2[crossover_point1:crossover_point2] + genome1[
                                                                                                     crossover_point2:]
    else:
        offspring_genome = genome2[:crossover_point1] + genome1[crossover_point1:crossover_point2] + genome2[
                                                                                                     crossover_point2:]
    offspring = Shape(parent1.image_width, parent1.image_height, parent1.max_num_shapes)
    offspring.genome = offspring_genome

    return offspring


def mutate(shape):
    genome = shape.genome
    if random.random() < 0.5:  # 50% chance to mutate a shape
        shape_to_mutate = random.choice(genome)

        if shape_to_mutate['type'] == 'circle':
            shape_to_mutate['center_x'] += random.randint(-10, 10)  # Adjust center
            shape_to_mutate['center_y'] += random.randint(-10, 10)
            shape_to_mutate['radius'] += random.randint(-5, 5)  # Adjust radius
            # ... (make sure the shape stays within the image bounds)
        else:  # 'rectangle'
            # ... mutations for rectangle parameters
            pass
    return shape
    # ... (add/delete or shape type change mutations here)

import random

import numpy as np
from PIL import ImageDraw, Image

from utils.genetic.shapevo.shapevo_operators import tournament_selection, calculate_fitness_stats, apply_elitism, \
    multi_point_crossover, burst_mutation, \
    rotation_mutation, row_based_crossover, row_column_swap_mutation, diagonal_reflection_mutation, crossover


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
            offspring = crossover(parent1, parent2)
            new_population.append(
                diagonal_reflection_mutation(row_column_swap_mutation(rotation_mutation(burst_mutation(offspring)))))
            # new_population.append(offspring)

        population = new_population  # Replace old population

        print(calculate_fitness_stats(population))
    return population


# Best so far: 0.09291720443317986

def generate_genome(image_width, image_height, max_num_shapes=5):
    genome = []
    num_shapes = random.randint(1, max_num_shapes)
    for _ in range(num_shapes):
        shape_type = random.choice(['circle', 'rectangle'])
        center_x = random.randint(0, image_width - 1)
        center_y = random.randint(0, image_height - 1)

        if shape_type == 'circle':
            # Ensure radius fits within image bounds
            max_radius = min(center_x, center_y, image_width - center_x, image_height - center_y)
            radius = random.randint(10, max_radius)
            shape_params = {'type': shape_type, 'center_x': center_x, 'center_y': center_y, 'radius': radius}
        else:
            width = random.randint(20, image_width // 3)  # Adjust ratios as needed
            height = random.randint(20, image_height // 3)
            shape_params = {'type': shape_type, 'center_x': center_x, 'center_y': center_y, 'width': width,
                            'height': height}

        genome.append(shape_params)

    return genome


def draw_circle(image, center_x, center_y, radius, color=0):
    draw = ImageDraw.Draw(image)
    bbox = (center_x - radius, center_y - radius, center_x + radius, center_y + radius)
    draw.ellipse(bbox, fill=color)


def draw_rectangle(image, center_x, center_y, width, height, color=0):
    draw = ImageDraw.Draw(image)
    bbox = [(center_x - width // 2, center_y - height // 2),
            (center_x + width // 2, center_y + height // 2)]
    draw.rectangle(bbox, fill=color)


def generate_image(genome):
    image = Image.new("L", (500, 500), color=255)  # Black background, "L" mode for grayscale

    for shape_params in genome:
        if shape_params['type'] == 'circle':
            draw_circle(image,
                        shape_params['center_x'], shape_params['center_y'],
                        shape_params['radius'])
        elif shape_params['type'] == 'rectangle':
            draw_rectangle(image,
                           shape_params['center_x'], shape_params['center_y'],
                           shape_params['width'], shape_params['height'])

    return image


generate_image(generate_genome(500, 500, 2)).show()

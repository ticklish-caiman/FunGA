import random

import numpy as np


def get_binary_array_grid_pattern():
    return [[1 if x % 10 == 0 or y % 10 == 0 else 0
             for x in range(200)]
            for y in range(200)]


def get_binary_array_alternating_squares():
    return [[1 if (x + y) % 2 == 0 else 0
             for x in range(200)]
            for y in range(200)]


def get_binary_array_circle():
    return [[1 if (x - 100) ** 2 + (y - 100) ** 2 <= 40 ** 2 else 0
             for x in range(200)]
            for y in range(200)]


def get_binary_array_random():
    return [[random.randint(0, 1) for x in range(200)]
            for y in range(200)]


def get_binary_biased_array_random(white_pixel_ratios=[0.25, 0.5, 0.75]):
    white_pixel_ratio = random.choice(white_pixel_ratios)

    # Biased array generation
    array = np.zeros((200, 200), dtype=bool)  # Start with all zeros (black)
    num_white_pixels = int(white_pixel_ratio * 200 * 200)  # Desired number
    white_indices = random.sample(range(40000), num_white_pixels)  # Unique indices
    array.flat[white_indices] = True  # Efficiently set as white
    return array


def get_binary_array_circle_cutout():  # Notice the change for cutout
    return [[0 if (x - 100) ** 2 + (y - 100) ** 2 <= 50 ** 2 else 1
             for x in range(200)]
            for y in range(200)]


def get_array_and_not_array(array1, array2):
    # Combine patterns (array1 AND NOT array2)
    return [[array1[y][x] and not array2[y][x] for x in range(200)]
            for y in range(200)]

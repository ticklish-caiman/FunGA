import random
import scipy.stats
import numpy as np
from scipy.ndimage import label


# def calculate_fitness(array):
#     entropy = scipy.stats.entropy(array.flatten())
#     fitness = 1 / (entropy + 1)  # Lower entropy -> higher fitness
#     return fitness

def calculate_fitness(array):
    entropy = scipy.stats.entropy(array.flatten())

    # Calculate a white pixel ratio (assuming white is 0 and black is 1)
    white_ratio = np.mean(array == 0)

    # Combine with a weighting factor (play around with this value)
    fitness = 0.8 * entropy + 0.2 * white_ratio

    return fitness


# def calculate_fitness(array, target_entropy=5.0):  # Example target
#     entropy = scipy.stats.entropy(array.flatten())
#     raw_fitness = 1 / (entropy + 1)
#
#     # Penalize if far from the target
#     distance_from_target = abs(entropy - target_entropy)
#     if distance_from_target > 2.0:  # Adjust this threshold
#         raw_fitness *= 0.1  # Significant penalty
#
#     return raw_fitness


def calculate_fitness_stats(population):
    fitness_scores = [calculate_fitness(array) for array in population]
    average_fitness = sum(fitness_scores) / len(population)
    highest_fitness = max(fitness_scores)

    return average_fitness, highest_fitness


def apply_elitism(population, num_elites=1):
    # Evaluate fitness and find elites
    fitness_scores = [calculate_fitness(x) for x in population]
    elite_indices = np.argsort(fitness_scores)[-num_elites:]

    # Create a new population, starting with the elites
    new_population = [population[i] for i in elite_indices]

    return new_population


def tournament_selection(population, tournament_size=4):
    # Sample indices of participants
    participant_indices = random.sample(range(len(population)), tournament_size)

    # Get fitness scores of participants
    fitness_scores = [calculate_fitness(population[i]) for i in participant_indices]

    # Index of the winner (the highest fitness)
    winner_index = np.argmax(fitness_scores)
    return population[winner_index]


def roulette_selection(population):
    fitness_scores = [calculate_fitness(x) for x in population]
    score_sum = np.sum(fitness_scores)  # Use NumPy's sum for efficiency
    wheel_sum = 0.0
    choice = np.random.uniform(0.0, 1.0)

    for i, individual in enumerate(population):
        wheel_sum += (fitness_scores[i] / score_sum)
        if wheel_sum >= choice:
            return individual


def mutation(array, mutation_rate=0.01):
    # Create a mutation mask
    mutation_mask = np.random.rand(*array.shape) < mutation_rate

    # Invert pixels based on the mask
    array[mutation_mask] = ~array[mutation_mask]

    return array


def crossover(individual1, individual2):
    # Ensure arrays have the same shape
    assert individual1.shape == individual2.shape

    # Choose a random crossover point
    crossover_point_x = random.randint(0, individual1.shape[0] - 1)
    crossover_point_y = random.randint(0, individual1.shape[1] - 1)

    # Create offspring
    offspring = np.copy(individual1)  # Start with a copy of individual1

    # Perform crossover (swap portions of the arrays)
    offspring[:crossover_point_x, :crossover_point_y] = individual2[:crossover_point_x, :crossover_point_y]

    return offspring


def multi_point_crossover(individual1, individual2):
    # Ensure arrays have the same shape
    assert individual1.shape == individual2.shape

    num_crossover_points = 4
    crossover_points_x = random.sample(range(individual1.shape[0]), num_crossover_points)
    crossover_points_y = random.sample(range(individual1.shape[1]), num_crossover_points)

    offspring = np.copy(individual1)
    for i in range(num_crossover_points // 2):  # Alternate between parents
        start_x, end_x = crossover_points_x[2 * i: 2 * i + 2]
        start_y, end_y = crossover_points_y[2 * i: 2 * i + 2]
        offspring[start_x:end_x, start_y:end_y] = individual2[start_x:end_x, start_y:end_y]

    return offspring


def row_based_crossover(individual1, individual2):
    # Ensure arrays have the same shape
    assert individual1.shape == individual2.shape

    num_crossover_rows = random.randint(1, individual1.shape[0] // 2)
    crossover_rows = random.sample(range(individual1.shape[0]), num_crossover_rows)

    offspring = np.copy(individual1)
    for row_index in crossover_rows:
        offspring[row_index, :] = individual2[row_index, :]

    return offspring


def find_connected_regions(bool_array):
    # Identifies connected regions of True values in a Boolean array

    labeled_array, num_regions = label(bool_array)  # Efficient labeling

    # Create region masks
    region_masks = []
    for region_id in range(1, num_regions + 1):  # Region IDs start from 1
        mask = labeled_array == region_id
        region_masks.append(mask)

    return region_masks


def shape_based_crossover(individual1, individual2):
    assert individual1.shape == individual2.shape

    # Find connected regions
    blob_masks1 = find_connected_regions(individual1)
    blob_masks2 = find_connected_regions(individual2)

    # Select random blobs (Prioritizes larger blobs)
    blob_sizes1 = [np.sum(mask) for mask in blob_masks1]
    blob_sizes2 = [np.sum(mask) for mask in blob_masks2]

    selected_blob_index1 = random.choices(range(len(blob_masks1)), weights=blob_sizes1)[0]
    selected_blob_index2 = random.choices(range(len(blob_masks2)), weights=blob_sizes2)[0]

    blob_mask1 = blob_masks1[selected_blob_index1]
    blob_mask2 = blob_masks2[selected_blob_index2]

    # Create offspring
    offspring = np.copy(individual1)

    # Swap the selected regions between the parents
    offspring[blob_mask1] = individual2[blob_mask1]
    offspring[blob_mask2] = individual1[blob_mask2]

    return offspring

# def crossover(individual1, individual2):
#     # Ensure arrays have the same shape
#     assert individual1.shape == individual2.shape
#
#     # Choose a random crossover point
#     crossover_point_x = random.randint(0, individual1.shape[0] - 1)
#     crossover_point_y = random.randint(0, individual1.shape[1] - 1)
#
#     # Create offspring
#     offspring = np.copy(individual1)  # Start with a copy of individual1
#
#     # Perform crossover (swap portions of the arrays)
#     offspring[:crossover_point_x, :crossover_point_y] = individual2[:crossover_point_x, :crossover_point_y]
#
#     return offspring

# def extract_patches(image_array, patch_size=50):
#     patches = []
#     for y in range(0, image_array.shape[0], patch_size):
#         for x in range(0, image_array.shape[1], patch_size):
#             patch = image_array[y:y + patch_size, x:x + patch_size]
#             patches.append(patch)
#     return patches

# def tournament_selection(population, tournament_size=4):
#     """Selects an individual based on the highest patch fitness"""
#
#     participants = random.sample(population, tournament_size)
#
#     best_participant = None
#     highest_patch_fitness = -float('inf')
#
#     for participant in participants:
#         patches = extract_patches(participant)  # Extract patches
#         for patch in patches:
#             patch_fitness = calculate_fitness(patch)
#             if patch_fitness > highest_patch_fitness:
#                 highest_patch_fitness = patch_fitness
#                 best_participant = participant.copy()
#
#     return best_participant
#
#
# def crossover(individual1, individual2):
#     # Swaps corresponding patches between individuals
#     offspring = individual1.copy()
#     patches1 = extract_patches(individual1)
#     patches2 = extract_patches(individual2)
#
#     for i in range(len(patches1)):
#         if random.random() < 0.5:
#             y_start = i * 50
#             y_end = y_start + 50
#             x_start = i * 50
#             x_end = x_start + 50
#
#             # Ensure we don't go out of bounds
#             y_end = min(y_end, offspring.shape[0])
#             x_end = min(x_end, offspring.shape[1])
#
#             offspring[y_start:y_end, x_start:x_end] = patches2[i][0:y_end - y_start, 0:x_end - x_start].copy()
#
#     return offspring

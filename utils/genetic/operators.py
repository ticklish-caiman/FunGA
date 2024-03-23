import random
import scipy.stats
import numpy as np


def calculate_fitness(array):
    entropy = scipy.stats.entropy(array.flatten())
    fitness = 1 / (entropy + 1)  # Lower entropy -> higher fitness
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


# def tournament_selection(population, tournament_size=5):
#     # Sample indices of participants
#     participant_indices = random.sample(range(len(population)), tournament_size)
#
#     # Get fitness scores of participants
#     fitness_scores = [calculate_fitness(population[i]) for i in participant_indices]
#
#     # Index of the winner (the highest fitness)
#     winner_index = np.argmax(fitness_scores)
#     return population[winner_index]


def roulette_selection(population):
    fitness_scores = [calculate_fitness(x) for x in population]
    score_sum = np.sum(fitness_scores)  # Use NumPy's sum for efficiency
    wheel_sum = 0.0
    choice = np.random.uniform(0.0, 1.0)

    for i, individual in enumerate(population):
        wheel_sum += (fitness_scores[i] / score_sum)
        if wheel_sum >= choice:
            return individual


def mutation(array, mutation_rate=0.1):
    # Create a mutation mask
    mutation_mask = np.random.rand(*array.shape) < mutation_rate

    # Invert pixels based on the mask
    array[mutation_mask] = ~array[mutation_mask]

    return array


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

def extract_patches(image_array, patch_size=50):
    patches = []
    for y in range(0, image_array.shape[0], patch_size):
        for x in range(0, image_array.shape[1], patch_size):
            patch = image_array[y:y + patch_size, x:x + patch_size]
            patches.append(patch)
    return patches


def tournament_selection(population, tournament_size=4):
    """Selects an individual based on the highest patch fitness"""

    participants = random.sample(population, tournament_size)

    best_participant = None
    highest_patch_fitness = -float('inf')

    for participant in participants:
        patches = extract_patches(participant)  # Extract patches
        for patch in patches:
            patch_fitness = calculate_fitness(patch)
            if patch_fitness > highest_patch_fitness:
                highest_patch_fitness = patch_fitness
                best_participant = participant.copy()

    return best_participant


def crossover(individual1, individual2):
    # Swaps corresponding patches between individuals
    offspring = individual1.copy()
    patches1 = extract_patches(individual1)
    patches2 = extract_patches(individual2)

    for i in range(len(patches1)):
        if random.random() < 0.5:
            y_start = i * 50
            y_end = y_start + 50
            x_start = i * 50
            x_end = x_start + 50

            # Ensure we don't go out of bounds
            y_end = min(y_end, offspring.shape[0])
            x_end = min(x_end, offspring.shape[1])

            offspring[y_start:y_end, x_start:x_end] = patches2[i][0:y_end - y_start, 0:x_end - x_start].copy()

    return offspring

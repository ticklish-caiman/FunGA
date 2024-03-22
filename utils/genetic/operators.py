import random
import scipy.stats


def mutation(array):
    for x in range(len(array)):
        for y in range(len(array[x])):
            if random.random() < 0.2:
                array[x][y] = 1
    return array


def entropy_mutation(array, target_entropy=None):
    # TODO: other mutation operations like inversions, shifting, etc.

    # Entropy control
    current_entropy = scipy.stats.entropy(array.flatten())  # Flatten for entropy calculation
    print('Entropy: ', current_entropy)
    if target_entropy:
        entropy_diff = abs(target_entropy - current_entropy)
        if random.random() < entropy_diff:  # Mutation more likely if far from target
            # Add additional random changes here
            pass

    return array


def crossover(individual1, individual2):
    for x in range(len(individual1)):
        for y in range(len(individual1)):
            if random.random() < 0.5:
                individual1[x][y] = individual2[x][y]
    return individual1

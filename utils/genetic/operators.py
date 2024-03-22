import random


def mutation(array):
    for x in range(len(array)):
        for y in range(len(array[x])):
            if random.random() < 0.2:
                array[x][y] = 1
    return array


def crossover(individual1, individual2):
    for x in range(len(individual1)):
        for y in range(len(individual1)):
            if random.random() < 0.5:
                individual1[x][y] = individual2[x][y]
    return individual1

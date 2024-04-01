import random
from typing import List

import numpy as np

from utils.genetic.biomorphs.biomorphs_population import Biomorph

rng = np.random.default_rng(seed=42)


def mutation(biomorph: Biomorph, mutation_rate: float = 0.9) -> Biomorph:
    if random.random() < mutation_rate:
        for gene_name in biomorph.genes:
            if type(biomorph.genes[gene_name]) is int:
                if random.random() < 0.5:
                    biomorph.genes[gene_name] = biomorph.genes[gene_name] + int(0.3 * biomorph.genes[gene_name])
                else:
                    biomorph.genes[gene_name] = biomorph.genes[gene_name] - int(0.3 * biomorph.genes[gene_name])
    return biomorph


def arithmetic_crossover(biomorph1: Biomorph, biomorph2: Biomorph) -> Biomorph:
    """Performs arithmetic crossover between two biomorphs, generating a new gene dictionary."""

    offspring_genes = {}  # Create a dictionary for the offspring's genes

    for gene_name in biomorph1.genes:
        if type(biomorph1.genes[gene_name]) is int:
            average_gene = (biomorph1.genes[gene_name] + biomorph2.genes[gene_name]) // 2
            offspring_genes[gene_name] = average_gene
        if type(biomorph2.genes[gene_name]) is str:
            if random.random() < 0.5:
                offspring_genes[gene_name] = biomorph1.genes[gene_name]
            else:
                offspring_genes[gene_name] = biomorph2.genes[gene_name]
    offspring = Biomorph(size=biomorph1.size, genes=offspring_genes)
    offspring.color = random.choice([biomorph1.color, biomorph2.color])
    offspring.generate_biomorph()
    return offspring


def calculate_population_fitness(population: List[Biomorph]) -> List[Biomorph]:
    for i, biomorph in enumerate(population):
        if biomorph.chosen_one:
            chosen_one_index = i
    for biomorph in population:
        if not biomorph.chosen_one:
            fitness_scores = []
            total_difference = 0
            for gene_name, gene_value in biomorph.genes.items():
                if type(gene_value) is int:
                    total_difference += abs(gene_value - population[chosen_one_index].genes[gene_name]) ** 3
                    try:
                        fitness_scores.append(1 / total_difference)  # Lower difference -> higher fitness
                    except ZeroDivisionError:
                        fitness_scores.append(1)
            biomorph.fitness = sum(fitness_scores) / len(fitness_scores)
        else:
            biomorph.fitness = 1.0
    return population


def apply_elitism(population: List[Biomorph], num_elites=1) -> List[Biomorph]:
    # Evaluate fitness and find elites
    fitness_scores = [calculate_population_fitness(x) for x in population]
    elite_indices = np.argsort(fitness_scores)[-num_elites:]

    # Create a new population, starting with the elites
    new_population = [population[i] for i in elite_indices]

    return new_population


def tournament_selection(population: List[Biomorph], tournament_size: int = 3) -> List[Biomorph]:
    if population[0].fitness is None:
        population = calculate_population_fitness(population)
    # Sample indices of participants
    participant_indices = random.sample(range(len(population)), tournament_size)
    # Get fitness scores of participants
    fitness_scores = [population[i].fitness for i in participant_indices]
    # Index of the winner (the highest fitness)
    winner_index = participant_indices[np.argmax(fitness_scores)]
    return population[winner_index]


def roulette_selection(population):
    fitness_scores = [calculate_population_fitness(x) for x in population]
    score_sum = np.sum(fitness_scores)  # Use NumPy's sum for efficiency
    wheel_sum = 0.0
    choice = rng.uniform(0.0, 1.0)

    for i, individual in enumerate(population):
        wheel_sum += (fitness_scores[i] / score_sum)
        if wheel_sum >= choice:
            return individual

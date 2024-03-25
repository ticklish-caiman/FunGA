def calculate_fitness(population, chosen_biomorph):
    fitness_scores = []
    for biomorph in population:
        total_difference = 0
        for gene_name, gene_value in biomorph.genes.items():
            total_difference += abs(gene_value - chosen_biomorph.genes[gene_name])
        fitness_scores.append(1 / total_difference)  # Lower difference -> higher fitness
    return fitness_scores

from utils.genetic.biomorphs.genes import genes, generate_random_genes
from utils.genetic.biomorphs.phenotype import draw_biomorph
from utils.genetic.biomorphs.population import generate_biomorph


def evolve_biomorphs():
    return draw_biomorph(generate_biomorph(generate_random_genes()))

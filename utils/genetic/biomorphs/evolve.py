from utils.genetic.biomorphs.biomorphs_operators import calculate_population_fitness, tournament_selection
from utils.genetic.biomorphs.phenotype import draw_biomorph
from utils.genetic.biomorphs.population import Biomorph


def draw_biomorph():
    biomorph = Biomorph(size=(500, 500))
    biomorph.generate_biomorph()
    return draw_biomorph(biomorph)


def init_population(pop_size=10):
    biomorphs = []
    for i in range(pop_size):
        biomorph = Biomorph(size=(500, 500))
        biomorph.generate_biomorph()
        biomorphs.append(biomorph)
    return biomorphs


def evolve_biomrophs(population):
    # assume that 0 was chosen
    population[0].chosen_one = True
    calculate_population_fitness(population)
    for biomorph in population:
        print(biomorph.fitness)
    print("Winner:", tournament_selection(population).fitness)


def test_pass_choice(best):
    print(best)


pop = init_population()
evolve_biomrophs(pop)

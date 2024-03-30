from utils.genetic.biomorphs.biomorphs_operators import calculate_population_fitness, tournament_selection, \
    arithmetic_crossover, mutation
from utils.genetic.biomorphs.phenotype import draw_biomorph_pil
from utils.genetic.biomorphs.population import Biomorph


def draw_biomorph():
    biomorph = Biomorph(size=(500, 500))
    biomorph.generate_biomorph()
    return draw_biomorph_pil(biomorph)


def init_biomorphs_population(pop_size=10):
    biomorphs = []
    for i in range(pop_size):
        biomorph = Biomorph(size=(500, 500))
        biomorph.generate_biomorph()
        biomorphs.append(biomorph)
    return biomorphs


def evolve_biomrophs(population, chosen_one_index=0):
    population[chosen_one_index].chosen_one = True
    calculate_population_fitness(population)
    new_population = []
    for i in range(len(population)):
        new_population.append(mutation(arithmetic_crossover(tournament_selection(population), tournament_selection(population))))
    return new_population


def test_pass_choice(best):
    print(best)

# pop = init_biomorphs_population()
# evolve_biomrophs(pop)

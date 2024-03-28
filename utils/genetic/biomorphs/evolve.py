from utils.genetic.biomorphs.phenotype import draw_biomorph
from utils.genetic.biomorphs.population import Biomorph


def evolve_biomorphs():
    biomorph = Biomorph()
    biomorph.generate_biomorph()
    return draw_biomorph(biomorph)


def test_pass_choice(best):
    print(best)

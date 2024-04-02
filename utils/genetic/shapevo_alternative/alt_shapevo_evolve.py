from utils.genetic.shapevo_alternative.alt_shapevo_genes import generate_genome
from utils.genetic.shapevo_alternative.alt_shapevo_phenotype import generate_image

generate_image(generate_genome(500, 500, 25)).show()

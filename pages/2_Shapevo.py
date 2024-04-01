import streamlit as st

from utils.genetic.shapevo.shapevo_evolve import evolve
from utils.genetic.shapevo.shapevo_operators import calculate_fitness_return_all
from utils.genetic.shapevo.shapevo_phenotype import draw_image_from_array
from utils.genetic.shapevo.shapevo_population import init_population
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

st.header(_('Hello Evolving Shapes'))
col1, col2 = st.columns(2)
with col1:
    st.header("Initial population")
    population = init_population(20)
    for individual in population:
        entropy, white_ratio, fitness = calculate_fitness_return_all(individual)
        st.image(draw_image_from_array(individual),
                 caption=f"Entropy: {entropy:.4f}, White Ratio: {white_ratio:4f}, Fitness: {fitness:.4f}")
        # st.image(draw_image_from_array(rotation_mutation(individual.copy())),
        #          caption=f"Mutant")
with col2:
    evolved_population = evolve(population)
    st.header('Evolved population')
    for individual in evolved_population:
        entropy, white_ratio, fitness = calculate_fitness_return_all(individual)
        st.image(draw_image_from_array(individual),
                 caption=f"Entropy: {entropy:.4f}, White Ratio: {white_ratio:4f}, Fitness: {fitness:.4f}")

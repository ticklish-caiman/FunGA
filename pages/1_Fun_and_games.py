import math

import streamlit as st

from utils.genetic.evolve import evolve
from utils.genetic.operators import calculate_fitness_return_all, rotation_mutation
from utils.genetic.phenotype import draw_image_from_array
from utils.genetic.population import init_population
from utils.navigation import show_main_menu, get_localizator
import numpy as np

# from database.database_helper import DatabaseHelper

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

tabs_options = ["Shapevo", "Treevolution", "TSP "]

# db_helper = DatabaseHelper('database/data/funga_data.db')


tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header(_('Hello Evolving Shapes'))
    col1, col2 = st.columns(2)
    with col1:
        st.header("Initial population")
        population = init_population(200)
        for individual in population:
            entropy, white_ratio, fitness = calculate_fitness_return_all(individual)
            st.image(draw_image_from_array(individual),
                     caption=f"Entropy: {entropy:.4f}, White Ratio: {white_ratio:4f}, Fitness: {fitness:.4f}")
            st.image(draw_image_from_array(rotation_mutation(individual.copy())),
                     caption=f"Mutant")
    with col2:
        evolved_population = evolve(population)
        st.header('Evolved population')
        for individual in evolved_population:
            entropy, white_ratio, fitness = calculate_fitness_return_all(individual)
            st.image(draw_image_from_array(individual),
                     caption=f"Entropy: {entropy:.4f}, White Ratio: {white_ratio:4f}, Fitness: {fitness:.4f}")

with tabs[1]:
    st.header(_('Hello Evolving Trees'))
with tabs[2]:
    st.header(_('Hello Traveling Salesman'))

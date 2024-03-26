import base64
from pathlib import Path
from PIL import Image, ImageDraw

import streamlit as st
from streamlit.components.v1 import html

from utils.genetic.biomorphs.evolve import evolve_biomorphs
from utils.genetic.biomorphs.phenotype import draw_biomorph, get_base64_of_image
from utils.genetic.shapevo.evolve import evolve
from utils.genetic.shapevo.operators import calculate_fitness_return_all, rotation_mutation
from utils.genetic.shapevo.phenotype import draw_image_from_array
from utils.genetic.shapevo.population import init_population
from utils.navigation import show_main_menu, get_localizator
from st_clickable_images import clickable_images

# from database.database_helper import DatabaseHelper

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

tabs_options = ["Shapevo", "Biomorphs", "TSP "]

# db_helper = DatabaseHelper('database/data/funga_data.db')


tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header(_('Hello Evolving Shapes'))
    col1, col2 = st.columns(2)
    with col1:
        st.header("Initial population")
        population = init_population(2)
        for individual in population:
            entropy, white_ratio, fitness = calculate_fitness_return_all(individual)
            st.image(draw_image_from_array(individual),
                     caption=f"Entropy: {entropy:.4f}, White Ratio: {white_ratio:4f}, Fitness: {fitness:.4f}")
            # st.image(draw_image_from_array(rotation_mutation(individual.copy())),
            #          caption=f"Mutant")
    with col2:
        # evolved_population = evolve(population)
        st.header('Evolved population')
        # for individual in evolved_population:
        #     entropy, white_ratio, fitness = calculate_fitness_return_all(individual)
        #     st.image(draw_image_from_array(individual),
        #              caption=f"Entropy: {entropy:.4f}, White Ratio: {white_ratio:4f}, Fitness: {fitness:.4f}")

with tabs[1]:
    st.header(_('Biomorphs'))

    if "clicked" not in st.session_state:
        st.session_state["clicked"] = ""
    st.text(st.session_state["clicked"])

    biomorphs = []
    for i in range(12):
        biomorphs.append(get_base64_of_image(evolve_biomorphs()))

    clicked = clickable_images(
        biomorphs,
        titles=[f"Creature #{str(i + 1)}" for i in range(len(biomorphs))],
        div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        img_style={"margin": "10px", "height": "200px"},
    )
    if clicked:
        st.session_state["clicked"] = clicked
    st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

with tabs[2]:
    st.header(_('Hello Traveling Salesman'))

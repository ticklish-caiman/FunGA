import streamlit as st

from utils.genetic.biomorphs.evolve import evolve_biomorphs, test_pass_choice
from utils.genetic.biomorphs.phenotype import get_base64_of_image
from utils.genetic.shapevo.operators import calculate_fitness_return_all
from utils.genetic.shapevo.phenotype import draw_image_from_array
from utils.genetic.shapevo.population import init_population
from utils.navigation import show_main_menu, get_localizator

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

    biomorphs = []
    for i in range(12):
        biomorphs.append(get_base64_of_image(evolve_biomorphs()))


    def on_click():
        biomorphs = []
        for i in range(12):
            biomorphs.append(get_base64_of_image(evolve_biomorphs()))


    col1, col2, col3 = st.columns(3)

    for i in range(12):
        if i < 4:
            with col1:
                with st.container(border=1):
                    if st.button("⬇️ Choose me ⬇️", args=i, key=i, on_click=on_click(), use_container_width=True):
                        st.session_state["clicked"] = i
                        test_pass_choice(i)
                    st.image(biomorphs[i], width=200)
        elif i < 8:
            with col2:
                with st.container(border=1):
                    if st.button("⬇️ Choose me ⬇️", args=i, key=i, on_click=on_click(), use_container_width=True):
                        st.session_state["clicked"] = i
                        test_pass_choice(i)
                    st.image(biomorphs[i], width=200)
        else:
            with col3:
                with st.container(border=1):
                    if st.button("⬇️ Choose me ⬇️", args=i, key=i, on_click=on_click(), use_container_width=True):
                        st.session_state["clicked"] = i
                        test_pass_choice(i)
                    st.image(biomorphs[i], width=200)

with tabs[2]:
    st.header(_('Hello Traveling Salesman'))

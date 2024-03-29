import streamlit as st

from utils.custom_css import custom_buttons_style
from utils.genetic.biomorphs.biomorphs_operators import calculate_population_fitness
from utils.genetic.biomorphs.evolve import draw_biomorph, test_pass_choice
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

    custom_buttons_style()

    if "clicked" not in st.session_state:
        st.session_state["clicked"] = ""

    # User input for columns and rows
    # num_columns = st.sidebar.number_input("Number of columns", min_value=1, max_value=12, value=3)
    num_columns = 3  # only 3 columns look good
    num_rows = st.sidebar.number_input("Number of rows", min_value=1, max_value=12, value=3)


    def on_click():
        biomorphs = []
        for i in range(num_columns * num_rows):
            biomorphs.append(get_base64_of_image(draw_biomorph()))


    # Initialize biomorphs (you may want to move this into on_click
    # if they need to be generated on demand)
    biomorphs = []
    for i in range(num_columns * num_rows):
        biomorphs.append(get_base64_of_image(draw_biomorph()))

    biomorph_id = 0
    # Dynamic grid creation
    for row in range(num_rows):
        cols = st.columns(num_columns)
        start_index = row * num_columns
        end_index = start_index + num_columns

        for i, biomorph in enumerate(biomorphs[start_index:end_index]):
            col_index = i % num_columns  # Get the column index within the current row

            with cols[col_index]:
                with st.container(border=1):
                    if st.button("⬇️ Choose me ⬇️", args=i, key=biomorph_id, on_click=on_click()):
                        st.session_state["clicked"] = biomorph_id
                        test_pass_choice(biomorph_id)
                    st.image(biomorph, width=200)
                biomorph_id += 1

with tabs[2]:
    st.header(_('Hello Traveling Salesman'))

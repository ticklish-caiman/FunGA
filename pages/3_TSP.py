import streamlit as st

from utils.genetic.tsp.tsp_evolve import create_population, evolve
from utils.genetic.tsp.tsp_genes import generate_cities
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

if 'tsp_plot' not in st.session_state:
    st.session_state['tsp_plot'] = None

st.header(_('Traveling Salesman Problem'))

# Input parameters from the user
cities_count = st.number_input("How many cities:", min_value=5, value=50, max_value=300)
random_cities = st.checkbox('⬅️ Random cities')
pop_size = st.number_input("Population Size", min_value=10, value=50)
generations = st.number_input("Generations", min_value=50, value=500)
tournament_size = st.number_input("Tournament size:", min_value=2, value=int(pop_size / 10), max_value=pop_size)
mutation_rate = st.number_input("Mutation rate:", min_value=0.01, value=0.5, step=0.01)

if st.button("Start Optimization"):
    with st.spinner("Running Genetic Algorithm..."):
        cities = generate_cities(cities_count, random_cities)
        population = create_population(pop_size, len(cities))
        progress_plot_img = []
        generator = evolve(population, cities, generations, tournament_size, mutation_rate)  # Get generator object
        image_placeholder = st.empty()  # Create a placeholder

        for i, (population, last_image) in enumerate(generator):
            image_placeholder.image(last_image)  # Display only the new images
            progress_plot_img.append(last_image)

        st.text("Evolution complete!")

        with st.popover("Show Evolution Process"):
            for plot_img in progress_plot_img:
                st.image(plot_img)

import streamlit as st

from utils.genetic.tsp.tsp_evolve import create_population, evolve
from utils.genetic.tsp.tsp_genes import generate_cities
from utils.genetic.tsp.tsp_operators import route_distance
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

if 'tsp_plot' not in st.session_state:
    st.session_state['tsp_plot'] = None

st.header(_('Hello Traveling Salesman'))

# Input parameters from the user
pop_size = st.number_input("Population Size", min_value=10, value=50)
generations = st.number_input("Generations", min_value=50, value=500)
# ... Other parameters (tournament_size, mutation_rate)

if st.button("Start Optimization"):
    with st.spinner("Running Genetic Algorithm..."):
        cities = generate_cities()
        population = create_population(pop_size, len(cities))
        progress_plot_img = []
        generator = evolve(population, cities, generations)  # Get generator object
        image_placeholder = st.empty()  # Create a placeholder

        for i, (population, new_images) in enumerate(generator):
            image_placeholder.image(new_images)  # Display only the new images
    st.text("Evolution complete!")

    # Area to display the plot:
    # st.image(progress_plot_img)

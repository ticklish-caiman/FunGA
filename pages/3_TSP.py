import streamlit as st

from utils.custom_css import custom_write_style
from utils.genetic.tsp.tsp_evolve import create_population, evolve
from utils.genetic.tsp.tsp_genes import generate_cities
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

if 'generations_choice' not in st.session_state:
    st.session_state['generations_choice'] = 500

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False


def disable():
    st.session_state["disabled"] = True


def enable():
    st.session_state["disabled"] = False


st.header(_('Traveling Salesman Problem'))

with st.sidebar.expander("⚙️ TSP OPTIONS️ ⚙️", expanded=True):
    generations = st.number_input("Generations", min_value=50, value=st.session_state['generations_choice'],
                                  disabled=st.session_state.disabled)

    with st.popover("🔧 Advanced options", disabled=st.session_state.disabled):
        col1, col2 = st.columns(2)
        with col1:
            pop_size = st.number_input("Population Size", min_value=10, value=50)
            cities_count = st.number_input("How many cities:", min_value=5, value=50, max_value=300)
            random_cities = st.checkbox('⬅️ Random cities')
        with col2:
            tournament_size = st.number_input("Tournament size:", min_value=2, value=int(pop_size / 10),
                                              max_value=pop_size)
            mutation_rate = st.number_input("Mutation rate:", min_value=0.01, value=0.5, step=0.01)

with st.expander("What is TSP? (click to expand)", expanded=False):
    custom_write_style()
    st.write(
        """The Traveling Salesman Problem is like finding the shortest way to visit a bunch of cities, going to each 
        city only once, and ending back where you started.""")
    st.write('Want to know why it is so hard?')
    st.page_link('pages/4_Theory.py', label="Click here to see detailed explanation")

st.write("Adjust parameters from ⚙️TSP OPTIONS️⚙️ in the sidebar.")
st.markdown("⤸")

if st.session_state["disabled"]:
    st.button("Start again", on_click=enable)
    st.sidebar.button("Start again", on_click=enable, key='sidebar_reset')

if st.button("⏱Start Evolution⏱", on_click=disable, disabled=st.session_state.disabled):
    complete_message = st.empty()
    with st.spinner("Running Genetic Algorithm..."):
        cities = generate_cities(cities_count, random_cities)
        population = create_population(pop_size, len(cities))
        progress_plot_img = []
        generator = evolve(population, cities, generations, tournament_size,
                           mutation_rate)  # Get generator object
        image_placeholder = st.empty()  # Create a placeholder

        for i, (population, last_image) in enumerate(generator):
            image_placeholder.image(last_image)  # Display only the new images
            progress_plot_img.append(last_image)
    complete_message.text("Evolution complete! ✅")

    with st.popover("Show Evolution Process"):
        for plot_img in progress_plot_img:
            st.image(plot_img)

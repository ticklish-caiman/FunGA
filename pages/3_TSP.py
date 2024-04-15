import streamlit as st

from database.model.activity import Activity
from utils.custom_css import custom_write_style
from utils.genetic.tsp.tsp_creator import custom_city_generator, custom_city_creator
from utils.genetic.tsp.tsp_evolve import create_population, evolve
from utils.genetic.tsp.tsp_genes import generate_cities

from utils.navigation import show_main_menu, get_localizator

from database.database_helper import DatabaseHelper

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

db_helper = DatabaseHelper('database/data/funga_data.db')

if 'generations_choice' not in st.session_state:
    st.session_state['generations_choice'] = 500

if 'cities_count' not in st.session_state:
    st.session_state['cities_count'] = 50

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False


def disable():
    st.session_state["disabled"] = True


def enable():
    st.session_state["disabled"] = False


# TODO: human vs machine, human and machine cooperation
#       1. give use the ability to find a better solution than GA (vs mode)
#       2. Give the the ability to help the algorithm (coop mode) - user will be able to add initial solutions


st.header(_(':rainbow[Traveling Salesman Problem]'))

task_type = st.radio(
    _("**Choose type of the game**"),
    [":blue[**Computer**]", ":orange[**Human**]", ":green[**Cooperation**]"],
    captions=["Let the algorithm work for you.", "Do it yourself.", "Help the computer."], horizontal=True)

if task_type == ":blue[**Computer**]":

    with st.sidebar.expander("⚙️ TSP OPTIONS️ ⚙️", expanded=True):
        generations = st.number_input("Generations", min_value=50, value=st.session_state['generations_choice'],
                                      disabled=st.session_state.disabled)

        with st.popover("🔧 Advanced options", disabled=st.session_state.disabled):
            col1, col2 = st.columns(2)
            with col1:
                pop_size = st.number_input("Population Size", min_value=10, value=50)
                st.session_state['cities_count'] = st.number_input("How many cities:", min_value=5,
                                                                   value=st.session_state['cities_count'],
                                                                   max_value=300)
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

    st.write("⤸ Adjust parameters from ⚙️TSP OPTIONS️⚙️ in the sidebar.")

    if st.session_state["disabled"]:
        st.button("Start again", on_click=enable)
        st.sidebar.button("Start again", on_click=enable, key='sidebar_reset')

    if st.button("⏱Start Evolution⏱", on_click=disable, disabled=st.session_state.disabled):
        complete_message = st.empty()
        with st.spinner("Running Genetic Algorithm..."):
            cities = generate_cities(st.session_state['cities_count'], random_cities)
            population = create_population(pop_size, len(cities))
            progress_plot_img = []
            generator = evolve(population, cities, generations, tournament_size,
                               mutation_rate)  # Get generator object
            image_placeholder = st.empty()  # Create a placeholder

            for i, (population, last_image) in enumerate(generator):
                image_placeholder.image(last_image)  # Display only the new images
                progress_plot_img.append(last_image)

        if st.session_state["authentication_status"]:
            print('Saving logged user results...')
        else:
            print('Saving guest result...')
            activity = Activity('test_login', 'TSP', 'TSP_result', user_id=1)
            db_helper.add_activity(activity)

        complete_message.text("Evolution complete! ✅")

        with st.popover("Show Evolution Process"):
            for plot_img in progress_plot_img:
                st.image(plot_img)

    if 'cities' not in st.session_state:
        st.session_state['cities'] = generate_cities()

    if 'road_clicks' not in st.session_state:
        st.session_state['road_clicks'] = []
    if 'user_roads' not in st.session_state:
        st.session_state['user_roads'] = []

if task_type == ":orange[**Human**]":
    print('TAB 1')
    custom_city_generator()
    custom_city_creator()
    print('TAB 1 rendered')

if task_type == ":green[**Cooperation**]":
    st.write("Work in progress...")
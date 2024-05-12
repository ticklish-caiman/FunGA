import numpy as np
import pandas as pd
import streamlit as st
import logging

from database.model.tspactivity import TspActivity
from utils.custom_css import custom_write_style
from utils.genetic.tsp.tsp_creator import custom_city_generator, custom_city_creator
from utils.genetic.tsp.tsp_evolve import create_population, evolve
from utils.genetic.tsp.tsp_genes import generate_cities, convert_string_routes
from utils.genetic.tsp.tsp_operators import route_distance

from utils.navigation import show_main_menu
from utils.localization_helper import get_localizator

from database.database_helper import DatabaseHelper

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

db_helper = DatabaseHelper('database/data/funga_data.db')

logging.basicConfig(level=logging.INFO)

if 'generations_choice' not in st.session_state:
    st.session_state['generations_choice'] = 500

if 'cities_count' not in st.session_state:
    st.session_state['cities_count'] = 20

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False


def disable():
    st.session_state["disabled"] = True


def enable():
    st.session_state["disabled"] = False


def start_evolution(population: list = None):
    complete_message = st.empty()
    with st.spinner(_("Running Genetic Algorithm...")):
        cities = generate_cities(st.session_state['cities_count'], random_cities)
        if not population:
            mode = 'computer'
            population = create_population(pop_size, len(cities))
        else:
            mode = 'cooperation'
            if len(population) == pop_size:
                pass
            elif len(population) < pop_size:
                print('population:', population)
                population = convert_string_routes(population)
                print('converted population:', population)
                print('pop_size', pop_size)
                logging.info('User passed too small population, expanding with random ones')
                population.extend(create_population(pop_size - len(population), len(cities)))
                print('new population:', population)
            else:
                print('population:', len(population))
                print('pop_size', pop_size)
                logging.info('User passed too big population, not all proposed routes will be used')

        progress_plot_img = []
        generator = evolve(population, cities, generations, tournament_size,
                           mutation_rate)  # Get generator object
        image_placeholder = st.empty()  # Create a placeholder

        for i, (population, last_image) in enumerate(generator):
            image_placeholder.image(last_image)  # Display only the new images
            progress_plot_img.append(last_image)

        best_route = min(population, key=lambda route: route_distance(route, cities))
        logging.info(f"Best route: {best_route}")
        logging.info(f"Distance: {route_distance(best_route, cities)}")

    ga_params = {'generations': generations, 'pop_size': pop_size, 'tournament_size': tournament_size,
                 'mutation_rate': mutation_rate}
    if st.session_state["authentication_status"]:
        logging.info(_('Saving logged user results...'))
        activity = TspActivity(st.session_state["username"], mode, st.session_state["name"],
                               route_distance(best_route, cities), str(best_route), str(ga_params))
        db_helper.add_tsp_activity(activity)
    else:
        logging.info(_('Saving guest result...'))

        activity = TspActivity('Guest_account', "computer", 'Guest',
                               route_distance(best_route, cities), str(best_route), str(ga_params))
        db_helper.add_tsp_activity(activity)

    complete_message.text(_("Evolution complete! ✅"))

    with st.popover(_("Show Evolution Process")):
        for plot_img in progress_plot_img:
            st.image(plot_img)


st.header(_(':rainbow[Traveling Salesman Problem]'))

with st.expander(_("What is TSP? (click to expand)"), expanded=False):
    custom_write_style()
    st.write(
        _("The Traveling Salesman Problem is like finding the shortest way to visit a bunch of cities, going to each "
          "city only once, and ending back where you started."))
    st.write(_('Want to know why it is so hard?'))
    st.page_link('pages/4_Theory.py', label=_("Click here to see detailed explanation"))

with st.sidebar.expander(_("⚙️ TSP OPTIONS️ ⚙️"), expanded=True):
    generations = st.number_input("Generations", min_value=50, value=st.session_state['generations_choice'],
                                  disabled=st.session_state.disabled)

    with st.popover(_("🔧 Advanced options"), disabled=st.session_state.disabled):
        col1, col2 = st.columns(2)
        with col1:
            pop_size = st.number_input(_("Population Size"), min_value=10, value=50)
            st.session_state['cities_count'] = st.number_input(_("How many cities:"), min_value=5,
                                                               value=st.session_state['cities_count'],
                                                               max_value=300)
            random_cities = st.checkbox(_('⬅️ Random cities'))
        with col2:
            tournament_size = st.number_input(_("Tournament size:"), min_value=2, value=int(pop_size / 10),
                                              max_value=pop_size)
            mutation_rate = st.number_input(_("Mutation rate:"), min_value=0.01, value=0.5, step=0.01)

difficulty = st.radio(
    _("**Choose difficulty**"),
    [_(":green[**Easy**]"), _(":orange[**Medium**]"), _(":red[**Hard**]"), _(":blue[**Custom**]")],
    captions=[_("20 Cities"), _("30 cities"), _("50 cities")], horizontal=True)

task_type = st.radio(
    _("**Choose type of the game**"),
    [_(":blue[**Computer**]"), _(":orange[**Human**]"), _(":green[**Cooperation**]")],
    captions=[_("Let the algorithm work for you."), _("Do it yourself."), _("Help the computer.")], horizontal=True)

if task_type == _(":blue[**Computer**]"):

    st.write(_("⤸ Adjust parameters from ⚙️TSP OPTIONS️⚙️ in the sidebar."))

    if st.session_state["disabled"]:
        st.button(_("Start again"), on_click=enable)
        st.sidebar.button(_("Start again"), on_click=enable, key='sidebar_reset')

    if st.button(_("⏱Start Evolution⏱"), on_click=disable, disabled=st.session_state.disabled):
        start_evolution()

if task_type == _(":orange[**Human**]"):

    if difficulty == _(":green[**Easy**]"):
        st.session_state['cities_count'] = 20

    if difficulty == _(":orange[**Medium**]"):
        st.session_state['cities_count'] = 30

    if difficulty == _(":red[**Hard**]"):
        st.session_state['cities_count'] = 50

    if difficulty == _(":blue[**Custom**]"):
        custom_city_generator()

    if 'cities' not in st.session_state:
        st.session_state['cities'] = generate_cities(st.session_state['cities_count'])
    if 'road_clicks' not in st.session_state:
        st.session_state['road_clicks'] = []
    if 'user_roads' not in st.session_state:
        st.session_state['user_roads'] = []

    if st.session_state['cities_count'] != len(st.session_state['cities']):
        st.session_state['cities'] = generate_cities(st.session_state['cities_count'])

    custom_city_creator()

if task_type == _(":green[**Cooperation**]"):
    if st.session_state["authentication_status"]:
        user_tsp_results = pd.DataFrame(db_helper.get_user_manual_tsp(st.session_state['username']))
        user_tsp_results.index = np.arange(1, len(user_tsp_results) + 1)  # index from 1
        user_tsp_results.columns = [_('Distance'), _('Route')]
        st.table(user_tsp_results)

        selected_indices = st.multiselect(_('Select routes to use:'), user_tsp_results.index,
                                          placeholder=_('Select routes to use'))
        selected_rows = user_tsp_results.loc[selected_indices]
        st.table(selected_rows)
        if st.button(_('Evolve with selected routes')):
            if not selected_indices:  # Check if any indices are selected
                st.error("Please select routes to evolve with.")
            else:
                selected_routes = selected_rows["Route"].tolist()
                start_evolution(selected_routes)

    else:
        st.header(_('Log into your account to see or create routes. '))

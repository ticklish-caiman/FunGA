import time

import pandas as pd
import streamlit as st

from database.model.activity import Activity
from utils.custom_css import custom_write_style
from utils.genetic.tsp.tsp_evolve import create_population, evolve
from utils.genetic.tsp.tsp_genes import generate_cities
from utils.navigation import show_main_menu, get_localizator

from database.database_helper import DatabaseHelper

import plotly.graph_objects as go
import plotly.express as px
from streamlit_plotly_events import plotly_events

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

db_helper = DatabaseHelper('database/data/funga_data.db')

if 'generations_choice' not in st.session_state:
    st.session_state['generations_choice'] = 500

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False


def disable():
    st.session_state["disabled"] = True


def enable():
    st.session_state["disabled"] = False


tabs_options = ['Genetic algorithm', 'Create you own road']
tabs = st.tabs(tabs_options)

with tabs[0]:
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

    st.write("⤸ Adjust parameters from ⚙️TSP OPTIONS️⚙️ in the sidebar.")

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

with tabs[1]:
    @st.cache_data
    def init_user_input_plot():
        # Generate city data and create the Plotly figure (outside draw_map)
        df = pd.DataFrame(st.session_state['cities'], columns=['x', 'y'])
        fig = px.scatter(df, x='x', y='y', title='Click on a city, then on another one to create a road',
                         range_x=(-10, 110), range_y=(-10, 110), color_discrete_sequence=['blue'])

        fig.layout.xaxis.visible = False
        fig.layout.yaxis.visible = False
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        fig.layout.margin.t = 80
        fig.layout.margin.l = 5
        fig.layout.margin.r = 5
        fig.layout.margin.b = 5
        fig.layout.showlegend = False
        fig.layout.boxmode = 'group'

        # worth investigating
        fig.layout.clickmode = 'event+select'

        # probably a better way to sett fig properties
        fig.layout.update(dragmode=False)

        return fig


    fig = init_user_input_plot()


    @st.experimental_fragment
    def draw_map():
        # Draw all existing roads
        for start, end in st.session_state['user_roads']:
            fig.add_trace(
                go.Scatter(x=[start[0], end[0]], y=[start[1], end[1]], mode='lines', line=dict(color='red'))
            )
        return fig


    if st.button("Undo (remove last road)"):
        if len(st.session_state.user_roads) > 0:
            st.session_state.user_roads.pop()

    rerun = False

    selected_points = plotly_events(draw_map(), click_event=True, select_event=False, hover_event=False)

    if selected_points:
        x, y = selected_points[0]['x'], selected_points[0]['y']
        st.session_state['road_clicks'].extend([x, y])

        if len(st.session_state['road_clicks']) >= 4:
            start_x, start_y, end_x, end_y = st.session_state['road_clicks'][-4:]
            st.session_state['user_roads'].append([(start_x, start_y), (end_x, end_y)])
            st.session_state['road_clicks'] = []
            rerun = True
    st.write("Road so far:")
    custom_write_style()
    st.write(f"{(st.session_state['user_roads'])}")

    if rerun:
        st.rerun()

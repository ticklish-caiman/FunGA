import pandas as pd
import streamlit as st

import plotly.graph_objects as go
import plotly.express as px
from streamlit_plotly_events import plotly_events

from utils.custom_css import custom_write_style
from utils.genetic.tsp.tsp_operators import coordinates_to_permutation, route_distance
from utils.genetic.tsp.tsp_genes import generate_cities


def custom_city_generator():
    def update_cities(ccc):
        st.session_state['cities'] = generate_cities(ccc)

    custom_cities_count = st.number_input("How many cities:", min_value=5,
                                          value=51,
                                          max_value=300,
                                          key='custom_cities_c')
    update_cities(custom_cities_count)


# that took a while... but I'm not satisfied with the results,
# even after fixing remaining bugs we will have the responsiveness problem,
# and it will only get worse after deploying the app on server
# idea: use canvas: https://github.com/andfanilo/streamlit-drawable-canvas
# problem: how to generate route based on user drawing
def custom_city_creator():
    if 'auto_connect_roads' not in st.session_state:
        st.session_state['auto_connect_roads'] = False

    if 'last_error' not in st.session_state:
        st.session_state['last_error'] = None

    if 'last_instruction' not in st.session_state:
        st.session_state['last_instruction'] = "Click on the first city!"

    if 'user_permutation' not in st.session_state:
        st.session_state["user_permutation"] = []

    if 'final_connection' not in st.session_state:
        st.session_state["final_connection"] = False

    if st.session_state["last_error"]:
        st.error(st.session_state["last_error"])
        st.session_state["last_error"] = None

    if st.session_state["last_instruction"]:
        st.info(st.session_state["last_instruction"])
        if st.button('Save route'):
            st.write('Route has been successfully saved!')

    def init_user_input_plot():
        # Generate city data and create the Plotly figure (outside draw_map)
        df = pd.DataFrame(st.session_state['cities'], columns=['x', 'y'])
        fig = px.scatter(df, x='x', y='y', title='',
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

    def draw_map():
        # Draw all existing roads
        for start, end in st.session_state['user_roads']:
            fig.add_trace(
                go.Scatter(x=[start[0], end[0]], y=[start[1], end[1]], mode='lines', line=dict(color='red'))
            )
        return fig

    st.session_state['last_instruction'] = "Click on the second city to create a road!"

    rerun = False

    button_col1, button_col2 = st.columns(2)

    with button_col1:

        if st.button("Undo (remove last road)"):
            if len(st.session_state.user_roads) > 0:
                st.session_state.user_roads.pop()
                st.session_state.user_permutation.pop()
                st.session_state['road_clicks'] = []

    with button_col2:

        if st.button("Clear roads (start again)"):
            if len(st.session_state.user_roads) > 0:
                st.session_state['user_roads'] = []
                st.session_state['road_clicks'] = []
                st.session_state['user_permutation'] = []
                st.session_state['auto_connect_roads'] = False
                st.session_state['last_instruction'] = "Click on the first city!"
                rerun = True

    selected_points = plotly_events(draw_map(), click_event=True, select_event=False, hover_event=False)

    if selected_points:

        st.session_state["final_connection"] = len(st.session_state["user_permutation"]) == len(
            st.session_state['cities'])
        x, y = selected_points[0]['x'], selected_points[0]['y']

        if st.session_state["final_connection"]:
            st.session_state['last_instruction'] = "Congratulations! Your route has been successfully created!"
        else:
            st.session_state['last_instruction'] = "Click on the next city to create another road!"

        if st.session_state['auto_connect_roads']:
            # Automatically connect to the last city
            if st.session_state['user_roads']:
                last_road = st.session_state['user_roads'][-1]
                start_x, start_y = last_road[1]  # End of the last road becomes the start
                st.session_state['road_clicks'].extend([start_x, start_y, x, y])
        else:
            st.session_state['road_clicks'].extend([x, y])

        if len(st.session_state['road_clicks']) >= 4:
            start_x, start_y, end_x, end_y = st.session_state['road_clicks'][-4:]

            if (start_x, start_y) != (end_x, end_y):  # check if the start/end cities are different

                start_city_occurrences = sum(road.count((start_x, start_y))
                                             for road in st.session_state['user_roads'])
                end_city_occurrences = sum(road.count((end_x, end_y))
                                           for road in st.session_state['user_roads'])

                if start_city_occurrences >= 2 or end_city_occurrences >= 2:  # prevent connecting city more than twice
                    st.session_state["last_error"] = "City already has maximum connections!"
                else:
                    old_permutation = st.session_state["user_permutation"]

                    # Convert coordinates to indices before the check
                    start_city_index = st.session_state['cities'].index((start_x, start_y))
                    end_city_index = st.session_state['cities'].index((end_x, end_y))

                    # prevent creating sub-routes / Handle final connection
                    if start_city_index not in old_permutation or end_city_index not in old_permutation or \
                            st.session_state["final_connection"]:
                        st.session_state['user_roads'].append([(start_x, start_y), (end_x, end_y)])
                        st.session_state["user_permutation"] = coordinates_to_permutation(
                            st.session_state['user_roads'],
                            st.session_state['cities'])
                    else:

                        st.session_state["last_error"] = "Changes would create sub-routes!"

                    # prevent creating separate routes
                    if len(old_permutation) + 2 == len(st.session_state['user_permutation']) and len(
                            old_permutation) > 1:
                        st.session_state.user_permutation.pop()
                        st.session_state.user_permutation.pop()
                        st.session_state.user_roads.pop()
                        st.session_state["last_error"] = "Can't create separate routes!"

            else:
                st.session_state["last_error"] = "Double click! You clicked twice on the same city."

            # Writing functions to prevent duplicates/reverse roads might be unnecessary,
            # as the "coordinates_to_permutation" function handles them

            st.session_state['road_clicks'] = []
            st.session_state['auto_connect_roads'] = True
            if not st.session_state["last_error"]:
                rerun = True
    st.write("Road so far:")
    custom_write_style()
    st.write(f"{(st.session_state['user_roads'])}")
    st.write("Permutation:")
    st.write(f"{st.session_state['user_permutation']}")
    st.write("Distance:")
    st.write(route_distance(st.session_state['user_permutation'], st.session_state['cities']))

    if rerun:
        st.rerun()

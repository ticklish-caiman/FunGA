import base64
from pathlib import Path
from PIL import Image, ImageDraw

import streamlit as st

from utils.genetic.biomorphs.evolve import evolve_biomorphs
from utils.genetic.biomorphs.phenotype import draw_biomorph
from utils.genetic.shapevo.evolve import evolve
from utils.genetic.shapevo.operators import calculate_fitness_return_all, rotation_mutation
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

    img_path = Path(__file__).parent.parent / 'img'

    if 'biomorph_message' not in st.session_state:
        st.session_state['biomorph_message'] = ''
    if 'img_path' not in st.session_state:
        st.session_state['img_path'] = img_path

    biomorphs_output = st.write(st.session_state['biomorph_message'])

    # Function to read image and encode as Base64
    def get_base64_of_image(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded_string}"


    try:
        base64_img = get_base64_of_image(st.session_state['img_path'])
    except PermissionError:
        new_biomorph_image = evolve_biomorphs()

        # Save the Biomorph Image (using row and col for naming)
        new_biomorph_image.save(img_path / f'00.jpg')

        # Update an image path in session state
        st.session_state['img_path'] = img_path / f'00.jpg'
        base64_img = get_base64_of_image(st.session_state['img_path'])


    def on_click(row, col):
        st.session_state['biomorph_message'] = f"You chose square at row {row}, column {col}"
        st.session_state['img_path'] = Path(__file__).parent.parent / 'img' / f'{row}{col}.jpg'
        # Generate a new Biomorph
        new_biomorph_image = evolve_biomorphs()

        # Save the Biomorph Image (using row and col for naming)
        new_biomorph_image.save(img_path / f'{row}{col}.jpg')

        # Update an image path in session state
        st.session_state['img_path'] = img_path / f'{row}{col}.jpg'


    st.write("Choose the best specimen:")

    rows = 3
    cols = 4
    st.markdown(f"""
    <style>
    .stButton button {{
        width: 150px; /* Adjust as needed */
        height: 150px; /* Adjust as needed */
        background-image: url("{base64_img}"); 
        background-size: cover; /* To fit the image */
        border: none;
        color: transparent; /* Hide the default button text */  
    }}
    .stButton p {{ 
        display: none; /* Hide button label */
    }}
    </style>
    """, unsafe_allow_html=True)
    for row in range(rows):
        cols_container = st.columns(cols)  # Create a row of columns
        for col in range(cols):
            with cols_container[col]:
                if st.button(f"({row}, {col})", on_click=on_click, args=(row, col), help="Click me!"):
                    pass
with tabs[2]:
    st.header(_('Hello Traveling Salesman'))

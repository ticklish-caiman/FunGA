import streamlit as st
from utils.navigation import show_main_menu, get_localizator
from PIL import Image, ImageDraw
import numpy as np
import random

# from database.database_helper import DatabaseHelper

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

tabs_options = ["Treevolution", "Shapevo", "TSP "]


# db_helper = DatabaseHelper('database/data/funga_data.db')

def draw_image_from_array(binary_array):
    width = len(binary_array[0])  # Get width from the first row
    height = len(binary_array)  # Get height from the number of rows

    image = Image.new('RGB', (width, height), color='white')  # Create a white image
    draw = ImageDraw.Draw(image)

    # Iterate over the array, drawing pixels
    for y, row in enumerate(binary_array):
        for x, pixel in enumerate(row):
            if pixel == 1:
                draw.point((x, y), fill='black')  # Draw a black pixel

    return image


# Since it's 200x200, let's create the array procedurally (example)
binary_array_grid_pattern = [[1 if x % 10 == 0 or y % 10 == 0 else 0
                              for x in range(200)]
                             for y in range(200)]

binary_array_alternating_squares = [[1 if (x + y) % 2 == 0 else 0
                                     for x in range(200)]
                                    for y in range(200)]

binary_array_circle = [[1 if (x - 100) ** 2 + (y - 100) ** 2 <= 40 ** 2 else 0
                        for x in range(200)]
                       for y in range(200)]

binary_array_random = [[random.randint(0, 1) for x in range(200)]  # Random 0s and 1s
                       for y in range(200)]

# Generate the grid pattern
grid_array = [[1 if (x + y) % 10 == 0 else 0
               for x in range(200)]
              for y in range(200)]

# Generate the circle pattern
circle_array = [[0 if (x - 100) ** 2 + (y - 100) ** 2 <= 50 ** 2 else 1
                 for x in range(200)]
                for y in range(200)]

# Combine patterns (grid AND NOT circle)
combined_array = [[grid_array[y][x] and not circle_array[y][x] for x in range(200)]
                  for y in range(200)]

result_image = draw_image_from_array(combined_array)

tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header(_('Hello Evolving Shapes'))

    # Show image
    st.text('Sample image:')
    st.image(result_image)

    all_arrays = [binary_array_grid_pattern, binary_array_alternating_squares, binary_array_circle, binary_array_random,
                  grid_array, circle_array]

    random.shuffle(all_arrays)
    st.text('Random image:')
    result_image = draw_image_from_array(all_arrays[0])
    st.image(result_image)

    st.text('Randomly combined image:')
    combined_array = [[all_arrays[0][y][x] and not all_arrays[1][y][x] for x in range(200)]
                      for y in range(200)]
    result_image = draw_image_from_array(combined_array)
    st.image(result_image)

with tabs[1]:
    st.header(_('Hello Evolving Trees'))
with tabs[2]:
    st.header(_('Hello Traveling Salesman'))

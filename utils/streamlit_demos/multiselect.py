import streamlit as st


# https://30days.streamlit.app/?challenge=Day11
def multiselect_demo():
    st.header('st.multiselect')

    options = st.multiselect(
        'What are your favorite colors',
        ['Green', 'Yellow', 'Red', 'Blue'],
        ['Yellow', 'Red'])

    st.write('You selected:', options)

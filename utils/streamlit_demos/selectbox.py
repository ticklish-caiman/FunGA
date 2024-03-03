import streamlit as st


# https://30days.streamlit.app/?challenge=Day10
def selectbox_demo():
    st.header('st.selectbox')

    option = st.selectbox(
        'What is your favorite color?',
        ('Blue', 'Red', 'Green'))

    st.write('Your favorite color is ', option)

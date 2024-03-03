import streamlit as st


# https://30days.streamlit.app/?challenge=Day12
def checkbox_demo():
    st.header('st.checkbox')

    st.write('What would you like to order?')

    icecream = st.checkbox('Ice cream')
    coffee = st.checkbox('Coffee')
    cola = st.checkbox('Cola')

    if icecream:
        st.write("Great! Here's some more 🍦")

    if coffee:
        st.write("Okay, here's some coffee ☕")

    if cola:
        st.write("Here you go 🥤")

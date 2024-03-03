import streamlit as st
from utils.streamlit_demos import sliders, chart, selectbox, multiselect, checkbox, file_uploader

sidebar_options = ["Hello", "Button", "Sliders demo", "Chart demo", "Select box demo", "Multiselect demo",
                   "Checkbox demo", "File uploader demo"]
sidebar = st.sidebar.selectbox('Select your', sidebar_options)


def show_sidebar():
    if sidebar == "Hello":
        st.write('Hello funga world!')

    elif sidebar == "Button":
        st.header('First funga button')

        if st.button('Answer me!'):
            st.write('Fun with Genetic Algorithms!')
        else:
            st.write('What is FunGa?')

    elif sidebar == "Sliders demo":
        sliders.sliders_demo()

    elif sidebar == "Chart demo":
        chart.chart_demo()

    elif sidebar == "Select box demo":
        selectbox.selectbox_demo()

    elif sidebar == "Multiselect demo":
        multiselect.multiselect_demo()

    elif sidebar == "Checkbox demo":
        checkbox.checkbox_demo()

    elif sidebar == "File uploader demo":
        file_uploader.file_uploader_demo()


show_sidebar()

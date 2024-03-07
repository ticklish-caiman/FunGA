import streamlit as st


tabs_options = ["Change password", "Change password", "Change password"]


tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header('Hello')
with tabs[1]:
    st.header('Hello2')

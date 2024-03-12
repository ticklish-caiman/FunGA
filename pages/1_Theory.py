import streamlit as st

st.set_page_config(page_title="FunGA - Theory", page_icon='📚')
tabs_options = ["Natural selection", "Genetic Algorithms", "Similar approaches"]

tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header('Hello Darwin')
with tabs[1]:
    st.header('Hello Holland/De Jong')
with tabs[2]:
    st.header('Hello others')

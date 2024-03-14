import streamlit as st
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

tabs_options = ["Treevolution", "Shapevo", "TSP "]

tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header(_('Hello Evolving Trees'))
with tabs[1]:
    st.header(_('Hello Evolving Shapes'))
with tabs[2]:
    st.header(_('Hello Traveling Salesman'))

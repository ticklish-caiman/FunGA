import streamlit as st
import gettext
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='📚')

show_main_menu(_)

tabs_options = ["Natural selection", "Genetic Algorithms", "Similar approaches"]

tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header(_('Hello Darwin'))
with tabs[1]:
    st.header('Hello Holland/De Jong')
with tabs[2]:
    st.header('Hello others')

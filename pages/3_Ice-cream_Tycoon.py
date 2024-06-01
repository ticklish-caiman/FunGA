import streamlit as st

from utils.custom_css import custom_write_style
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='📚')

show_main_menu(_)

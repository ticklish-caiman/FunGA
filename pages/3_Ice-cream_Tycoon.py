import streamlit as st

from utils.custom_css import custom_write_style, custom_css
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='📚')
custom_css()
show_main_menu(_)

st.header(_("🚧 Under construction 🚧"))

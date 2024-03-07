import streamlit as st

from utils.auth import show_login_form
from utils.sidebar import show_sidebar
from utils.custom_css import custom_tabs_css

st.set_page_config(page_title="FunGA")
custom_tabs_css()

if 'kg' not in st.session_state:
    st.session_state['kg'] = 0.1
if 'lbs' not in st.session_state:
    st.session_state['lbs'] = 0.2

# Necessary to prevent streamlit from wiping out session_state when widget gets closed/hidden
st.session_state.kg = st.session_state.kg
st.session_state.lbs = st.session_state.lbs

show_login_form()
if st.session_state["authentication_status"]:
    show_sidebar()

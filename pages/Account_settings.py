import streamlit as st
from utils import global_variables as gv

from utils.auth import show_change_password_form

tabs_options = ["Change password", "Change password", "Change password"]


tabs = st.tabs(tabs_options)
with tabs[0]:

    show_change_password_form(gv.authenticator, gv.config)
with tabs[1]:
    st.header('Hello')

import sqlite3

import streamlit as st
import datetime
from utils.navigation import show_main_menu, get_localizator

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

tabs_options = ["Treevolution", "Shapevo", "TSP "]

if st.session_state["authentication_status"]:
    # Connect to a database or create it if it doesn't exist
    con = sqlite3.connect("activity_data.db")
    # Create cursor required to execute SQL statements
    cur = con.cursor()
tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header(_('Hello Evolving Trees'))
    if st.button('Add tree'):
        cur.execute("""
            INSERT INTO treevolution VALUES
                ('2024-03-17:16:33', 42, 112223344)
        """)
        con.commit()
    res = cur.execute("SELECT seed FROM treevolution")
    st.write("Seeds:", res.fetchall())
with tabs[1]:
    st.header(_('Hello Evolving Shapes'))
with tabs[2]:
    st.header(_('Hello Traveling Salesman'))

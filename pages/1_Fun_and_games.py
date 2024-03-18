import streamlit as st
from utils.navigation import show_main_menu, get_localizator
from database.database_helper import DatabaseHelper
from database.model.activity import Activity

_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='🕹️')
show_main_menu(_)

tabs_options = ["Treevolution", "Shapevo", "TSP "]
db_helper = DatabaseHelper('database/data/activity_data.db')


tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header(_('Hello Evolving Trees'))
    if st.button('Add tree'):
        activity = Activity(2, 'Mike', 'Treevolution', "Some game data to recreate game state")
        query = "INSERT INTO activities (activity_id, login, game, data) VALUES (?, ?, ?, ?)"
        params = (activity.activity_id, activity.login, activity.game, activity.data)
        db_helper.execute_query(query, params)
    res = db_helper.execute_query("SELECT * FROM activities")
    st.write("Seeds:", res.fetchall())
with tabs[1]:
    st.header(_('Hello Evolving Shapes'))
with tabs[2]:
    st.header(_('Hello Traveling Salesman'))

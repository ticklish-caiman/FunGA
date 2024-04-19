import streamlit as st
import gettext

from utils.custom_css import custom_css
from utils.streamlit_demos import sliders, chart, selectbox, multiselect, checkbox, file_uploader, progress, form, \
    session_demo

from utils.authorization import authorization_check
from database.database_helper import DatabaseHelper

_ = gettext.gettext
db_helper = DatabaseHelper('database/data/funga_data.db')
sidebar_options = ["Hello", "Button", "Sliders demo", "Chart demo", "Select box demo", "Multiselect demo",
                   "Checkbox demo", "File uploader demo", "Progress demo", "Form demo", "Session demo"]

tabs_options = ["Account ", "Activities ", "Notes "]


def show_main_menu(_):
    st.sidebar.page_link("Home_Page.py", label=_("Home"), icon="🏠")
    with st.sidebar.expander("Fun and games 🕹️", expanded=True):
        st.page_link("pages/1_Biomorphs.py", label=_("Biomorphs"), icon="😶️")
        st.page_link("pages/2_Shapevo.py", label=_("Shapevo"), icon="💠️")
        st.page_link("pages/3_TSP.py", label=_("TSP"), icon="🗺️️")
    st.sidebar.page_link("pages/4_Theory.py", label=_("Theory"), icon="📚")
    st.sidebar.page_link("pages/About.py", label=_("About"), icon="❓")


def show_sidebar():
    sidebar = st.sidebar.selectbox('Select your', sidebar_options)
    if sidebar == "Hello":
        None
    elif sidebar == "Button":
        st.header('First funga button')

        if st.button('Answer me!'):
            st.write('Fun with Genetic Algorithms!')
        else:
            st.write('What is FunGa?')

        st.image('img/funga_img01.jpg', use_column_width=True, caption='Beautiful')
        st.image('img/funga_img02.jpg', caption='Also Beautiful')

    elif sidebar == "Sliders demo":
        sliders.sliders_demo()

    elif sidebar == "Chart demo":
        chart.chart_demo()

    elif sidebar == "Select box demo":
        selectbox.selectbox_demo()

    elif sidebar == "Multiselect demo":
        multiselect.multiselect_demo()

    elif sidebar == "Checkbox demo":
        checkbox.checkbox_demo()

    elif sidebar == "File uploader demo":
        file_uploader.file_uploader_demo()

    elif sidebar == "Progress demo":
        progress.progress_demo()

    elif sidebar == "Form demo":
        form.form_demo()

    elif sidebar == "Session demo":
        session_demo.session_demo()


def show_tab0():
    authorization_check()


def show_tab1():
    if st.session_state["authentication_status"]:
        st.header('Hello')
        st.write('You are logged in!')
        st.write("st.session_state object:", st.session_state)
    else:
        st.header('Logg in to your account to see your activities. ')
        st.write("Best TSP results:")
        print(db_helper.get_best_tsp_activities(3))
        st.dataframe(db_helper.get_best_tsp_activities(3))


def show_tab2():
    if st.session_state["authentication_status"]:
        st.header('Hello')
        st.write('You are logged in!')
        # problem with this approach: "press enter to apply" can't be translated, can be disabled at best
        note = st.text_input('Add a note:', 'note text')
        if note != 'note text':
            db_helper.add_note(st.session_state['username'], note)
        st.title("NOTES:")
        st.dataframe(db_helper.get_user_notes(), use_container_width=True)
    else:
        st.header('Logg in to your account to add or see your notes. ')


def show_tabs():
    custom_css()
    tabs = st.tabs(tabs_options)
    with tabs[0]:
        show_tab0()
    with tabs[1]:
        show_tab1()
    with tabs[2]:
        show_tab2()


def get_localizator():
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'

    _ = gettext.gettext

    try:
        # Important - languages=[language] have to be passed as a list, won't work without []
        localizator = gettext.translation('base', localedir='locales', languages=[st.session_state['language']])
        localizator.install()
        _ = localizator.gettext
    except Exception as e:
        st.error(e)
    return _

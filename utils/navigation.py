import numpy as np
import pandas as pd
import streamlit as st

from utils.localization_helper import get_localizator
from utils.streamlit_demos import sliders, chart, selectbox, multiselect, checkbox, file_uploader, progress, form, \
    session_demo

from utils.authorization import authorization_check
from database.database_helper import DatabaseHelper

db_helper = DatabaseHelper('database/data/funga_data.db')
sidebar_options = ["Hello", "Button", "Sliders demo", "Chart demo", "Select box demo", "Multiselect demo",
                   "Checkbox demo", "File uploader demo", "Progress demo", "Form demo", "Session demo"]


def show_main_menu(_):
    st.sidebar.page_link("Home_Page.py", label=_("Home"), icon="🏠")
    with st.sidebar.expander("Fun and games 🕹️", expanded=True):
        st.page_link("pages/1_Biomorphs.py", label=_("Biomorphs"), icon="😶️")
        st.page_link("pages/3_Ice-cream_Tycoon.py", label=_("Ice-cream Tycoon"), icon="🍦️")
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


def show_best_tsp():
    _ = get_localizator()
    st.write(_('Best TSP results:'))
    best_tsp_results = pd.DataFrame(db_helper.get_best_tsp_activities(3))
    best_tsp_results.index = np.arange(1, len(best_tsp_results) + 1)  # index from 1

    try:
        best_tsp_results.columns = [_('Type'), _('User'), _('Distance'), _('Route'), _('Parameters')]
    except ValueError:
        pass
    st.dataframe(best_tsp_results)


def show_tab1():
    _ = get_localizator()
    if st.session_state["authentication_status"]:
        st.write(_('Your TSP results:'))
        user_tsp_results = pd.DataFrame(db_helper.get_user_tsp_activities(st.session_state['username']))
        user_tsp_results.index = np.arange(1, len(user_tsp_results) + 1)  # index from 1
        user_tsp_results.columns = [_('Type'), _('Distance'), _('Route'), _('Parameters')]

        # Extract num_cities using Pandas
        try:
            user_tsp_results['num_cities'] = user_tsp_results[_('Route')].astype(str).str.extract(
                r"'number_of_cities': (\d+)").astype(int)
            print(user_tsp_results['num_cities'])
        except ValueError:
            pass

        st.dataframe(user_tsp_results)
        show_best_tsp()
    else:
        st.header(_('Logg in to your account to see your activities. '))
        show_best_tsp()


def show_tab2():
    _ = get_localizator()
    if st.session_state["authentication_status"]:

        note_task_type = st.radio(
            " ",
            [_(":green[**Add a note**]"), _(":red[**Remove notes**]")])

        if note_task_type == _(":green[**Add a note**]"):

            # problem with text_input: "press enter to apply" can't be translated, can be disabled at best
            note = st.text_input(_('Write below and press ENTER to add:'), '')
            if note != '':
                db_helper.add_note(st.session_state['username'], note)

            st.title("NOTES:")
            df = pd.DataFrame(db_helper.get_user_notes(), columns=("Date", "Note"))
            df.index = np.arange(1, len(df) + 1)  # index from 1
            st.table(df)

        if note_task_type == _(":red[**Remove notes**]"):

            df = pd.DataFrame(db_helper.get_user_notes(), columns=("Date", "Note"))
            df.index = np.arange(1, len(df) + 1)  # index from 1
            st.table(df)

            selected_indices = st.multiselect(_('Select notes to delete:'), df.index,
                                              placeholder=_('Select notes to delete'))
            selected_rows = df.loc[selected_indices]
            st.table(selected_rows)
            if st.button(_('Delete selected notes')):
                db_helper.delete_notes(st.session_state['username'], selected_rows['Note'])
                st.rerun()
    else:
        st.header(_('Logg in to your account to add or see your notes. '))


def show_tabs():
    _ = get_localizator()
    task_type = st.radio(
        " ",
        [_(":blue[**Account**]"), _(":orange[**Activities**]"), _(":green[**Notes**]")],
        captions=[_("Manage your account."), _("Check your activity."), _("Manage your notes.")], horizontal=True)

    if task_type == _(":blue[**Account**]"):
        show_tab0()
    if task_type == _(":orange[**Activities**]"):
        show_tab1()
    if task_type == _(":green[**Notes**]"):
        show_tab2()

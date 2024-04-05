import streamlit as st
import gettext
from utils.streamlit_demos import sliders, chart, selectbox, multiselect, checkbox, file_uploader, progress, form, \
    session_demo

sidebar_options = ["Hello", "Button", "Sliders demo", "Chart demo", "Select box demo", "Multiselect demo",
                   "Checkbox demo", "File uploader demo", "Progress demo", "Form demo", "Session demo"]

tabs_options = ["Tab 1 ", "Tab 2 ", "Tab 3 ", "Tab 4 ", "Tab 5"]


@st.cache_resource
def show_main_menu(_):
    st.sidebar.page_link("Home_Page.py", label=_("Home"), icon="🏠")
    with st.sidebar.expander("Fun and games 🕹️", expanded=True):
        st.page_link("pages/1_Biomorphs.py", label=_("Biomorphs"), icon="😶️")
        st.page_link("pages/2_Shapevo.py", label=_("Shapevo"), icon="💠️")
        st.page_link("pages/3_TSP.py", label=_("TSP"), icon="🗺️️")
    st.sidebar.page_link("pages/4_Theory.py", label=_("Theory"), icon="📚")
    st.sidebar.page_link("pages/About.py", label=_("About"), icon="❓")


@st.cache_resource
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


def show_tabs():
    tabs = st.tabs(tabs_options)
    with tabs[0]:
        st.header('Hello')
        st.write('Hello funga world!')
        st.write("st.session_state object:", st.session_state)
    with tabs[1]:
        st.header('Hello')
        # show_change_password_form(gv.authenticator, gv.config)


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

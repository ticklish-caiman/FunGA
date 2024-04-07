import streamlit as st
import gettext

from utils.custom_css import custom_css
from utils.streamlit_demos import sliders, chart, selectbox, multiselect, checkbox, file_uploader, progress, form, \
    session_demo
import streamlit_authenticator as stauth
from database.database_helper import DatabaseHelper

db_helper = DatabaseHelper('database/data/funga_data.db')
_ = gettext.gettext
sidebar_options = ["Hello", "Button", "Sliders demo", "Chart demo", "Select box demo", "Multiselect demo",
                   "Checkbox demo", "File uploader demo", "Progress demo", "Form demo", "Session demo"]

tabs_options = ["Account ", "Tab 2 ", "Tab 3 ", "Tab 4 ", "Tab 5"]


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
    st.success(
        'Account allows you to save your results and create your own experiments! It\'s free and always will be! 😁')
    col3, col4 = st.columns(2)

    def show_logged_user_menu(authenticator: stauth):
        # use .sidebar only in the top container, same goes for location='sidebar' (use 'main')
        col1, col2 = st.sidebar.columns(2)
        st.info(f'Logged in as 💻 {st.session_state["name"]}')
        with col1:
            # logout error (KeyError: 'cookie_name') is possibly caused by add-blockers
            # it's a known issue https://github.com/mkhorasani/Streamlit-Authenticator/issues/134
            # the author promises to fix this in v0.3.2.
            # a temporary solution is to catch the KeyError
            try:
                authenticator.logout(button_name='Logout 🚀', location='main')  # Logout button
            except KeyError:
                st.session_state["authentication_status"] = None
        with col2:
            st.info(f'💻 {st.session_state["name"]}')

        # Update account details
        # For authenticator.update_user_details to properly display within expander in sidebar - use location='main'
        with col4:
            try:
                authenticator.logout(button_name='Logout 🚀', location='main', key='logout_button1')  # Logout button
            except KeyError:
                st.session_state["authentication_status"] = None
            with st.expander("🛠️ Change name/email"):
                if st.session_state["authentication_status"]:
                    try:
                        if authenticator.update_user_details(st.session_state["username"]):
                            db_helper.update_credentials_in_database(authenticator.credentials,
                                                                     st.session_state["username"])
                            # TODO success message should be visible after the refresh
                            st.success('Change saved successfully ✔️')

                    except Exception as e:
                        st.error(e)

            # Password change
            # For authenticator.reset_password to properly display within expander in sidebar - use location='main'
            st.empty()
            with st.expander("🔒 Change password"):
                if st.session_state["authentication_status"]:
                    try:
                        if authenticator.reset_password(st.session_state["username"], location='main',
                                                        fields={'Form name': '', 'Reset': 'Change'}):
                            db_helper.update_credentials_in_database(authenticator.credentials,
                                                                     st.session_state["username"])
                            st.success('Password modified successfully ✔️')

                    except Exception as e:
                        st.error(e)

    def show_register_form(authenticator: stauth):
        st.warning('Don\'t have an account? Register below.')
        try:
            email_of_registered_user, _, _ = authenticator.register_user(
                preauthorization=False, fields={'Form name': 'Register User 📝',
                                                'Email': 'Email',
                                                'Username': 'Username',
                                                'Password': 'Password',
                                                'Repeat password': 'Repeat password',
                                                'Register': 'Register'})
            db_helper.safe_credentials_to_database(authenticator.credentials)
            if email_of_registered_user:
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)

    def authentication(authenticator: stauth):
        # Authentication logic
        if st.session_state["authentication_status"]:
            show_logged_user_menu(authenticator)

        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')

        # Register form
        if not st.session_state["authentication_status"]:
            with col4:
                show_register_form(authenticator)

    def show_login_form():

        # This eliminates the gap above the login form, but also makes info/error messages disappear
        # st.markdown("""
        #     <style>
        # .st-emotion-cache-pchmfb{
        # display: none
        # }
        #     </style>
        # """, unsafe_allow_html=True)

        st.title("")
        st.write("")

        # Load cookie config from the database
        config = db_helper.get_cookie_config()
        # Authenticator initialization
        authenticator = stauth.Authenticate(
            db_helper.get_all_user_credentials(),
            config['name'],
            config['cookie_key'],
            int(config['expiry_days']),
            None
        )

        # Login widget
        authenticator.login(fields={'Form name': 'Login 🔑',
                                    'Username': _('Username'),
                                    'Password': _('Password'),
                                    'Login': 'Login'})
        authentication(authenticator)

    with col3:
        show_login_form()


def show_tabs():
    custom_css()
    tabs = st.tabs(tabs_options)
    with tabs[0]:
        show_tab0()
    with tabs[1]:
        st.header('Hello')
        st.write('Hello funga world!')
        st.write("st.session_state object:", st.session_state)

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

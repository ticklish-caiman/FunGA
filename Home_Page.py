import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth

import gettext
from database.database_helper import DatabaseHelper

from utils.navigation import show_sidebar, show_tabs, show_main_menu
from utils.custom_css import custom_tabs_css

_ = gettext.gettext
st.set_page_config(page_title="FunGA", page_icon='🍄')

custom_tabs_css()
db_helper = DatabaseHelper('database/data/funga_data.db')

if 'language' not in st.session_state:
    st.session_state['language'] = 'en'

if 'language_selected' not in st.session_state:
    st.session_state['language_selected'] = 'en'

lang_menu = st.sidebar.popover(_('🌍 Language/Język'), use_container_width=True)
language = st.session_state.get('language')

# ISSUE: when using index=language_index (necessary to not go back to en when switching pages) in the second language
# switch, it is necessary to click twice on the radio option FIX: on_change switch the language and force page rerun
# - downside: after returning to Home_Page language returns to 'eng'
# - bigger downside: it breaks login form
# def fix_double_click():
#     if st.session_state['language_selected'] != st.session_state['language']:
#         if st.session_state['language_selected'] == 'pl':
#             st.session_state['language'] = 'pl'
#         else:
#             st.session_state['language'] = 'en'
#         st.rerun()


st.session_state['language'] = lang_menu.radio('Language', ['en', 'pl'], label_visibility='collapsed',
                                               index=0 if language == 'en' else 1, captions=['💂 English', '🥟 Polski'])

# Apply translation only if needed
if st.session_state['language'] != 'en':
    try:
        # Important - languages=[language] have to be passed as a list, won't work without []
        localizator = gettext.translation('base', localedir='locales', languages=[st.session_state['language']])
        localizator.install()
        _ = localizator.gettext
    except Exception as e:
        st.error(e)

show_main_menu(_)
st.sidebar.markdown("""<hr style="height:2px;border:none;background-color:#996;margin-top:1px;margin-bottom:1px" /> """,
                    unsafe_allow_html=True)


def show_logged_user_menu(authenticator: stauth):
    # use .sidebar only in the top container, same goes for location='sidebar' (use 'main')
    col1, col2 = st.sidebar.columns(2)
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
        st.markdown(f'💻 {st.session_state["name"]}')

    # Update account details
    # For authenticator.update_user_details to properly display within expander in sidebar - use location='main'
    with st.sidebar.expander("🛠️ Change name/email"):
        if st.session_state["authentication_status"]:
            try:
                if authenticator.update_user_details(st.session_state["username"]):
                    db_helper.update_credentials_in_database(authenticator.credentials,
                                                             st.session_state["username"])
                    # TODO success message should be visible after the refresh
                    st.sidebar.success('Change saved successfully ✔️')

            except Exception as e:
                st.sidebar.error(e)

    # Password change
    # For authenticator.reset_password to properly display within expander in sidebar - use location='main'
    with st.sidebar.expander("🔒 Change password"):
        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"], location='main',
                                                fields={'Form name': '', 'Reset': 'Change'}):
                    db_helper.update_credentials_in_database(authenticator.credentials,
                                                             st.session_state["username"])
                    st.sidebar.success('Password modified successfully ✔️')

            except Exception as e:
                st.sidebar.error(e)


def show_register_form(authenticator: stauth):
    st.sidebar.warning('Don\'t have an account? Register below.')
    try:
        email_of_registered_user, _, _ = authenticator.register_user(
            preauthorization=False, location='sidebar')
        db_helper.safe_credentials_to_database(authenticator.credentials)
        if email_of_registered_user:
            st.sidebar.success('User registered successfully')
    except Exception as e:
        st.sidebar.error(e)


def authentication(authenticator: stauth):
    # Authentication logic
    print(st.session_state["authentication_status"])
    if st.session_state["authentication_status"]:
        show_logged_user_menu(authenticator)

    elif st.session_state["authentication_status"] is False:
        st.sidebar.error('Username/password is incorrect')

    # Register form
    if not st.session_state["authentication_status"]:
        show_register_form(authenticator)


def show_login_form():
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
    authenticator.login(location='sidebar', fields={'Form name': 'Login',
                                                    'Username': _('Username'),
                                                    'Password': _('Password'),
                                                    'Login': 'Login'})
    authentication(authenticator)


show_login_form()

# Setting custom CSS creates unwanted spacing, below hack fixes it
#   See: https://github.com/streamlit/streamlit/issues/6605
# TODO: that won't do - after logging in text gets too high, it's ok after page refresh
#       easy fix may be impossible as it behaves differently in different conditions.
height_hack = '''
<script>
    var hide_me_list = window.parent.document.querySelectorAll('iframe');
    for (let i = 0; i < hide_me_list.length; i++) {
        if (hide_me_list[i].height == 0) {
            hide_me_list[i].parentNode.style.height = 0;
            hide_me_list[i].parentNode.style.marginBottom = '-4rem'; // adjust accordingly
        };
    };
</script>
'''
components.html(height_hack, height=0)

st.title("Welcome to FunGA! ")
if st.session_state["authentication_status"]:
    # show_sidebar()
    # show_tabs()
    st.write('Now you are logged in. You can save your results and create your own experiments!')
else:
    st.write('You are not logged in, but you can still use the app.')
    st.write('Account allows you to save your results and create your own experiments!')
    st.write('👈 Log in or create an account. It\'s free and always will be! 😁')
st.image('img/funGA_logo1.jpg')
# Thing to consider: sidebar-less layout: https://discuss.streamlit.io/t/version-1-32-0/64158/2

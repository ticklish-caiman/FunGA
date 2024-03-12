import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import yaml

import gettext

from utils.navigation import show_sidebar, show_tabs
from utils.custom_css import custom_tabs_css

st.set_page_config(page_title="FunGA", page_icon='🍄')
custom_tabs_css()

# To generate pot file use:
#
_ = gettext.gettext
with st.sidebar.expander('🌍 Language/Język'):
    # label_visibility='collapsed' doesn't leave empty space in place of the label TODO: aliases
    language = st.radio('Language', ['en', 'pl'], label_visibility='collapsed')
try:
    # Important - languages=[language] have to be passed as a list, won't work without []
    localizator = gettext.translation('base', localedir='locales', languages=[language])
    localizator.install()
    _ = localizator.gettext
except Exception as e:
    st.error(e)

print(_('Sample'))


# ['💂 English', '🥟 Polski']
# 🗽

def show_login_form():
    with open('configs/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    # Authenticator initialization
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    # Guest account TODO

    # Login widget
    authenticator.login(location='sidebar', fields={'Form name': 'Login',
                                                    'Username': _('Username'),
                                                    'Password': _('Password'),
                                                    'Login': 'Login'})
    st.sidebar.text(_("not working"))
    # Authentication logic
    if st.session_state["authentication_status"]:
        # use .sidebar only in the top container, same goes for location='sidebar' (use 'main')
        col1, col2 = st.sidebar.columns(2)
        with col1:
            authenticator.logout(button_name='Logout 🚀', location='main')  # Logout button
        with col2:
            st.markdown(f'💻 {st.session_state["name"]}')
            # name = f'💻 {st.session_state["name"]}'
            # st.markdown(f"""<p style="text-align: right">{name}</p>""", True, help='Logged in user')

    elif st.session_state["authentication_status"] is False:
        st.sidebar.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.sidebar.info('Please enter your username and password')

    # Register form
    if not st.session_state["authentication_status"]:
        st.sidebar.warning('Don\'t have an account? Register below.')
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
                preauthorization=False, location='sidebar')
            with open('configs/config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            if email_of_registered_user:
                st.sidebar.success('User registered successfully')
        except Exception as e:
            st.error(e)

    # Update account details
    # For authenticator.update_user_details to properly display within expander in sidebar - use location='main'
    with st.sidebar.expander("🛠️ Change name/email"):
        if st.session_state["authentication_status"]:
            try:
                if authenticator.update_user_details(st.session_state["username"]):
                    with open('configs/config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
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
                    with open('configs/config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    st.sidebar.success('Password modified successfully ✔️')

            except Exception as e:
                st.sidebar.error(e)


show_login_form()
st.image('img/funGA_logo1.jpg')

if st.session_state["authentication_status"]:
    show_sidebar()
    show_tabs()

# if 'kg' not in st.session_state:
#     st.session_state['kg'] = 0.1
# if 'lbs' not in st.session_state:
#     st.session_state['lbs'] = 0.2
#
# # Necessary to prevent streamlit from wiping out session_state when the widget gets closed/hidden
# st.session_state.kg = st.session_state.kg
# st.session_state.lbs = st.session_state.lbs

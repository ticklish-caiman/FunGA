import streamlit as st
import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import yaml

from utils.navigation import show_sidebar, show_tabs
from utils.custom_css import custom_tabs_css

st.set_page_config(page_title="FunGA")
custom_tabs_css()


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
    # Guest account

    # Login widget
    authenticator.login(location='sidebar')
    # Authentication logic
    if st.session_state["authentication_status"]:
        # use .sidebar only in the top container, same goes for location='sidebar' (use 'main')
        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.write('')
            st.markdown(f'💻 {st.session_state["name"]}', help='Logged in user')
        with col2:
            authenticator.logout(button_name='Logout 🚀', location='main')  # Logout button
        st.title('Some content')
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

    # Password change
    # For authenticator.reset_password to properly display within expander in sidebar - use location='main'
    with st.sidebar.expander("⚙️ Change password"):
        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"], location='main'):
                    with open('configs/config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    st.sidebar.success('Password modified successfully')

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
# # Necessary to prevent streamlit from wiping out session_state when widget gets closed/hidden
# st.session_state.kg = st.session_state.kg
# st.session_state.lbs = st.session_state.lbs

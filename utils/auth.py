import streamlit as st
import yaml


def show_login_form(authenticator):
    # Login widget
    authenticator.login()

    # Authentication logic
    if st.session_state["authentication_status"]:
        st.sidebar.write(f'*{st.session_state["name"]}*')
        authenticator.logout(location='sidebar')  # Logout button
        st.title('Some content')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')


def show_change_password_form(authenticator, config):
    # Password change
    if st.session_state["authentication_status"]:
        try:
            if authenticator.reset_password(st.session_state["username"]):
                with open('configs/config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

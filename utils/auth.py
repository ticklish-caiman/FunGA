import streamlit as st
import yaml


def show_login_form(authenticator):
    # Authentication logic
    if st.session_state["authentication_status"]:
        st.sidebar.write(f'*{st.session_state["name"]}*')
        authenticator.logout(location='sidebar')  # Logout button
        st.title('Some content')
    elif st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.info('Please enter your username and password')
    # Login widget
    authenticator.login()


def show_register_form(authenticator, config):
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
            preauthorization=False)
        with open('../config.yaml', 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        if email_of_registered_user:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)


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

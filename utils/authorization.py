import streamlit as st
import streamlit_authenticator as stauth
import gettext

from database.database_helper import DatabaseHelper
from utils.localization_helper import get_localizator

_ = gettext.gettext
db_helper = DatabaseHelper('database/data/funga_data.db')


def authorization_check():
    col3, col4 = st.columns(2)

    def show_logged_user_menu(authenticator: stauth):
        _ = get_localizator()
        # use .sidebar only in the top container, same goes for location='sidebar' (use 'main')
        col1, col2 = st.sidebar.columns(2)
        st.info(_('Logged in as ') + f'💻 {st.session_state["name"]}')
        with col1:
            # logout error (KeyError: 'cookie_name') is possibly caused by add-blockers
            # it's a known issue https://github.com/mkhorasani/Streamlit-Authenticator/issues/134
            # the author promises to fix this in v0.3.2.
            # a temporary solution is to catch the KeyError
            # update: v0.3.2 was released,
            # but it introduced many problems for current FunGA implementation
            try:
                authenticator.logout(button_name=_('Logout 🚀'), location='main')  # Logout button
            except KeyError:
                st.session_state["authentication_status"] = None
        with col2:
            st.info(f'💻 {st.session_state["name"]}')
        # Update account details
        # For authenticator.update_user_details to properly display within expander in sidebar - use location='main'
        with col4:
            with st.expander(_("🛠️ Change name/email")):
                if st.session_state["authentication_status"]:
                    try:
                        if authenticator.update_user_details(st.session_state["username"],
                                                             fields={'Form name': '',
                                                                     'Field': _('Change:'), 'Name': _('Name'),
                                                                     'Email': 'Email', 'New value': _('New value'),
                                                                     'Update': _('Update')}):
                            db_helper.update_credentials_in_database(authenticator.credentials,
                                                                     st.session_state["username"])
                            # TODO success message should be visible after the refresh
                            st.success(_('Change saved successfully ✔️'))

                    except Exception as e:
                        st.error(e)

            # Password change
            # For authenticator.reset_password to properly display within expander in sidebar - use location='main'
            st.empty()
            with st.expander(_("🔒 Change password")):
                if st.session_state["authentication_status"]:
                    try:
                        if authenticator.reset_password(st.session_state["username"], location='main',
                                                        fields={'Form name': '',
                                                                'Current password': _('Current password'),
                                                                'New password': _('New password'),
                                                                'Repeat password': _('Repeat password'),
                                                                'Reset': _('Reset')}):
                            db_helper.update_credentials_in_database(authenticator.credentials,
                                                                     st.session_state["username"])
                            st.success(_('Password modified successfully ✔️'))

                    except Exception as e:
                        st.error(e)

            try:
                authenticator.logout(button_name='Logout 🚀', location='main', key='logout_button1')  # Logout button
            except KeyError:
                st.session_state["authentication_status"] = None

    def show_register_form(authenticator: stauth):
        _ = get_localizator()
        st.warning(_('Don\'t have an account? Register below.'))
        try:
            email_of_registered_user, _, _ = authenticator.register_user(
                preauthorization=False, fields={'Form name': _('Register User 📝'),
                                                'Email': 'Email',
                                                'Username': _('Login'),
                                                'Name': _('Name (public)'),
                                                'Password': _('Password'),
                                                'Repeat password': _('Repeat password'),
                                                'Register': _('Register')})
            db_helper.safe_credentials_to_database(authenticator.credentials)
            if email_of_registered_user:
                st.success(_('User registered successfully'))
        except Exception as e:
            st.error(e)

    def authentication(authenticator: stauth):
        # Authentication logic
        if st.session_state["authentication_status"]:
            show_logged_user_menu(authenticator)

        elif st.session_state["authentication_status"] is False:
            st.error(_('Login/password is incorrect'))

        # Register form
        if not st.session_state["authentication_status"]:
            with col4:
                show_register_form(authenticator)

    def show_login_form():
        _ = get_localizator()
        st.success(
            _('Account allows you to save your results and create your own experiments! 😁'))

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
        authenticator.login(fields={'Form name': _('Login 🔑'),
                                    'Username': _('Login'),
                                    'Password': _('Password'),
                                    'Login': 'Login'})
        authentication(authenticator)

    with col3:
        show_login_form()

import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import yaml
from streamlit import set_page_config

# set_page_config has to be here, before every other action triggerd by other imports
set_page_config(page_title="FunGA")

with open('configs/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
# For some reason, creating authenticator above the functions in auth.py cases it to not initiate properly.
# Creating it twice for each function raises "multiple widgets with same key" error.
# Therefore, to be able to separate login/password_reset/account_creation forms
# we need to pass authenticator as a separate variable
# I'm getting very weird behavior when doing it this way:
# KeyError: 'st.session_state has no key "authentication_status".
# Sometimes app throws above error, but after rerun it works -
# I think closing the browser tab before reset fixes the problem
# NO IT DOESN'T WORK AFTER REFRESHING THE PAGE!

# Authenticator initialization
# global authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

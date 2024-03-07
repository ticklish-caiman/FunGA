import streamlit_authenticator as stauth
from yaml.loader import SafeLoader
import yaml

with open('configs/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
# For some reason creating authenticator above the functions in auth.py cases it to not initiate properly.
# Creating it twice for each function raise "multiple widgets with same key" error.
# Therefore, to be able to separate login/password_reset/account_creation forms
# we need to pass authenticator from separate file

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

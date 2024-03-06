import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from utils.streamlit_demos import sliders, chart, selectbox, multiselect, checkbox, file_uploader, progress, form, \
    session_demo, session_storage

st.set_page_config(page_title="FunGA")
# layout.layout_demo()

sidebar_options = ["Hello", "Button", "Sliders demo", "Chart demo", "Select box demo", "Multiselect demo",
                   "Checkbox demo", "File uploader demo", "Progress demo", "Form demo", "Session demo"]
sidebar = st.sidebar.selectbox('Select your', sidebar_options)

if 'kg' not in st.session_state:
    st.session_state['kg'] = 0.1
if 'lbs' not in st.session_state:
    st.session_state['lbs'] = 0.2

# Necessary to prevent streamlit from wiping out session_state when widget gets closed/hidden
st.session_state.kg = st.session_state.kg
st.session_state.lbs = st.session_state.lbs


# TODO - as the wiped session_state problem is solved, new one emerged:
# TODO - why the data from "Streamlit_elements.py" persist without this trick?
#  It's not so much of a problem, but an opportunity - maybe reassigning each key on every page will be unnecessary


def show_sidebar():
    if sidebar == "Hello":
        st.write('Hello funga world!')
        st.write("st.session_state object:", st.session_state)

        # Authenticator initialization
        with open('configs/config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )

        # Login widget
        authenticator.login()

        # Authentication logic
        if st.session_state["authentication_status"]:
            authenticator.logout()
            st.write(f'Welcome *{st.session_state["name"]}*')
            st.title('Some content')
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')

        # Password reset
        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"]):
                    with open('configs/config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    st.success('Password modified successfully')
            except Exception as e:
                st.error(e)

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


show_sidebar()

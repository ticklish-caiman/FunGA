import streamlit as st

from utils.navigation import show_main_menu, get_localizator
_ = get_localizator()
st.set_page_config(page_title=_("FunGA - About"), page_icon='❓')


show_main_menu(_)

st.header('100Commitów', divider=True)
st.text(_('This project takes part in:'))
st.markdown(
    f"""[<img src="https://100commitow.pl/img/100-comittow_long.png" width=400px >](https://100commitow.pl/)""",
    True)
st.text('Competition organized by:')
st.markdown(
    f"""[<img src="https://100commitow.pl/img/devmentors-logo.png" width=400px 
    style="background-color:grey" >](https://devmentors.io/)""",
    True)
st.divider()

st.header('About me', divider=True)

st.header('Contact', divider=True)

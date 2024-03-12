import streamlit as st
import gettext

_ = gettext.gettext
try:
    # Important - languages=[language] have to be passed as a list, won't work without []
    localizator = gettext.translation('base', localedir='locales', languages=[st.session_state['language']])
    localizator.install()
    _ = localizator.gettext
except Exception as e:
    st.error(e)

st.set_page_config(page_title="FunGA - Theory", page_icon='📚')
tabs_options = ["Natural selection", "Genetic Algorithms", "Similar approaches"]

tabs = st.tabs(tabs_options)
with tabs[0]:
    st.header(_('Hello Darwin'))
with tabs[1]:
    st.header('Hello Holland/De Jong')
with tabs[2]:
    st.header('Hello others')

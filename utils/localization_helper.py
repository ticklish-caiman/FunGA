import streamlit as st
import gettext


def get_localizator():
    if 'language' not in st.session_state:
        st.session_state['language'] = 'en'

    _ = gettext.gettext

    try:
        # Important - languages=[language] have to be passed as a list, won't work without []
        localizator = gettext.translation('base', localedir='locales', languages=[st.session_state['language']])
        localizator.install()
        _ = localizator.gettext
    except Exception as e:
        st.error(e)
    return _

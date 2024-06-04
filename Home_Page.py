import streamlit as st

import gettext

from utils.custom_css import custom_css
from utils.navigation import show_tabs, show_main_menu

_ = gettext.gettext
st.set_page_config(page_title="FunGA", page_icon='🍄')

if 'language' not in st.session_state:
    st.session_state['language'] = 'en'

if 'language_selected' not in st.session_state:
    st.session_state['language_selected'] = 'en'

lang_menu = st.sidebar.popover(_('🌍 Language/Język'), use_container_width=True)
language = st.session_state.get('language')

# ISSUE: when using index=language_index (necessary to not go back to en when switching pages) in the second language
# switch, it is necessary to click twice on the radio option FIX: on_change switch the language and force page rerun
# - downside: after returning to Home_Page language returns to 'eng'
# - bigger downside: it breaks login form
# def fix_double_click():
#     if st.session_state['language_selected'] != st.session_state['language']:
#         if st.session_state['language_selected'] == 'pl':
#             st.session_state['language'] = 'pl'
#         else:
#             st.session_state['language'] = 'en'
#         st.rerun()


st.session_state['language'] = lang_menu.radio('Language', ['en', 'pl'], label_visibility='collapsed',
                                               index=0 if language == 'en' else 1, captions=['💂 English', '🥟 Polski'])

# Apply translation only if needed
if st.session_state['language'] != 'en':
    try:
        # Important - languages=[language] have to be passed as a list, won't work without []
        localizator = gettext.translation('base', localedir='locales', languages=[st.session_state['language']])
        localizator.install()
        _ = localizator.gettext
    except Exception as e:
        st.error(e)

show_main_menu(_)
st.sidebar.markdown("""<hr style="height:2px;border:none;background-color:#996;margin-top:1px;margin-bottom:1px" /> """,
                    unsafe_allow_html=True)
custom_css()
st.title("")  # empty title makes the view jump below it at initial render
st.image('img/fung_line.png')
st.title(_("Welcome to FunGA!"))

show_tabs()

# Thing to consider: sidebar-less layout: https://discuss.streamlit.io/t/version-1-32-0/64158/2

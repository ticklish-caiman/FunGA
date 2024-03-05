import streamlit as st


# IMPORTANT: each time widget is gets hidden or closed the session_state will be wiped out!
# https://docs.streamlit.io/library/advanced-features/widget-behavior#widget-clean-up-process
# To prevent this you have to put "st.session_state.key = st.session_state.key" for every key at the top of every page.


def session_demo():
    if 'kg' not in st.session_state:
        st.session_state['kg'] = 0.1
    if 'lbs' not in st.session_state:
        st.session_state['lbs'] = 0.2

    st.title('st.session_state')

    def lbs_to_kg():
        st.session_state.kg = st.session_state.lbs / 2.2046
        # session_storage.kg = st.session_state.kg

    def kg_to_lbs():
        st.session_state.lbs = st.session_state.kg * 2.2046

    st.header('Input')
    col1, spacer, col2 = st.columns([2, 1, 2])
    with col1:
        pounds = st.number_input("Pounds:", key="lbs", on_change=lbs_to_kg)
    with col2:
        kilogram = st.number_input("Kilograms:", key="kg", on_change=kg_to_lbs)

    st.header('Output')
    st.write("st.session_state object:", st.session_state)

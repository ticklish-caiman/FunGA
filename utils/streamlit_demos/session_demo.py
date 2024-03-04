import streamlit as st

# from utils.streamlit_demos import session_storage


# It seems that "reactivity" of Streamlit renders the session basically useless -
# it gets erased even after clicking a button
# It's possible that behavior is caused by the fact that we are creating the variables
# inside a function, therefore they are created locally
# TODO experiment with session_state or find a different solution
# One work-around would be to save it in separate variable, then update it each time, and load it when necessary
# but why would we need the session_storage then? There has to be a better way.
# st.session_state.kg = session_storage.kg
# def initialize_session_state():
#     if 'kg' not in st.session_state:
#         st.session_state['kg'] = 0.1
#     if 'lbs' not in st.session_state:
#         st.session_state['lbs'] = 0.2
#
#
# initialize_session_state()

# The weirdest part is that it works once - if you change the page from "Session demo" to "Hello" it will pass the
# values, but if you change page again it will erase session_state


def session_demo():
    st.title('st.session_state')

    def lbs_to_kg():
        st.session_state.kg = st.session_state.lbs / 2.2046
        #session_storage.kg = st.session_state.kg

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

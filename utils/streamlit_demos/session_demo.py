import streamlit as st


# It seems that "reactivity" of Streamlit renders the session basically useless -
# it gets erased even after clicking a button
# It's possible that behavior is caused by the fact that we are creating the variables
# inside, therefore they are created locally
# TODO experiment with session_state or find a different solution  

def session_demo():
    st.title('st.session_state')

    def lbs_to_kg():
        st.session_state.kg = st.session_state.lbs / 2.2046

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

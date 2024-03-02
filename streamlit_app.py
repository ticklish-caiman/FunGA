import streamlit as st

st.write('Hello funga world!')

st.header('First funga button')

if st.button('Answer me!'):
    st.write('Fun with Genetic Algorithms!')
else:
    st.write('What is FunGa?')

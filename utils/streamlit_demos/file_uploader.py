import streamlit as st
import pandas as pd


# https://30days.streamlit.app/?challenge=Day18
def file_uploader_demo():
    st.title('st.file_uploader')

    st.subheader('Input CSV')
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.subheader('DataFrame')
        st.write(df)
        st.subheader('Descriptive Statistics')
        st.write(df.describe())
    else:
        st.info('☝️ Upload a CSV file')

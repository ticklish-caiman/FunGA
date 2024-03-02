import streamlit as st
import pandas as pd
import numpy as np


# https://30days.streamlit.app/?challenge=Day9
def chart_demo():
    st.header('Line chart')

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.line_chart(chart_data)

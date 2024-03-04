import streamlit as st
import numpy as np
import pandas as pd
from time import time

st.title('st.cache')

# Using cache
a0 = time()
st.subheader('Using st.cache')


@st.cache_data
def load_data_a():
    df = pd.DataFrame(
        np.random.rand(2000000, 10),
        columns=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    )
    return df


st.write(load_data_a())
a1 = time()
st.info(a1 - a0)

# Not using cache
b0 = time()
st.subheader('Not using st.cache')


def load_data_b():
    df = pd.DataFrame(
        np.random.rand(2000000, 10),
        columns=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    )
    return df


st.write(load_data_b())
b1 = time()
st.info(b1 - b0)

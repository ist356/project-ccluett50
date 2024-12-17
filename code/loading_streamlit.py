import streamlit as st
import pandas as pd
import numpy as np

st.title('My first app')

st.write("Here's our first attempt at using data to create a table:")
data = pd.read_csv('./cache/filtered_odds.csv')
df = pd.DataFrame(data)
st.write(df)
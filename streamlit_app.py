import streamlit as st

# import pandas as pd

# df = pd.read_csv("2021-05-24.csv")
x = st.slider("x")  # 👈 this is a widget
st.write(x, "squared is", x * x)

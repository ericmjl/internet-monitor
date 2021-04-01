import streamlit as st
from tinydb import TinyDB
from pathlib import Path
from lib import to_dataframe, measure_speed, log_data
import matplotlib.pyplot as plt


db = TinyDB(path=Path.home() / ".speedtest.db")


def load_dataframe():
    df = to_dataframe(db)
    df = df.set_index("datetime")
    return df


st.header("Internet Speed Monitor")

plot = st.empty()
plot.line_chart(data=load_dataframe())

col1, col2 = st.beta_columns([1, 1])
with col1:
    st.write("Measure internet speed.")
    measure = st.button("Measure")
    if measure:
        with st.spinner("Measuring..."):
            data = measure_speed()
            st.write(data)
            log_data(data, db)

with col2:
    st.write("Refresh the chart.")
    refresh = st.button("Refresh")
    if refresh:
        plot.line_chart(data=load_dataframe())

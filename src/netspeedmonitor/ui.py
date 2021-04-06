"""Streamlit UI."""
import socket

import matplotlib.pyplot as plt
import streamlit as st
from tendo import singleton

from netspeedmonitor.database import table_to_df
from netspeedmonitor.latency import measure_local, measure_sentinels
from netspeedmonitor.speedtest import load_db, measure_netspeed


def despine(ax):
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)


me = singleton.SingleInstance(lockfile="/tmp/netspeedmonitor_ui.lock")

db = load_db()

st.header("Internet Speed Monitor")

hostname = socket.gethostname()
st.write(
    f"""
- Host name: {hostname}
- FQDN: {socket.getfqdn()}
"""
)


chart_col1, chart_col2 = st.beta_columns([1, 1])

with chart_col1:
    speed_chart = st.empty()

with chart_col2:
    latency_chart = st.empty()


def refresh_speed_chart():
    fig, ax = plt.subplots(figsize=(5, 2))
    df = table_to_df("speed").set_index("datetime")
    df.plot(ax=ax)
    despine(ax)
    speed_chart.pyplot(fig)


def refresh_latency_chart():
    df = table_to_df("latency")
    piv = df.pivot_table(values="latency", columns=("host"), index="datetime")
    fig, ax = plt.subplots(figsize=(5, 2))
    for column in piv.columns:
        piv[column].dropna().plot(ax=ax, label=column)
    ax.legend()
    despine(ax)
    latency_chart.pyplot(fig)


refresh_speed_chart()
refresh_latency_chart()


st.sidebar.header("Control Panel")
measure = st.sidebar.button("Measure internet speed once")

if measure:
    with st.spinner("Measuring..."):
        measure_netspeed()
        measure_local()
        measure_sentinels()

refresh = st.sidebar.button("Refresh charts")
if refresh:
    refresh_speed_chart()
    refresh_latency_chart()


st.header("Error log")
try:
    errors_df = table_to_df("errors")
    st.write(errors_df)
except Exception:
    st.write("There are no errors showing up just yet!")

"""Streamlit UI."""
import socket
from functools import partial
from threading import Thread

import pandas as pd
import streamlit as st
from tendo import singleton

from netspeedmonitor.lib import (
    load_db,
    log_data,
    measure_speed,
    record_func,
    to_dataframe,
)

me = singleton.SingleInstance()


db = load_db()


def load_dataframe():
    df = to_dataframe(db)
    df = df.rename(
        {
            "download_speed": "Download Speed (Mbps)",
            "upload_speed": "Upload Speed (Mbps)",
        },
        axis=1,
    )
    return df


st.header("Internet Speed Monitor")


hostname = socket.gethostname()
st.write(
    f"""
- Host name: {hostname}
- FQDN: {socket.getfqdn()}
"""
)

plot = st.empty()
plot.line_chart(data=load_dataframe())


col1, col2, col3 = st.beta_columns([1, 1, 1])
# Allow output mutation is necessary
# so that we don't overwrite running_threads
# each time an interaction happens on the UI.
@st.cache(allow_output_mutation=True)
def init_running_processes():
    return []


running_processes = init_running_processes()
with col1:
    st.write("Background recording")
    status = st.empty()
    if len(running_processes) == 0:
        min_interval_placeholder = st.empty()
        min_interval = min_interval_placeholder.number_input(
            "Minimum Interval (minutes)", min_value=1, max_value=60
        )
        max_interval_placeholder = st.empty()
        max_interval = max_interval_placeholder.number_input(
            "Maximum Interval (minutes)", min_value=2, max_value=120
        )
        recorder_placeholder = st.empty()
        record = recorder_placeholder.button("Start recorder")
        func = partial(
            record_func, min_interval=min_interval, max_interval=max_interval
        )
        if record:
            process = Thread(target=func, daemon=True)
            process.start()
            running_processes.append(process)
            status.success(f"Recorder running in background")
            recorder_placeholder.empty()
            min_interval_placeholder.empty()
            max_interval_placeholder.empty()

    else:
        status.success(f"Recorder running in background")


with col2:
    st.write("Measure internet speed once.")
    measure = st.button("Measure")
    if measure:
        with st.spinner("Measuring..."):
            data = measure_speed()
            st.write(data)
            log_data(data, db)

with col3:
    st.write("Refresh the chart.")
    refresh = st.button("Refresh")
    if refresh:
        plot.line_chart(data=load_dataframe())


st.header("Error log")
errors = db.table("errors")
errors_df = pd.DataFrame(errors.all())
st.write(errors_df)

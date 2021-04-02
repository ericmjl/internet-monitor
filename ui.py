from functools import partial
from loguru import logger
import streamlit as st
from tinydb import TinyDB
from pathlib import Path
from lib import load_db, to_dataframe, measure_speed, log_data, record_func
from tendo import singleton
from threading import Thread, get_ident

me = singleton.SingleInstance()


db = load_db()


def load_dataframe():
    df = to_dataframe(db)
    df = df.set_index("datetime")
    df = df.rename(
        {
            "download_speed": "Download Speed (Mbps)",
            "upload_speed": "Upload Speed (Mbps)",
        },
        axis=1,
    )
    return df


st.header("Internet Speed Monitor")

plot = st.empty()
plot.line_chart(data=load_dataframe())

col1, col2, col3 = st.beta_columns([1, 1, 1])


# Allow output mutation is necessary
# so that we don't overwrite running_threads
# each time an interaction happens on the UI.
@st.cache(allow_output_mutation=True)
def init_running_threads():
    return []


running_threads = init_running_threads()
with col1:
    st.write("Background recording")
    status = st.empty()
    if len(running_threads) == 0:
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
            thread = Thread(target=func, daemon=True)
            thread.start()
            running_threads.append(thread)
            status.success("Recorder running in background")
            recorder_placeholder.empty()
            min_interval_placeholder.empty()
            max_interval_placeholder.empty()

    else:
        status.success("Recorder running in background")


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


import pandas as pd

st.header("Error log")
errors = db.table("errors")
errors_df = pd.DataFrame(errors.all())
st.write(errors_df)

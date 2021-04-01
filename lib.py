from pathlib import Path

from tinydb import TinyDB
import speedtest
from datetime import datetime
import pandas as pd


db = TinyDB(path=Path.home() / ".speedtest.db")


def measure_speed():
    try:
        st = speedtest.Speedtest()
        down_speed = st.download() / 1024 ** 2
        up_speed = st.upload() / 1024 ** 2
        data = {
            "upload_speed": int(up_speed),
            "download_speed": int(down_speed),
            "datetime": str(datetime.now()),
        }
        return data
    except Exception as e:
        data = {"error_message": str(e), "datetime": str(datetime.now())}
        return data


def log_data(data, db):
    if "error_message" in data.keys():
        errors = db.table("errors")
        errors.insert(data)
    else:
        db.insert(data)
    return db


def record_data():
    db = TinyDB(path=Path.home() / ".speedtest.db")
    data = measure_speed()
    log_data(data, db)


def to_dataframe(db):
    df = pd.DataFrame(db.all()).dropna().drop_duplicates()
    df["datetime"] = df["datetime"].astype("datetime64[ns]")
    return df


def plot_data(df):
    df["datetime"] = df["datetime"].astype("datetime64[ns]")
    df["upload_speed"] = df["upload_speed"]
    df["download_speed"] = df["download_speed"]
    df = df.set_index("datetime")
    return df.plot()

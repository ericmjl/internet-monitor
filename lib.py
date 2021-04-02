from pathlib import Path

from tinydb import TinyDB
import speedtest
from datetime import datetime
import pandas as pd
from threading import get_ident
import schedule
import time
from tendo import singleton
from loguru import logger
import time


def load_db():
    return TinyDB(path=Path.home() / ".speedtest.json")


def measure_speed():
    logger.info("Measuring internet speed!")
    try:
        st = speedtest.Speedtest()
        down_speed = st.download() / 1024 ** 2
        up_speed = st.upload() / 1024 ** 2
        data = {
            "upload_speed": int(up_speed),
            "download_speed": int(down_speed),
            "datetime": str(datetime.now()),
        }
        logger.info(data)
        return data
    except Exception as e:
        data = {"error_message": str(e), "datetime": str(datetime.now())}
        logger.info(data)
        return data


def log_data(data, db):
    if "error_message" in data.keys():
        errors = db.table("errors")
        errors.insert(data)
    else:
        db.insert(data)
    return db


def record_data():
    db = load_db()
    data = measure_speed()
    log_data(data, db)


def to_dataframe(db):
    df = pd.DataFrame(db.all()).dropna().drop_duplicates()
    df["datetime"] = df["datetime"].astype("datetime64[ns]")
    return df


def record_func(min_interval: int, max_interval: int):
    me = singleton.SingleInstance()
    logger.info(f"Thread ID: {get_ident()}")
    schedule.every(min_interval).to(max_interval).minutes.do(record_data)
    while True:
        schedule.run_pending()

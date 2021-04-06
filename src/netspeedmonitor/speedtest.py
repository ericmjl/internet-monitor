"""Code for using speedtest.net to programmatically measure internet speed."""
import threading
import time
from datetime import datetime
from threading import get_ident

import pandas as pd
import schedule
import speedtest
from loguru import logger
from tendo import singleton
from tinyrecord import transaction
from netspeedmonitor.database import load_db, log_data
import asyncio
from concurrent.futures import ThreadPoolExecutor


def record_speed():
    """Return internet speed in megabytes per second."""
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
        log_data(data, "speed")
        return data
    except Exception as e:
        data = {"error_message": str(e), "datetime": str(datetime.now())}
        logger.info(data)
        log_data(data, "speed_errors")
        return data


def measure_netspeed():
    """Wrapper function for consistency."""
    logger.info("Measuring internet speed!")
    result = record_speed()
    return result


def log_speed():
    db = load_db()
    speed = measure_netspeed()
    log_data(speed, table="speed", db=db)


def to_dataframe(db):
    df = pd.DataFrame(db.all()).dropna().drop_duplicates()
    if len(db.all()) == 0:
        db = load_db()
        df = pd.DataFrame(db.all())
    if len(df) > 0:
        df["datetime"] = df["datetime"].astype("datetime64[ns]")
    return df.set_index("datetime")


def record_func(min_interval: int, max_interval: int):
    me = singleton.SingleInstance(lockfile="/tmp/netspeedmonitor_speedtest.lock")
    logger.info(f"Thread ID: {get_ident()}")
    schedule.every(min_interval).to(max_interval).minutes.do(log_speed)
    while True:
        schedule.run_pending()


def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread(daemon=True)
    continuous_thread.start()
    return continuous_thread, cease_continuous_run

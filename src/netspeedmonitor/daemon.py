"""Background process where we run once every however often."""
import threading
import time
from typing import Callable

import schedule
from setproctitle import setproctitle

from netspeedmonitor.latency import measure_local, measure_sentinels
from netspeedmonitor.speedtest import measure_netspeed
from netspeedmonitor.utils import detachify


def schedule_measure_netspeed(interval: int):
    add_to_schedule(measure_netspeed, interval)


def schedule_measure_sentinels(interval: int):
    add_to_schedule(measure_sentinels, interval)


def schedule_measure_local(interval: int):
    add_to_schedule(measure_local, interval)


def add_to_schedule(func: Callable, interval: int):
    min_interval = max(interval - 5, 1)
    max_interval = interval + 1
    schedule.every(min_interval).to(max_interval).minutes.do(func)


def fire_and_forget(netspeed_interval, sentinel_interval, local_interval):
    """Run all measurements and forget about them."""
    setproctitle("netspeedmonitord")
    schedule_measure_netspeed(netspeed_interval)
    schedule_measure_sentinels(sentinel_interval)
    schedule_measure_local(local_interval)

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
    return cease_continuous_run

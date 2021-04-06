"""Background process where we run once every however often."""
from typing import Callable
import schedule

from netspeedmonitor.database import log_data
from netspeedmonitor.latency import measure_local, measure_sentinels, record_latency
from netspeedmonitor.speedtest import record_speed, measure_netspeed


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

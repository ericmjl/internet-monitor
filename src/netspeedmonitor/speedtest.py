"""Code for using speedtest.net to programmatically measure internet speed."""
from datetime import datetime

import speedtest
from loguru import logger
from netspeedmonitor.database import Speed, SpeedErrors, log_data


def record_speed():
    """Return internet speed in megabytes per second."""
    try:
        st = speedtest.Speedtest()
        down_speed = st.download() / 1024 ** 2
        up_speed = st.upload() / 1024 ** 2
        data = Speed(
            upload_speed=int(up_speed),
            download_speed=int(down_speed),
            datetime=datetime.now(),
        )
        logger.info(data)
        log_data(data.dict(), "speed")
        return data
    except Exception as e:
        data = SpeedErrors(error_message=str(e), datetime=datetime.now())
        logger.info(data)
        log_data(data.dict(), "speed_errors")
        return data


def measure_netspeed():
    """Measure internet speed.

    Wrapper function for consistency
    with the same family of measure_X functions in `netspeedmonitor.latency`.
    """
    logger.info("Measuring internet speed!")
    result = record_speed()
    return result

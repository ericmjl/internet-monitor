import datetime as dt
import sqlite3
from pathlib import Path
from typing import Dict, Optional

import pandas as pd
from pydantic import BaseModel, validate_arguments

tables = ["speed", "speed_errors", "latency"]


class Speed(BaseModel):
    datetime: dt.datetime
    upload_speed: float
    download_speed: float


class SpeedErrors(BaseModel):
    datetime: dt.datetime
    error_message: str


class Latency(BaseModel):
    datetime: dt.datetime
    host: str
    latency: Optional[float]
    kind: str


def load_db():
    """Load database connector."""
    con = sqlite3.connect(Path.home() / ".speedtest.db")
    return con


@validate_arguments
def table_to_df(table_name: str):
    con = load_db()
    df = pd.read_sql(f"select * from {table_name}", con=con, parse_dates=["datetime"])
    return df


@validate_arguments
def log_data(data: Dict, table: str):
    """Log one element of data to database in a given table."""
    con = load_db()
    data = pd.DataFrame(data, index=[0])
    data.to_sql(table, con, if_exists="append", index=False)


@validate_arguments
def export(table: str, fname: Path):
    """Export database to csv."""
    df = table_to_df(table)
    if not fname.suffix == ".csv":
        raise NameError(
            "For your convenience, please name your file such that "
            "it ends with the `.csv` extension!"
        )
    df.to_csv(fname)

from tinydb import TinyDB

from pathlib import Path

from tinyrecord import transaction
import pandas as pd


def load_db():
    """Load database."""
    return TinyDB(path=Path.home() / ".speedtest.json")


def log_data(data, table):
    """Log latency data to database in a given table."""
    db = load_db()
    table = db.table(table)
    with transaction(table) as tr:
        tr.insert(data)


def export(table: str, fname: Path):
    db = load_db()
    table = db.table(table)
    df = pd.DataFrame(table.all())
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
    if not fname.suffix == ".csv":
        raise NameError(
            "For your convenience, please name your file such that "
            "it ends with the `.csv` extension!"
        )
    df.to_csv(fname)

"""Netspeedmonitor CLI."""
import os
from pathlib import Path

import click
import streamlit.cli
from tabulate import tabulate
from tendo import singleton

from netspeedmonitor.daemon import fire_and_forget
from netspeedmonitor.database import export, load_db, table_to_df
from netspeedmonitor.latency import measure_local, measure_sentinels
from netspeedmonitor.speedtest import measure_netspeed


@click.group()
def main():
    pass


@main.command("app")
def main_streamlit():
    setproctitle("netspeedmonitor-ui")
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "ui.py")
    args = []
    streamlit.cli._main_run(filename, args)


@main.command("init")
def init():
    """Initialize database."""
    measure_local()
    measure_sentinels()
    measure_netspeed()


@main.command("measure")
def measure():
    """Measure internet speed and latency once."""
    me = singleton.SingleInstance(lockfile="/tmp/netspeedmonitor_cli.lock")
    measure_local()
    measure_sentinels()
    measure_netspeed()


@main.command("export")
def export_data():
    """Export data to a collection of CSV files."""
    db = load_db()
    table_names = sorted(db.tables())
    for table_name in table_names:
        table = db.table(table_name)
        output = Path(f"{table_name}.csv")
        export(table, output)


@main.command("daemon")
@click.option(
    "--netspeed", default=10, help="Time interval between internet speed pings."
)
@click.option(
    "--sentinel", default=1, help="Time interval between sentinel site pings."
)
@click.option("--local", default=1, help="Time interval between local host pings.")
def daemon(netspeed, sentinel, local):
    """Run internet speed test monitor in the background."""
    fire_and_forget(
        netspeed_interval=netspeed,
        sentinel_interval=sentinel,
        local_interval=local,
    )


@main.command("data")
@click.option(
    "--table_name",
    default=None,
    help="Table to view. If nothing is passed in, all tables are shown.",
)
@click.option("--tail", default=5, help="Display only the last N rows of each table.")
def show_database(table_name: str = None, tail: int = 10):
    """Show the data in the console."""
    table_names = ["speed", "latency", "speed_errors"]
    if table_name:
        table_names = [table_name]

    for table_name in sorted(table_names):
        try:
            df = table_to_df(table_name)
            print(f"Showing data for table `{table_name}`:")
            print(tabulate(df.tail(tail), tablefmt="fancy_grid", headers=df.columns))
        except Exception as e:
            print(e)
            pass


if __name__ == "__main__":
    main()

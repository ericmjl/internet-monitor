import click
import streamlit.cli
import os
from tendo import singleton
from pathlib import Path
from netspeedmonitor.database import export, load_db
from tabulate import tabulate
import pandas as pd
from netspeedmonitor.latency import measure_local, measure_sentinels
from netspeedmonitor.speedtest import measure_netspeed


@click.group()
def main():
    pass


@main.command("app")
def main_streamlit():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "ui.py")
    args = []
    streamlit.cli._main_run(filename, args)


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


@main.command("data")
@click.option(
    "--table_name",
    default=None,
    help="Table to view. If nothing is passed in, all tables are shown.",
)
def show_database(table_name: str = None):
    """Show the data in the console."""
    db = load_db()
    table_names = db.tables()
    if table_name:
        table_names = [table_name]

    for table_name in sorted(table_names):
        table = db.table(table_name)
        df = pd.DataFrame(table.all())
        print(table_name)
        print(tabulate(df, tablefmt="fancy_grid", headers=df.columns))


if __name__ == "__main__":
    main()

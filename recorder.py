import schedule
from lib import record_data
from tendo import singleton

me = singleton.SingleInstance()

# Program the schedule
schedule.every(1).to(2).minutes.do(record_data)

while True:
    schedule.run_pending()

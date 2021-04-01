import schedule
from lib import record_data

# Program the schedule
schedule.every(1).to(2).minutes.do(record_data)

while True:
    schedule.run_pending()

#%%
import datetime
from schedule import repeat, every, run_pending
import time

from ingestors import DaysummaryIngestor
from writers import DataWriter

if __name__ == '__main__':
    day_summary_ingestor = DaysummaryIngestor(
        writer = DataWriter, 
        coins = ["BTC", "ETH", "LTC"], 
        default_start_date=datetime.date(2021, 6, 2)
        )

    @repeat(every(1).seconds)
    def job():
        day_summary_ingestor.ingest()

    while True:
        run_pending()
        time.sleep(0.5)
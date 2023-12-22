from schedule import every, repeat, run_pending
import time
from updatedb import create_table, persist_tracks, table_itunes_data


@repeat(every(10).minutes)
def job():
    persist_tracks()


if __name__ == '__main__':
    # init DB
    create_table(table_itunes_data)
    while True:
        run_pending()
        time.sleep(10)

from schedule import every, repeat, run_pending
import time
from updatedb import create_table, persist_tracks


@repeat(every(2).minutes)
def job():
    persist_tracks()


if __name__ == '__main__':
    # init DB
    create_table()
    while True:
        run_pending()
        time.sleep(1)

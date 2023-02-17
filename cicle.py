import time
import datetime

from table_pars import reset_table

while True:
    time.sleep(0.3)
    now_time = datetime.datetime.now()
    if now_time.hour == 5 and now_time.minute == 0 and now_time.second == 10:
        reset_table()
        time.sleep(86_200)

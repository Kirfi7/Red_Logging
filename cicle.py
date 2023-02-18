import time
import datetime
import sqlite3

from cfg import CONST
from main import sender
from table_pars import reset_table

while True:
    time.sleep(0.3)
    now_time = datetime.datetime.now()
    if now_time.hour == 5 and now_time.minute == 0 and now_time.second == 10:
        database = sqlite3.connect("database.db")
        cursor = database.cursor()
        online_list = cursor.execute(f"SELECT vk_id, nick_name, time FROM main WHERE online = '{1}'").fetchall()

        uix_now = int(str(datetime.datetime.now().timestamp()).split('.')[0])
        message = "📶 Список администрации онлайн:\n"

        for admin in online_list:
            message += f"— [id{admin[0]}|{admin[1]}] | Пробыл в сети: {(uix_now - int(admin[2])) // 60}\n"
        message += "\n\n⚠️ Список онлайна полностью очищен"

        reset_table()
        sender(CONST, message)
        time.sleep(86_200)

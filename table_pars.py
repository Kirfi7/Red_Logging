import sqlite3

import gspread

from oauth2client.service_account import ServiceAccountCredentials

# db = sqlite3.connect("database.db")
# c = db.cursor()
# c.execute(f"CREATE TABLE main (nick_name TEXT, vk_id INTEGER, online INTEGER, time INTEGER)")
# db.commit()
# db.close()

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
client = gspread.authorize(creds)
sheet = client.open("ADMINS RED1").sheet1


def reset_table():
    db = sqlite3.connect('database.db')
    c = db.cursor()
    c.execute("DELETE FROM main")
    db.commit()
    db.close()

    row = sheet.col_values(7)
    for i in range(len(row)):
        try:
            integer = int(row[i])
            values = sheet.row_values(i + 1)
            array = list(values)
            db = sqlite3.connect('database.db')
            c = db.cursor()
            c.execute(f"INSERT INTO main VALUES ('{array[1]}', '{integer}', '{0}', '{0}')")
            db.commit()
            db.close()

        except ValueError:
            pass


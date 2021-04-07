from telethon import TelegramClient
import sqlite3
import time

db = sqlite3.connect('Accounts.db')
cur = db.cursor()
 
max_count_bots = 4  # сколько всего ботов

for number_account in range(1, max_count_bots):
    print("Очередь аккаунта № " + str(number_account))
    cur.execute(f"SELECT PHONE FROM Accounts WHERE ID = '{number_account}'")
    time.sleep(0.2)
    Phone = str(cur.fetchone()[0])
    print("Входим в аккаунт: " + Phone)
    cur.execute(f"SELECT PASS FROM Accounts WHERE ID = '{number_account}'")
    time.sleep(0.2)
    password = str(cur.fetchone()[0])
    print(password)
    cur.execute(f"SELECT API_ID FROM Accounts WHERE ID = '{number_account}'")
    time.sleep(0.2)
    api_id = str(cur.fetchone()[0])
    cur.execute(f"SELECT API_HASH FROM Accounts WHERE ID = '{number_account}'")
    time.sleep(0.2)
    api_hash = str(cur.fetchone()[0])
    session = str(".anon" + str(number_account))
    client = TelegramClient(session, api_id, api_hash)
    client.start()
    number_account += 1
    time.sleep(1)
    client.disconnect()
    if number_account == max_count_bots:
        print("Aккаунты активированы!")
        break

db.close()
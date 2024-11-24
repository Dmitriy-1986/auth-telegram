import sqlite3

# Открытие базы данных
conn = sqlite3.connect('telegram_auth.session')
cursor = conn.cursor()

'''
sqlite> .tables
entities      sent_files    sessions      update_state  version
'''
# Запрос данных из таблицы sessions
cursor.execute("SELECT * FROM entities")
rows = cursor.fetchall()

# Печать бинарных данных
for row in rows:
    print(row)

conn.close()

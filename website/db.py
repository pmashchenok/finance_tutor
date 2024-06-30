# Не трогать!!!!!!!!!! это только для более простого заполнения таблицы с событиями
import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE Events(
               type TEXT,
               text TEXT,
               char TEXT,
               label1 TEXT,
               value1 INTEGER,
               label2 TEXT,
               value2 INTEGER,
               label3 TEXT,
               value3 INTEGER
               );""")

lines = []
llen = 0
cur = 0
with open("events.txt") as file:
    lines = file.readlines()
    llen = len(lines)

while cur < llen:
    event_buff = []
    line = ""
    while line != "*":
        line = lines[cur].rstrip()
        event_buff.append(line)
        cur += 1
    event_buff = event_buff[:-1]
    type = event_buff[0]
    text = event_buff[1]
    char = event_buff[2]
    if type == "CHOICE":
        label1, value1 = event_buff[3].split("|")
        value1 = int(value1)
        label2, value2 = "", 0
        label3, value3 = "", 0
    else:
        label1, value1 = event_buff[3].split("|")
        value1 = int(value1)
        label2, value2 = event_buff[4].split("|")
        value2 = int(value2)
        label3, value3 = event_buff[5].split("|")
        value3 = int(value3)
    print(type, text, char, label1, value1, label2, value2, label3, value3)
    cursor.execute("INSERT INTO Events VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", (type, text, char, label1, value1, label2, value2, label3, value3))

conn.commit()

cursor.execute("""CREATE TABLE Test(
               idx INTEGER,
               text TEXT,
               label1 TEXT,
               label2 TEXT,
               label3 TEXT,
               label4 TEXT,
               answer INTEGER
               );""")

lines = []
llen = 0
cur = 0
with open("test.txt") as file:
    lines = file.readlines()
    llen = len(lines)

while cur < llen:
    event_buff = []
    line = ""
    while line != "*":
        line = lines[cur].rstrip()
        event_buff.append(line)
        cur += 1
    event_buff = event_buff[:-1]
    idx = int(event_buff[0])
    text = event_buff[1]
    label1, label2, label3, label4 = event_buff[2:-1]
    answer = event_buff[-1]

    print(idx, text, label1, label2, label3, label4, answer)
    cursor.execute("INSERT INTO Test VALUES(?, ?, ?, ?, ?, ?, ?)", (idx, text, label1, label2, label3, label4, answer))

conn.commit()
cursor.close()
conn.close()

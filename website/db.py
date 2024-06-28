# Не трогать!!!!!!!!!! это только для более простого заполнения таблицы с событиями
import sqlite3

conn = sqlite3.connect("events.db")
cursor = conn.cursor()

lines = []
llen = 0
cur = 0
with open("events.txt") as file:
    lines = file.readlines()
    llen = len(lines)

print(llen)
while cur < llen:
    print(cur)
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
    cursor.execute("INSERT INTO Events VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (type, text, char, label1, value1, label2, value2, label3, value3))

conn.commit()
cursor.close()
conn.close()
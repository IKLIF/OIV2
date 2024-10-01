import sqlite3
import json

def get_percent(back, now):
    percent = round((float(now) - float(back)) / float(now) * 100, 3)
    return percent

def istoria_out():
    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM istoria WHERE symbol = ?', (0,))
    result = cursor.fetchone()

    massiv = result[1]
    massiv = json.loads(massiv)

    conn.close()
    return massiv


def istoria_in(data):
    conn = sqlite3.connect('OI.db', check_same_thread=False)
    cursor = conn.cursor()

    json_txt = json.dumps(data)
    cursor.execute("UPDATE istoria SET data = ? WHERE symbol = ?", (json_txt, 0))
    conn.commit()

    conn.close()


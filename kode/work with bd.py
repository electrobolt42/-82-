from flask import Flask, request, jsonify, render_template_string
import sqlite3
from datetime import datetime
import plotly.graph_objects as go
import base64
from io import BytesIO

app = Flask(__name__)
DB_FILE = 'data.db'


# БД НАЧАЛО
# открытие бд
def get_db():
    conn = sqlite3.connect(DB_FILE)
    return conn
# если нет бд то создает новую

def init_table():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value REAL NOT NULL,
            recorded_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


init_table()

# записывает температурку в файл
def save_temp(value):
    conn = get_db()
    c = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('INSERT INTO readings (value, recorded_at) VALUES (?, ?)', (value, now))
    conn.commit()
    conn.close()

# отображает последнюю запись в бдшке
def get_last():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT value, recorded_at FROM readings ORDER BY id DESC LIMIT 1')
    row = c.fetchone()
    conn.close()
    return row if row else (0.0, "Нет данных")

# отображает все записи в бдшке для построения графика
def get_all_data():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id, value, recorded_at FROM readings ORDER BY id ASC')
    rows = c.fetchall()
    conn.close()
    return rows

# ср мин макс
def get_stats(rows):
    if not rows:
        return 0, 0, 0
    values = [r[1] for r in rows]
    return sum(values) / len(values), min(values), max(values)


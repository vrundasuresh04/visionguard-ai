import sqlite3
from datetime import datetime

DB_PATH = "logs/detections.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

def log_detection(label):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO detections (label, timestamp)
        VALUES (?, ?)
    """, (label, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

def get_counts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT label, COUNT(*) FROM detections GROUP BY label")
    data = cursor.fetchall()

    conn.close()

    return dict(data)
import sqlite3
import threading
from datetime import datetime, timezone, timedelta

# Thread-local storage for database connection
thread_local = threading.local()

# IST timezone (UTC+5:30)
IST = timezone(timedelta(hours=5, minutes=30))

def get_db():
    if not hasattr(thread_local, 'connection'):
        thread_local.connection = sqlite3.connect(':memory:', check_same_thread=False)
        thread_local.connection.row_factory = sqlite3.Row
        init_db(thread_local.connection)
    return thread_local.connection

def init_db(conn):
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            instructor_name TEXT NOT NULL,
            datetime DATETIME NOT NULL,
            max_slots INTEGER NOT NULL,
            available_slots INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            classes_enrolled TEXT DEFAULT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE booking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            class_id INTEGER NOT NULL,
            FOREIGN KEY (class_id) REFERENCES classes (id)
        )
    ''')
    
    # Insert sample data with proper datetime objects in IST
    now = datetime.now(IST)
    
    # Create sample datetimes relative to current time in IST
    sample_classes = [
        ('Yoga Basics', 'John Doe', now.replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)),
        ('Advanced Pilates', 'Jane Smith', now.replace(hour=18, minute=0, second=0, microsecond=0) + timedelta(days=2)),
        ('Cardio Blast', 'Mike Johnson', now.replace(hour=7, minute=30, second=0, microsecond=0) + timedelta(days=3)),
        ('Meditation', 'Sarah Wilson', now.replace(hour=19, minute=0, second=0, microsecond=0) + timedelta(days=4))
    ]
    
    cursor.execute('''
        INSERT INTO classes (name, instructor_name, datetime, max_slots, available_slots)
        VALUES 
        (?, ?, ?, 20, 15),
        (?, ?, ?, 15, 2),
        (?, ?, ?, 25, 0),
        (?, ?, ?, 30, 25)
    ''', (
        sample_classes[0][0], sample_classes[0][1], sample_classes[0][2],
        sample_classes[1][0], sample_classes[1][1], sample_classes[1][2],
        sample_classes[2][0], sample_classes[2][1], sample_classes[2][2],
        sample_classes[3][0], sample_classes[3][1], sample_classes[3][2]
    ))
    
    cursor.execute('''
        INSERT INTO users (email, name)
        VALUES 
        ('john@example.com', 'John User'),
        ('jane@example.com', 'Jane User'),
        ('mike@example.com', 'Mike User')
    ''')
    
    conn.commit()
import sqlite3
import hashlib

def create_connection():
    conn = sqlite3.connect('data/users.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            activity TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_user(name, username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO users (username, name, password) VALUES (?, ?, ?)",
                   (username, name, hash_password(password)))
    conn.commit()
    conn.close()

def get_user():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return [{'username': user[0], 'name': user[1], 'password': user[2]} for user in users]

def save_user_activity(username, activity):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_activity (username, timestamp, activity) VALUES (?, datetime('now'), ?)",
                   (username, activity))
    conn.commit()
    conn.close()

def get_user_activity(username):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, activity FROM user_activity WHERE username = ? ORDER BY timestamp DESC", (username,))
    activities = cursor.fetchall()
    conn.close()
    return [{'timestamp': activity[0], 'activity': activity[1]} for activity in activities]

# Ensure tables are created
create_table()

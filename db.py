import sqlite3
import uuid

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()
    
    
def create_user_db(username, password):
    try:
        with sqlite3.connect(DB_NAME, timeout=5) as conn:
            cursor = conn.cursor()

            user_id = str(uuid.uuid4())

            cursor.execute("""
            INSERT INTO users (id, username, password)
            VALUES (?, ?, ?)
            """, (user_id, username, password))

            return {"id": user_id, "username": username}

    except sqlite3.IntegrityError:
        return None

    except Exception as e:
        print("DB ERROR:", e)
        return None


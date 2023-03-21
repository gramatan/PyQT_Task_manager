import sqlite3
from sqlite3 import Error


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("tasks.db")
    except Error as e:
        print(e)

    if conn:
        return conn
    else:
        raise Exception("Error connecting to the database")


def create_tables(conn):
    cursor = conn.cursor()

    # Create the 'tasks' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        daily_target INTEGER,
        weekly_target INTEGER
    )
    """)

    # Create the 'logs' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY,
        task_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        start_timestamp INTEGER NOT NULL,
        stop_timestamp INTEGER NOT NULL,
        FOREIGN KEY (task_id) REFERENCES tasks (id)
    )
    """)

    conn.commit()


def init_database():
    conn = create_connection()
    create_tables(conn)
    conn.close()


if __name__ == "__main__":
    init_database()


import sqlite3

def initialize_database():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Create users table (if you haven't already)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

    # Create child_progress table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS child_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_username TEXT NOT NULL,
            subject TEXT NOT NULL,
            grade TEXT,
            attendance_percentage INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parent_student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_username TEXT NOT NULL,
            student_username TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_database()
    print("Database initialized successfully.")
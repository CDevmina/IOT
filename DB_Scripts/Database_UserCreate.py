import sqlite3

conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            password TEXT
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            admin_id TEXT PRIMARY KEY,
            password TEXT
        )
    ''')

conn.commit()
conn.close()
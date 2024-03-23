import sqlite3

conn = sqlite3.connect('D:\Work\IOT\Database/vehicle_database.db')
cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY Not Null,
            password TEXT,
            status TEXT
        )
    ''')

cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INT PRIMARY KEY Not Null,
            password TEXT
        )
    ''')

conn.commit()
conn.close()
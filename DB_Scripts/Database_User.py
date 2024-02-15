import sqlite3

def add_admin(admin_id, password):
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO admins (admin_id, password)
        VALUES (?, ?)
    ''', (admin_id, password))
    conn.commit()
    conn.close()

def add_user(user_id, password):
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, password)
        VALUES (?, ?)
    ''', (user_id, password))
    conn.commit()
    conn.close()
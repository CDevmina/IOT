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
        INSERT INTO users (user_id, password, status)
        VALUES (?, ?, ?)
    ''', (user_id, password, 'Logged Out'))
    conn.commit()
    conn.close()


def verify_admin_credentials(admin_id, password):
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM admins WHERE admin_id = ? AND password = ?
    ''', (admin_id, password))
    admin = cursor.fetchone()

    conn.close()
    return admin is not None


def verify_user_credentials(user_id, password):
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM users WHERE user_id = ? AND password = ?
    ''', (user_id, password))
    user = cursor.fetchone()

    conn.close()
    return user is not None


def get_all_users():
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id, password FROM users')  # Select both the user_id and password columns
    users = cursor.fetchall()

    conn.close()
    return users


def get_user_view():
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id, status FROM users')  # Select both the user_id and password columns
    users = cursor.fetchall()

    conn.close()
    return users


def delete_user(user_id):
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()


def get_user_status():
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT user_id, status FROM users')
    users = cursor.fetchall()

    conn.close()
    return users


def update_user_status(user_id, status):
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE users SET status = ? WHERE user_id = ?
    ''', (status, user_id))

    conn.commit()
    conn.close()

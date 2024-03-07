import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
cursor = conn.cursor()

# Create a table to store vehicle data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicles (
        license_plate TEXT PRIMARY KEY Not Null,
        vehicle_class TEXT,
        time_entered TEXT,
        time_exited TEXT,
        entrance TEXT,
        exit TEXT,
        amount int,
        average_speed int,
        report_status TEXT
    )
''')

# Commit changes and close connection
conn.commit()
conn.close()
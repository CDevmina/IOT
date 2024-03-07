import sqlite3

# Delete vehicle from database

conn = sqlite3.connect('/home/pi/IOT/Database/vehicle_database.db')
cursor = conn.cursor()

 # Delete vehicle from database and display deleted vehicle

cursor.execute('''
    Delete from vehicles WHERE license_plate = ?
''', ("",))

conn.commit()  # Commit changes
conn.close()  # Close connection after committing

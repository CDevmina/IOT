import sqlite3


def insert_vehicle(license_plate, vehicle_class, time_entered, name):
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

#Delete vehicle from database and display deleted vehicle

    entrance = cursor.execute('''
        Delete * from vehicles WHERE license_plate = ?
    ''', (license_plate,))

    conn.commit()  # Commit changes
    conn.close()   # Close connection after committing

    print(license_plate, "Has exited.")

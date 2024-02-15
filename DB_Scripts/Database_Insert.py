import sqlite3

def insert_vehicle(license_plate, vehicle_class, time_entered, name):
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

#insert Vehicle
    cursor.execute('''
        INSERT INTO vehicles (license_plate, vehicle_class, time_entered, entrance)
        VALUES (?, ?, ?, ?)
    ''', (license_plate, vehicle_class, time_entered, name))

    conn.commit()  # Commit changes
    conn.close()   # Close connection after committing

    print("The Vehicle with License Plate: ", license_plate, " Entered.")

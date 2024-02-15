import sqlite3

# Insert vehicle into database
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


# Select vehicle from database
def select_vehicle(license_plate, vehicle_class, time_entered, name):
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

#Select Vehicle and assign entrance to variable

    entrance = cursor.execute('''
        SELECT entrance FROM vehicles WHERE license_plate = ?
    ''', (license_plate,))

    conn.commit()  # Commit changes
    conn.close()   # Close connection after committing

# Delete vehicle from database
def delete_vehicle(license_plate, vehicle_class, time_entered, name):
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

#Delete vehicle from database and display deleted vehicle

    entrance = cursor.execute('''
        Delete * from vehicles WHERE license_plate = ?
    ''', (license_plate,))

    conn.commit()  # Commit changes
    conn.close()   # Close connection after committing

    print(license_plate, "Has exited.")

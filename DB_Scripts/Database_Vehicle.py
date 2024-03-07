import sqlite3


# Insert vehicle into database
def insert_vehicle(license_plate, vehicle_class, time_entered, name, report_status):
    conn = sqlite3.connect('/home/pi/IOT/Database/vehicle_database.db')
    cursor = conn.cursor()

    # insert Vehicle
    cursor.execute('''
        INSERT INTO vehicles (license_plate, vehicle_class, time_entered, entrance, report_status)
        VALUES (?, ?, ?, ?, ?)
    ''', (license_plate, vehicle_class, time_entered, name, report_status))

    conn.commit()  # Commit changes
    conn.close()  # Close connection after committing

    print("The Vehicle with License Plate: ", license_plate, " Entered.")


# Select vehicle from database
def select_vehicle(license_plate):
    conn = sqlite3.connect('/home/pi/IOT/Database/vehicle_database.db')
    cursor = conn.cursor()

    # Select Vehicle and assign entrance to variable

    vehicle = cursor.execute('''
        SELECT * FROM vehicles WHERE license_plate = ?
    ''', (license_plate,))
    vehicle = vehicle.fetchone()

    conn.commit()  # Commit changes
    conn.close()  # Close connection after committing

    return vehicle


# Delete vehicle from database
def delete_vehicle(license_plate):
    conn = sqlite3.connect('/home/pi/IOT/Database/vehicle_database.db')
    cursor = conn.cursor()

    # Delete vehicle from database and display deleted vehicle

    cursor.execute('''
        Delete from vehicles WHERE license_plate = ?
    ''', (license_plate,))

    conn.commit()  # Commit changes
    conn.close()  # Close connection after committing

    print(license_plate, "Has exited.")


# Get all vehicles from the database
def get_all_vehicles():
    conn = sqlite3.connect('/home/pi/IOT/Database/vehicle_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT license_plate, entrance, time_entered,report_status FROM vehicles')
    vehicles = cursor.fetchall()

    conn.close()
    return vehicles


def update_vehicle_status(license_plate, status):
    conn = sqlite3.connect('/home/pi/IOT/Database/vehicle_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE vehicles SET report_status = ? WHERE license_plate = ?
    ''', (status, license_plate))

    conn.commit()
    conn.close()


def check_licenseplate_exists(license_plate):
    conn = sqlite3.connect('/home/pi/IOT/Database/vehicle_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM vehicles WHERE license_plate = ?', (license_plate,))
    vehicle = cursor.fetchone()

    conn.close()
    return vehicle is not None


def entrance_app(license_plate_text, vehicle_type, strftime, localtime):
    # check if vehicle exists in the DB
    if check_licenseplate_exists(license_plate_text):
        print("Vehicle already exists in the database")
    else:
        # insert vehicle into database
        insert_vehicle(license_plate_text, vehicle_type, strftime("%Y-%m-%d %H:%M:%S", localtime()), 'Homagama', 'Normal')


def exit_app(license_plate_text):
    # check if vehicle exists in the DB
    if check_licenseplate_exists(license_plate_text):
        # delete vehicle from database
        return select_vehicle(license_plate_text)
    else:
        print("Vehicle does not exist in the database")
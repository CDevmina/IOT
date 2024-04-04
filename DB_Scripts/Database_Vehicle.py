import sqlite3

con_str = '/home/pi/IOT/Database/vehicle_database.db'

# Insert vehicle into database
def insert_vehicle(license_plate, vehicle_class, time_entered, name, report_status):
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    # insert Vehicle
    cursor.execute('''
        INSERT INTO vehicles (license_plate, vehicle_class, time_entered, entrance, report_status, status)
        VALUES (?, ?, ?, ?, ?,?)
    ''', (license_plate, vehicle_class, time_entered, name, report_status, 'In'))

    conn.commit()  # Commit changes
    conn.close()  # Close connection after committing

    print("The Vehicle with License Plate: ", license_plate, " Entered.")


# Select vehicle from database
def select_vehicle(license_plate):
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    # Select Vehicle and assign entrance to variable

    vehicle = cursor.execute('''
        SELECT * FROM vehicles WHERE license_plate = ? and Status = ?
    ''', (license_plate, 'In'))
    vehicle = vehicle.fetchone()

    conn.commit()  # Commit changes
    conn.close()  # Close connection after committing

    return vehicle


# Delete vehicle from database
def delete_vehicle(license_plate):
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    # Delete vehicle from database and display deleted vehicle

    cursor.execute('''
        Delete from vehicles WHERE license_plate = ? and Status = ?
    ''', (license_plate, 'In'))

    conn.commit()  # Commit changes
    conn.close()  # Close connection after committing

    print(license_plate, "Has exited.")


# Get all vehicles from the database
def get_all_vehicles_in():
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, license_plate, entrance, time_entered,report_status, Status,average_speed, exit, time_exited, amount FROM vehicles WHERE Status = ? ',
        ('In',))
    vehicles = cursor.fetchall()

    conn.close()
    return vehicles


def get_all_vehicles_out():
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, license_plate, entrance, time_entered,report_status, Status,average_speed, exit, time_exited, amount FROM vehicles where Status = ? ',
        ('Out',))
    vehicles = cursor.fetchall()

    conn.close()
    return vehicles


def get_all_vehicles():
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, license_plate, entrance, time_entered,report_status, Status,average_speed, exit, time_exited, amount FROM vehicles')
    vehicles = cursor.fetchall()

    conn.close()
    return vehicles


def get_vehicles():
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    cursor.execute(
        'SELECT id, license_plate, entrance, time_entered,report_status, Status FROM vehicles where Status = ? ',
        ('In',))
    vehicles = cursor.fetchall()

    conn.close()
    return vehicles


def update_vehicle_report_status(license_plate, status):
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE vehicles SET report_status = ? WHERE license_plate = ? and Status = ?
    ''', (status, license_plate, 'In'))

    conn.commit()
    conn.close()


def check_licenseplate_exists(license_plate):
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM vehicles WHERE license_plate = ? and Status = ? ', (license_plate, 'In'))
    vehicle = cursor.fetchone()

    conn.close()
    return vehicle is not None


def entrance_app(license_plate_text, vehicle_type, strftime, localtime):
    entrance = 'Homagama'

    # check if vehicle exists in the DB
    if check_licenseplate_exists(license_plate_text):
        print("Vehicle already exists in the database")
    else:
        # insert vehicle into database
        insert_vehicle(license_plate_text, vehicle_type, strftime("%Y-%m-%d %H:%M:%S", localtime()), entrance, 'Normal')
        print(f"Vehicle {license_plate_text} added to the database.")


def exit_app(license_plate_text):
    # check if vehicle exists in the DB
    if check_licenseplate_exists(license_plate_text):
        return select_vehicle(license_plate_text)
    else:
        print("Vehicle does not exist in the database")


def update_vehicle_exit(license_plate, exit):
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE vehicles SET exit = ? WHERE license_plate = ? and Status = ?
    ''', (exit, license_plate, 'In'))

    conn.commit()
    conn.close()


def update_vehicle_amount(license_plate, amount):
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE vehicles SET amount = ? WHERE license_plate = ? and Status = ?
    ''', (amount, license_plate, 'In'))

    conn.commit()
    conn.close()


def update_vehicle_speed(license_plate, speed):
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    # Format speed to two decimal places, convert to string and append "Km/h"
    speed_str = "{:.2f} Km/h".format(speed)

    cursor.execute('''
        UPDATE vehicles SET average_speed = ? WHERE license_plate = ? and Status = ?
    ''', (speed_str, license_plate, 'In'))

    conn.commit()
    conn.close()


def update_vehicle_status(license_plate, status):
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE vehicles SET status = ? WHERE license_plate = ? and Status = ?
    ''', (status, license_plate, 'In'))

    conn.commit()
    conn.close()


def update_exit_time(license_plate, exit_time):
    conn = sqlite3.connect(con_str)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE vehicles SET time_exited = ? WHERE license_plate = ? and Status = ?
    ''', (exit_time, license_plate, 'In'))

    conn.commit()
    conn.close()

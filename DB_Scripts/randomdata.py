import random
from datetime import datetime, timedelta

from DB_Scripts.Database_Vehicle import insert_vehicle, update_vehicle_status, update_vehicle_exit, \
    update_vehicle_amount, update_vehicle_speed, update_exit_time

# Define some vehicle data
vehicles = [
    ('ABC123', 'Car'),
    ('DEF456', 'Truck'),
    ('GHI789', 'Motorcycle'),
]

# Define some entrances and exits
entrances = ['kadawatha', 'Kottawa', 'Homagama', 'Kaduwela', 'colombo', 'Galle', 'Matara']
exits = ['kadawatha', 'Kottawa', 'Homagama', 'Kaduwela', 'colombo', 'Galle', 'Matara']

# Define some report statuses
report_statuses = ['Overspeeding', 'Stolen', 'Reported', 'Normal']

# Insert the vehicles into the database
for day in range(3 * 365):  # For each day in the past 3 years
    for i in range(20):  # Generate 100 records for each day
        license_plate, vehicle_class = random.choice(vehicles)
        license_plate += str(day * 100 + i)  # Make the license plate unique

        # Calculate the time_entered for this record
        time_entered = datetime.now() - timedelta(days=day, hours=random.randint(0, 23), minutes=random.randint(0, 59),
                                                  seconds=random.randint(0, 59))

        entrance = random.choice(entrances)
        report_status = random.choice(report_statuses)
        insert_vehicle(license_plate, vehicle_class, time_entered.strftime('%Y-%m-%d %H:%M:%S'), entrance,
                       report_status)

        # Update the vehicle exit
        exit = random.choice(exits)
        update_vehicle_exit(license_plate, exit)

        # Update the vehicle amount
        amount = random.randint(100, 500)  # Random amount between 100 and 500
        update_vehicle_amount(license_plate, amount)

        # Update the vehicle speed with a random float number between 50 and 120
        speed = round(random.uniform(50, 120), 2)
        update_vehicle_speed(license_plate, speed)

        # Update the vehicle exit time
        time_exited = time_entered + timedelta(
            minutes=random.randint(1, 60))  # Add a random number of minutes to the time entered
        update_exit_time(license_plate, time_exited.strftime('%Y-%m-%d %H:%M:%S'))

        # Update the vehicle status to 'Out'
        update_vehicle_status(license_plate, 'Out')

import sqlite3
from datetime import datetime, timedelta


def totalcount_graph(ax, filter1, filter2):
    # Query database
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    if filter1 == 'Hourly':
        cursor.execute('SELECT strftime("%H:00", time_entered) as Hour, COUNT(*) as Count FROM vehicles WHERE strftime("%Y-%m-%d", time_entered) = ? GROUP BY strftime("%H", time_entered)', (filter2,))
    elif filter1 == 'Daily':
        cursor.execute('SELECT strftime("%m-%d", time_entered) as Day, COUNT(*) as Count FROM vehicles WHERE strftime("%Y-%m", time_entered) = ? GROUP BY strftime("%d", time_entered)', (filter2,))
    elif filter1 == 'Monthly':
        cursor.execute('SELECT strftime("%Y-%m", time_entered) as Month, COUNT(*) as Count FROM vehicles WHERE strftime("%Y", time_entered) = ? GROUP BY strftime("%Y-%m", time_entered)', (filter2,))
    elif filter1 == 'Yearly':
        cursor.execute('SELECT strftime("%Y", time_entered) as Year, COUNT(*) as Count FROM vehicles GROUP BY strftime("%Y", time_entered)')
    else:
        raise ValueError(f"Invalid filter value: {filter1}")

    data = cursor.fetchall()
    conn.close()

    # Check if data contains at least two elements
    if not data or len(data[0]) < 2:
        print("No data or not enough columns returned from the SQL query.")
        return

    # Process data
    x = [row[0] for row in data]
    y = [int(row[1]) for row in data]  # Convert count to integer

    # Create a bar graph
    ax.bar(x, y)
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Vehicles')
    ax.set_title('Total Count of Vehicles That Entered the Expressway')

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    return data

def average_speed_graph(ax, filter1, filter2):
    # Query database
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    # Determine the start time for the last 24 hours
    start_time = datetime.now() - timedelta(hours=24)

    if filter1 == 'Hourly':
        cursor.execute('SELECT strftime("%H:00", time_entered) as Hour, AVG(average_speed) as AverageSpeed FROM vehicles WHERE time_entered > ? AND strftime("%Y-%m-%d", time_entered) = ? GROUP BY strftime("%H", time_entered)', (start_time, filter2))
    elif filter1 == 'Daily':
        cursor.execute('SELECT strftime("%Y-%m-%d", time_entered) as Day, AVG(average_speed) as AverageSpeed FROM vehicles WHERE time_entered > ? AND strftime("%Y-%m", time_entered) = ? GROUP BY strftime("%Y-%m-%d", time_entered)', (start_time, filter2))
    elif filter1 == 'Monthly':
        cursor.execute('SELECT strftime("%Y-%m", time_entered) as Month, AVG(average_speed) as AverageSpeed FROM vehicles WHERE strftime("%Y", time_entered) = strftime("%Y", "now") AND strftime("%Y", time_entered) = ? GROUP BY strftime("%Y-%m", time_entered)', (filter2,))
    elif filter1 == 'Yearly':
        cursor.execute('SELECT strftime("%Y", time_entered) as Year, AVG(average_speed) as AverageSpeed FROM vehicles WHERE strftime("%Y", time_entered) = ? GROUP BY strftime("%Y", time_entered)', (filter2,))
    else:
        raise ValueError(f"Invalid filter value: {filter1}")

    data = cursor.fetchall()
    conn.close()

    # Check if data contains at least two elements
    if not data or len(data[0]) < 2:
        print("No data or not enough columns returned from the SQL query.")
        return

    # Process data
    x = [row[0] for row in data]
    y = [row[1] for row in data]

    # Create a line graph
    ax.plot(x, y)
    ax.set_xlabel('Time')
    ax.set_ylabel('Average Speed (km/h)')
    ax.set_title('Average Speed of Vehicles That Entered the Expressway')

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    return data

def reported_vehicles_graph(ax, filter, filter2):
    # Connect to the SQLite database
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    # Determine the start time for the last 24 hours
    start_time = datetime.now() - timedelta(hours=24)

    # Execute a SQL query to fetch the count of reported vehicles
    if filter == 'Hourly':
        cursor.execute('SELECT strftime("%H:00", time_entered) as Hour, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" AND time_entered > ? GROUP BY strftime("%H", time_entered)', (start_time,))
    elif filter == 'Daily':
        cursor.execute('SELECT strftime("%Y-%m-%d", time_entered) as Day, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" AND time_entered > ? GROUP BY strftime("%Y-%m-%d", time_entered)', (start_time,))
    elif filter == 'Monthly':
        cursor.execute('SELECT strftime("%Y-%m", time_entered) as Month, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" AND strftime("%Y", time_entered) = strftime("%Y", "now") GROUP BY strftime("%Y-%m", time_entered)')
    elif filter == 'Yearly':
        cursor.execute('SELECT strftime("%Y", time_entered) as Year, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" GROUP BY strftime("%Y", time_entered)')
    else:
        raise ValueError(f"Invalid filter value: {filter}")

    data = cursor.fetchall()
    conn.close()

    # Check if data contains at least two elements
    if not data or len(data[0]) < 2:
        print("No data or not enough columns returned from the SQL query.")
        return

    # Process data
    x = [row[0] for row in data]
    y = [row[1] for row in data]

    # Create a bar graph
    ax.bar(x, y)
    ax.set_xlabel('Time')
    ax.set_ylabel('Count of Reported Vehicles')
    ax.set_title('Count of Reported Vehicles That Entered the Expressway')

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    return data

def busiest_entrance_exit_graph(ax, filter1, filter2):
    # Connect to the SQLite database
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to fetch the average count of vehicles by entrance or exit
    if filter2 == 'Hourly':
        cursor.execute('SELECT strftime("%H:00", time_entered) as Hour, COUNT(*) as Count FROM vehicles WHERE {} = ? GROUP BY strftime("%H", time_entered)'.format(filter1), (filter1,))
    elif filter2 == 'Daily':
        cursor.execute('SELECT strftime("%Y-%m-%d", time_entered) as Day, COUNT(*) as Count FROM vehicles WHERE {} = ? GROUP BY strftime("%Y-%m-%d", time_entered)'.format(filter1), (filter1,))
    elif filter2 == 'Monthly':
        cursor.execute('SELECT strftime("%Y-%m", time_entered) as Month, COUNT(*) as Count FROM vehicles WHERE {} = ? GROUP BY strftime("%Y-%m", time_entered)'.format(filter1), (filter1,))
    elif filter2 == 'Yearly':
        cursor.execute('SELECT strftime("%Y", time_entered) as Year, COUNT(*) as Count FROM vehicles WHERE {} = ? GROUP BY strftime("%Y", time_entered)'.format(filter1), (filter1,))
    else:
        raise ValueError(f"Invalid filter value: {filter2}")

    data = cursor.fetchall()
    conn.close()

    # Check if data contains at least two elements
    if not data or len(data[0]) < 2:
        print("No data or not enough columns returned from the SQL query.")
        return

    # Process data
    x = [row[0] for row in data]
    y = [row[1] for row in data]

    # Create a bar graph
    ax.bar(x, y)
    ax.set_xlabel(filter2)
    ax.set_ylabel('Number of Vehicles')
    ax.set_title(f'Average Number of Vehicles at {filter1} {filter2}')

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    return data
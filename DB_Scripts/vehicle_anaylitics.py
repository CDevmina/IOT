import sqlite3


def totalcount_graph(ax, filter1, filter2):
    # Query database
    conn = sqlite3.connect('Database/vehicle_database.db')
    cursor = conn.cursor()

    if filter1 == 'Hourly':
        cursor.execute(
            'SELECT strftime("%H:00", time_entered) as Hour, vehicle_class, COUNT(*) as Count FROM vehicles WHERE strftime("%Y-%m-%d", time_entered) = ? GROUP BY strftime("%H", time_entered), vehicle_class',
            (filter2,))
    elif filter1 == 'Daily':
        cursor.execute(
            'SELECT strftime("%m-%d", time_entered) as Day, vehicle_class, COUNT(*) as Count FROM vehicles WHERE strftime("%Y-%m", time_entered) = ? GROUP BY strftime("%d", time_entered), vehicle_class',
            (filter2,))
    elif filter1 == 'Monthly':
        cursor.execute(
            'SELECT strftime("%Y-%m", time_entered) as Month, vehicle_class, COUNT(*) as Count FROM vehicles WHERE strftime("%Y", time_entered) = ? GROUP BY strftime("%Y-%m", time_entered), vehicle_class',
            (filter2,))
    elif filter1 == 'Yearly':
        cursor.execute(
            'SELECT strftime("%Y", time_entered) as Year, vehicle_class, COUNT(*) as Count FROM vehicles GROUP BY strftime("%Y", time_entered), vehicle_class')
    else:
        raise ValueError(f"Invalid filter value: {filter1}")

    data = cursor.fetchall()
    conn.close()

    # Check if data contains at least three elements
    if not data or len(data[0]) < 3:
        print("No data or not enough columns returned from the SQL query.")
        return

    # Process data
    x = list(set(row[0] for row in data))  # Use set to remove duplicates
    y = [sum(row[2] for row in data if row[0] == time) for time in x]
    hue = [row[1] for row in data]  # Vehicle class

    # Create a bar graph
    for vehicle_type in set(hue):
        y_filtered = [count if type == vehicle_type else 0 for count, type in zip(y, hue)]
        ax.bar(x, y_filtered, label=vehicle_type)

    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Vehicles')
    ax.set_title('Total Count of Vehicles That Entered the Expressway')
    ax.legend()

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    return data


def average_speed_graph(ax, filter1, filter2):
    # Query database
    conn = sqlite3.connect('Database/vehicle_database.db')
    cursor = conn.cursor()

    if filter1 == 'Hourly':
        cursor.execute(
            'SELECT strftime("%H:00", time_entered) as Hour, AVG(average_speed) as AverageSpeed FROM vehicles WHERE strftime("%Y-%m-%d", time_entered) = ? GROUP BY strftime("%H", time_entered)',
            (filter2,))
    elif filter1 == 'Daily':
        cursor.execute(
            'SELECT strftime("%Y-%m-%d", time_entered) as Day, AVG(average_speed) as AverageSpeed FROM vehicles WHERE strftime("%Y-%m", time_entered) = ? GROUP BY strftime("%Y-%m-%d", time_entered)',
            (filter2,))
    elif filter1 == 'Monthly':
        cursor.execute(
            'SELECT strftime("%Y-%m", time_entered) as Month, AVG(average_speed) as AverageSpeed FROM vehicles WHERE strftime("%Y", time_entered) = ? GROUP BY strftime("%Y-%m", time_entered)',
            (filter2,))
    elif filter1 == 'Yearly':
        cursor.execute(
            'SELECT strftime("%Y", time_entered) as Year, AVG(average_speed) as AverageSpeed FROM vehicles WHERE strftime("%Y", time_entered) = ? GROUP BY strftime("%Y", time_entered)',
            (filter2,))
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


def reported_vehicles_graph(ax, filter1, filter2):
    # Connect to the SQLite database
    conn = sqlite3.connect('Database/vehicle_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to fetch the count of reported vehicles
    if filter1 == 'Hourly':
        cursor.execute(
            'SELECT strftime("%H:00", time_entered) as Hour, report_status, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" AND strftime("%Y-%m-%d", time_entered) = ? GROUP BY strftime("%H", time_entered), report_status',
            (filter2,))
    elif filter1 == 'Daily':
        cursor.execute(
            'SELECT strftime("%Y-%m-%d", time_entered) as Day, report_status, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" AND strftime("%Y-%m", time_entered) = ? GROUP BY strftime("%Y-%m-%d", time_entered), report_status',
            (filter2,))
    elif filter1 == 'Monthly':
        cursor.execute(
            'SELECT strftime("%Y-%m", time_entered) as Month, report_status, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" AND strftime("%Y", time_entered) = ? GROUP BY strftime("%Y-%m", time_entered), report_status',
            (filter2,))
    elif filter1 == 'Yearly':
        cursor.execute(
            'SELECT strftime("%Y", time_entered) as Year, report_status, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" AND strftime("%Y", time_entered) = ? GROUP BY strftime("%Y", time_entered), report_status',
            (filter2,))
    else:
        raise ValueError(f"Invalid filter value: {filter1}")

    data = cursor.fetchall()
    conn.close()

    # Check if data contains at least three elements
    if not data or len(data[0]) < 3:
        print("No data or not enough columns returned from the SQL query.")
        return

    # Process data
    x = list(set(row[0] for row in data))  # Use set to remove duplicates
    y = [sum(row[2] for row in data if row[0] == time) for time in x]
    hue = [row[1] for row in data]  # Report status

    # Create a bar graph with different colors for each report status
    for report_type in set(hue):
        y_filtered = [count if type == report_type else 0 for count, type in zip(y, hue)]
        ax.bar(x, y_filtered, label=report_type)

    ax.set_xlabel('Time')
    ax.set_ylabel('Count of Reported Vehicles')
    ax.set_title('Count of Reported Vehicles That Entered the Expressway')
    ax.legend()

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    return data


def busiest_entrance_exit_graph(ax, entrance_or_exit, date):
    # Connect to the SQLite database
    conn = sqlite3.connect('Database/vehicle_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to fetch the count of vehicles by entrance or exit for each hour of the specified date
    cursor.execute(
        'SELECT strftime("%H:00", time_entered) as Hour, COUNT(*) as Count FROM vehicles WHERE (entrance = ? OR exit = ?) AND strftime("%Y-%m-%d", time_entered) = ? GROUP BY strftime("%H", time_entered)',
        (entrance_or_exit, entrance_or_exit, date))

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
    ax.set_xlabel('Hour')
    ax.set_ylabel('Number of Vehicles')
    ax.set_title(f'Number of Vehicles at {entrance_or_exit} on {date}')

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    return data

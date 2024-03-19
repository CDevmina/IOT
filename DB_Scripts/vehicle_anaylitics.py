import sqlite3
from datetime import datetime, timedelta


def totalcount_graph(ax, filter):
    # Query database
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    if filter == 'Hourly':
        cursor.execute('SELECT strftime("%H - ", time_entered) || strftime("%H", datetime(time_entered, "+1 hour")) as Hour, vehicle_class, COUNT(*) as Count FROM vehicles WHERE time_entered > datetime("now", "-24 hours") GROUP BY strftime("%H", time_entered), vehicle_class')
    elif filter == 'Daily':
        cursor.execute('SELECT strftime("%m/%d", time_entered) as Day, vehicle_class, COUNT(*) as Count FROM vehicles WHERE time_entered > datetime("now", "-30 days") GROUP BY strftime("%m/%d", time_entered), vehicle_class')
    elif filter == 'Monthly':
        cursor.execute('SELECT strftime("%m-%Y", time_entered) as Month, vehicle_class, COUNT(*) as Count FROM vehicles WHERE strftime("%Y", time_entered) = strftime("%Y", "now") GROUP BY strftime("%m", time_entered), vehicle_class')
    elif filter == 'Yearly':
        cursor.execute('SELECT strftime("%Y", time_entered) as Year, vehicle_class, COUNT(*) as Count FROM vehicles GROUP BY strftime("%Y", time_entered), vehicle_class')
    else:
        raise ValueError(f"Invalid filter value: {filter}")

    data = cursor.fetchall()
    conn.close()

    # Check if data contains at least three elements
    if not data or len(data[0]) < 3:
        print("No data or not enough columns returned from the SQL query.")
        return

    # Process data
    x = [row[0] for row in data]
    y = [row[2] for row in data]
    hue = [row[1] for row in data]

    # Create a bar graph
    for vehicle_type in set(hue):
        y_filtered = [count if type == vehicle_type else 0 for count, type in zip(y, hue)]
        ax.bar(x, y_filtered, label=vehicle_type)

    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Vehicles')
    ax.set_title('Total Count of Vehicles That Entered the Expressway')

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    # Add a legend
    ax.legend()

    return data


def average_speed_graph(ax, filter):
    # Connect to the SQLite database
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to fetch the average speed of vehicles
    if filter == 'Hourly':
        cursor.execute('SELECT strftime("%H - ", time_entered) || strftime("%H", datetime(time_entered, "+1 hour")) as Hour, AVG(CAST(REPLACE(average_speed, " Km/h", "") AS FLOAT)) as AverageSpeed FROM vehicles WHERE time_entered > datetime("now", "-24 hours") GROUP BY strftime("%H", time_entered)')
    elif filter == 'Daily':
        cursor.execute('SELECT strftime("%m/%d", time_entered) as Day, AVG(CAST(REPLACE(average_speed, " Km/h", "") AS FLOAT)) as AverageSpeed FROM vehicles WHERE time_entered > datetime("now", "-30 days") GROUP BY strftime("%m/%d", time_entered)')
    elif filter == 'Monthly':
        cursor.execute('SELECT strftime("%m-%Y", time_entered) as Month, AVG(CAST(REPLACE(average_speed, " Km/h", "") AS FLOAT)) as AverageSpeed FROM vehicles WHERE strftime("%Y", time_entered) = strftime("%Y", "now") GROUP BY strftime("%m", time_entered)')
    elif filter == 'Yearly':
        cursor.execute('SELECT strftime("%Y", time_entered) as Year, AVG(CAST(REPLACE(average_speed, " Km/h", "") AS FLOAT)) as AverageSpeed FROM vehicles GROUP BY strftime("%Y", time_entered)')
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

    # Create a line graph
    ax.plot(x, y)
    ax.set_xlabel('Time')
    ax.set_ylabel('Average Speed')
    ax.set_title('Average Speed of Vehicles That Entered the Expressway')

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    return data

def reported_vehicles_graph(ax, filter):
    # Connect to the SQLite database
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to fetch the count of reported vehicles
    if filter == 'Hourly':
        cursor.execute('SELECT strftime("%H - ", time_entered) || strftime("%H", datetime(time_entered, "+1 hour")) as Hour, report_status, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" AND time_entered > datetime("now", "-24 hours") GROUP BY strftime("%H", time_entered), report_status')
    elif filter == 'Daily':
        cursor.execute('SELECT strftime("%m/%d", time_entered) as Day, report_status, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" AND time_entered > datetime("now", "-30 days") GROUP BY strftime("%m/%d", time_entered), report_status')
    elif filter == 'Monthly':
        cursor.execute('SELECT strftime("%m-%Y", time_entered) as Month, report_status, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" AND strftime("%Y", time_entered) = strftime("%Y", "now") GROUP BY strftime("%m", time_entered), report_status')
    elif filter == 'Yearly':
        cursor.execute('SELECT strftime("%Y", time_entered) as Year, report_status, COUNT(*) as Count FROM vehicles WHERE report_status != "Normal" GROUP BY strftime("%Y", time_entered), report_status')
    else:
        raise ValueError(f"Invalid filter value: {filter}")

    data = cursor.fetchall()
    conn.close()

    # Check if data contains at least three elements
    if not data or len(data[0]) < 3:
        print("No data or not enough columns returned from the SQL query.")
        return

    # Process data
    x = [row[0] for row in data]
    y = [row[2] for row in data]
    hue = [row[1] for row in data]

    for report_type in set(hue):
        y_filtered = [count if type == report_type else 0 for count, type in zip(y, hue)]
        ax.bar(x, y_filtered, label=report_type)

    ax.set_xlabel('Time')
    ax.set_ylabel('Count of Reported Vehicles')
    ax.set_title('Count of Reported Vehicles That Entered the Expressway')

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    # Add a legend
    ax.legend()

    return data

def busiest_entrance_exit_graph(ax, filter):
    # Connect to the SQLite database
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to fetch the count of vehicles by entrance or exit
    if filter == 'Entrance':
        cursor.execute('SELECT entrance, COUNT(*) as Count FROM vehicles WHERE time_entered > datetime("now", "-12 months") GROUP BY entrance')
    elif filter == 'Exit':
        cursor.execute('SELECT exit, COUNT(*) as Count FROM vehicles WHERE time_entered > datetime("now", "-12 months") GROUP BY exit')
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
    ax.set_xlabel(filter)
    ax.set_ylabel('Number of Vehicles')
    ax.set_title(f'Busiest {filter}s in the Last 12 Months')

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=90, fontsize=6)

    return data
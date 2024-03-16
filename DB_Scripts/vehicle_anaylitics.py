import sqlite3
from time import strftime
import datetime  # Updated import statement
import matplotlib.pyplot as plt


def totalcount_graph(ax, filter):
    # Query database
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()
    if filter == 'All':
        cursor.execute('SELECT time_entered FROM vehicles')
    else:
        cursor.execute('SELECT time_entered FROM vehicles WHERE strftime("%w", time_entered) = ?', (str((int(filter) + 6) % 7),))
    data = cursor.fetchall()
    conn.close()

    # Process data
    counts = {}
    for row in data:
        date = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        day = date.strftime('%A')
        if day not in ['Monday', 'Sunday']:  # Exclude Monday and Sunday
            if day not in counts:
                counts[day] = 0
            counts[day] += 1

    # Order the days
    ordered_days = ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    ordered_counts = [counts[day] for day in ordered_days if day in counts]

    # Create graph
    ax.bar(ordered_days, ordered_counts)
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Number of Vehicles')
    ax.set_title('Total Count of Vehicles That Entered the Expressway')
import sqlite3
from datetime import datetime, timedelta


def totalcount_graph(ax, filter):
    # Query database
    conn = sqlite3.connect('D:\IOT\Database/vehicle_database.db')
    cursor = conn.cursor()

    if filter == 'Hourly':
        cursor.execute('SELECT strftime("%H - ", time_entered) || strftime("%H", datetime(time_entered, "+1 hour")) as Hour, COUNT(*) as Count FROM vehicles WHERE time_entered > datetime("now", "-24 hours") GROUP BY strftime("%H", time_entered)')
    elif filter == 'Daily':
        cursor.execute('SELECT strftime("%m/%d", time_entered) as Day, COUNT(*) as Count FROM vehicles WHERE time_entered > datetime("now", "-30 days") GROUP BY strftime("%m/%d", time_entered)')
    elif filter == 'Monthly':
        cursor.execute('SELECT strftime("%m-%Y", time_entered) as Month, COUNT(*) as Count FROM vehicles WHERE strftime("%Y", time_entered) = strftime("%Y", "now") GROUP BY strftime("%m", time_entered)')
    elif filter == 'Yearly':
        cursor.execute('SELECT strftime("%Y", time_entered) as Year, COUNT(*) as Count FROM vehicles GROUP BY strftime("%Y", time_entered)')
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

    # Create a list of all hours, days, or months based on the selected filter
    if filter == 'Hourly':
        all_times = [f"{str(i).zfill(2)} - {str((i+1)%24).zfill(2)}" for i in range(24)]
    elif filter == 'Daily':
        all_times = [(datetime.now() - timedelta(days=i)).strftime("%m/%d") for i in range(30)]
    elif filter == 'Monthly':
        all_times = [datetime.now().replace(month=i+1).strftime("%m-%Y") for i in range(12)]
    elif filter == 'Yearly':
        all_times = [str(i) for i in range(datetime.now().year - len(data) + 1, datetime.now().year + 1)]
    else:
        raise ValueError(f"Invalid filter value: {filter}")

    # Merge the data with the list of all hours, days, or months
    x = all_times
    y = [next((count for time, count in data if time == t), 0) for t in all_times]

    # Create graph
    ax.bar(x, y)
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Vehicles')
    ax.set_title('Total Count of Vehicles That Entered the Expressway')

    # Set the x-ticks and rotate the labels and reduce their font size
    ax.set_xticks(range(len(x)))  # Add this line
    ax.set_xticklabels(x, rotation=90, fontsize=6)  # Reduce the font size to 6

    return data
import sqlite3

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QHBoxLayout, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from DB_Scripts.vehicle_anaylitics import totalcount_graph, average_speed_graph, reported_vehicles_graph , busiest_entrance_exit_graph

class AnalyticsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Analytics')
        self.resize(800, 600)

        # Create a layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Create labels for the filters
        self.label1 = QLabel('Graph 1:')
        self.label2 = QLabel('Graph 2:')
        self.label3 = QLabel('Graph 3:')
        self.label4 = QLabel('Graph 4:')

        # Create a combo box for the filter
        self.filter_combo1 = QComboBox()
        self.filter_combo1.addItems(['Hourly', 'Daily', 'Monthly', 'Yearly'])
        self.filter_combo1.currentTextChanged.connect(self.update_filter_options)

        self.filter_combo2 = QComboBox()
        self.filter_combo2.currentTextChanged.connect(self.update_graph)

        # Create three more pairs of combo boxes
        self.combo2_1 = QComboBox()
        self.combo2_1.addItems(['Hourly', 'Daily', 'Monthly', 'Yearly'])
        self.combo2_1.currentTextChanged.connect(self.update_filter_options)

        self.combo2_2 = QComboBox()
        self.combo2_2.currentTextChanged.connect(self.update_graph)

        self.combo3_1 = QComboBox()
        self.combo3_1.addItems(['Hourly', 'Daily', 'Monthly', 'Yearly'])
        self.combo3_1.currentTextChanged.connect(self.update_filter_options)

        self.combo3_2 = QComboBox()
        self.combo3_2.currentTextChanged.connect(self.update_graph)

        self.combo4_1 = QComboBox()
        self.combo4_1.addItems(self.get_all_entrances_exits())
        self.combo4_1.currentTextChanged.connect(self.update_filter_options)

        self.combo4_2 = QComboBox()
        self.combo4_2.currentTextChanged.connect(self.update_graph)


        # Create a layout for the first two combo boxes
        self.layout1 = QHBoxLayout()
        self.layout1.setSpacing(10)  # Reduce the spacing
        self.layout1.addWidget(self.label1)
        self.layout1.addWidget(self.filter_combo1)
        self.layout1.addWidget(self.filter_combo2)
        self.layout1.addWidget(self.label2)
        self.layout1.addWidget(self.combo2_1)
        self.layout1.addWidget(self.combo2_2)

        # Create a layout for the last two combo boxes
        self.layout2 = QHBoxLayout()
        self.layout2.setSpacing(10)  # Reduce the spacing
        self.layout2.addWidget(self.label3)
        self.layout2.addWidget(self.combo3_1)
        self.layout2.addWidget(self.combo3_2)
        self.layout2.addWidget(self.label4)
        self.layout2.addWidget(self.combo4_1)
        self.layout2.addWidget(self.combo4_2)

        # Add the layouts to the main layout
        self.layout.addLayout(self.layout1)
        self.layout.addLayout(self.layout2)

        # Create a figure and a canvas
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.layout.addWidget(self.canvas)

        # Create a back button
        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        # Update the graph with default filter values
        self.update_filter_options()
        self.update_graph()

    def update_filter_options(self):
        sender = self.sender()

        if sender is None:
            # Initialize all combo boxes
            self.update_graph_for_combos(self.filter_combo1, self.filter_combo2)
            self.update_graph_for_combos(self.combo2_1, self.combo2_2)
            self.update_graph_for_combos(self.combo3_1, self.combo3_2)
            self.update_graph_for_combos(self.combo4_1, self.combo4_2)
        else:
            if sender == self.filter_combo1:
                target = self.filter_combo2
            elif sender == self.combo2_1:
                target = self.combo2_2
            elif sender == self.combo3_1:
                target = self.combo3_2
            elif sender == self.combo4_1:
                target = self.combo4_2
            else:
                return

            self.update_graph_for_combos(sender, target)

    def update_graph_for_combos(self, sender, target):
        filter1 = sender.currentText()

        target.clear()

        if sender == self.combo4_1:
            target.addItems(self.get_all_days())
        else:
            if filter1 == 'Hourly':
                target.addItems(self.get_all_days())
            elif filter1 == 'Daily':
                target.addItems(self.get_all_months())
            elif filter1 == 'Monthly':
                target.addItems(self.get_all_years())
            elif filter1 == 'Yearly':
                target.addItem('N/A')


    def get_all_entrances_exits(self):
        conn = sqlite3.connect('D:\Work\IOT\Database/vehicle_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT entrance FROM vehicles UNION SELECT DISTINCT exit FROM vehicles ORDER BY entrance')
        entrances_exits = [row[0] for row in cursor.fetchall()]
        conn.close()
        return entrances_exits


    def get_all_days(self):
        conn = sqlite3.connect('D:\Work\IOT\Database/vehicle_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT strftime("%Y-%m-%d", time_entered) as Day FROM vehicles ORDER BY Day')
        days = [row[0] for row in cursor.fetchall()]
        conn.close()
        return days

    def get_all_months(self):
        conn = sqlite3.connect('D:\Work\IOT\Database/vehicle_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT strftime("%Y-%m", time_entered) as Month FROM vehicles ORDER BY Month')
        months = [row[0] for row in cursor.fetchall()]
        conn.close()
        return months

    def get_all_years(self):
        conn = sqlite3.connect('D:\Work\IOT\Database/vehicle_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT strftime("%Y", time_entered) as Year FROM vehicles ORDER BY Year')
        years = [row[0] for row in cursor.fetchall()]
        conn.close()
        return years

    def update_graph(self):
        # Clear the figure
        self.figure.clear()

        # Create the graphs
        ax1 = self.figure.add_subplot(2, 2, 1)
        totalcount_graph(ax1, self.filter_combo1.currentText(), self.filter_combo2.currentText())

        ax2 = self.figure.add_subplot(2, 2, 2)
        average_speed_graph(ax2, self.combo2_1.currentText(), self.combo2_2.currentText())

        ax3 = self.figure.add_subplot(2, 2, 3)
        reported_vehicles_graph(ax3, self.combo3_1.currentText(), self.combo3_2.currentText())

        ax4 = self.figure.add_subplot(2, 2, 4)
        busiest_entrance_exit_graph(ax4, self.combo4_1.currentText(), self.combo4_2.currentText())

        # Adjust the spacing between the subplots
        self.figure.subplots_adjust(hspace=0.5, wspace=0.3)

        # Draw the canvas
        self.canvas.draw()

    def go_back(self):
        from AdminHome import AdminHome

        # Close the AnalyticsWindow
        self.close()

        # Open the AdminHome page
        self.admin_home = AdminHome()
        self.admin_home.show()
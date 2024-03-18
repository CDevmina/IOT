from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QHBoxLayout, QPushButton
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

        # Create a combo box for the filter
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['Hourly', 'Daily', 'Monthly', 'Yearly'])
        self.filter_combo.currentTextChanged.connect(self.update_graph)

        # Create three more combo boxes
        self.combo2 = QComboBox()
        self.combo2.addItems(['Hourly', 'Daily', 'Monthly', 'Yearly'])
        self.combo2.currentTextChanged.connect(self.update_graph)

        self.combo3 = QComboBox()
        self.combo3.addItems(['Hourly', 'Daily', 'Monthly', 'Yearly'])
        self.combo3.currentTextChanged.connect(self.update_graph)

        self.combo4 = QComboBox()
        self.combo4.addItems(['Entrance', 'Exit'])
        self.combo4.currentTextChanged.connect(self.update_graph)

        # Create a layout for the first two combo boxes
        self.layout1 = QHBoxLayout()
        self.layout1.addWidget(self.filter_combo)
        self.layout1.addWidget(self.combo2)

        # Create a layout for the last two combo boxes
        self.layout2 = QHBoxLayout()
        self.layout2.addWidget(self.combo3)
        self.layout2.addWidget(self.combo4)

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

        # Update the graph
        self.update_graph()

    def update_graph(self):
        # Clear the figure
        self.figure.clear()

        # Create the graphs
        ax1 = self.figure.add_subplot(2, 2, 1)
        totalcount_graph(ax1, self.filter_combo.currentText())

        ax2 = self.figure.add_subplot(2, 2, 2)
        average_speed_graph(ax2, self.combo2.currentText())

        ax3 = self.figure.add_subplot(2, 2, 3)
        reported_vehicles_graph(ax3, self.combo3.currentText())

        ax4 = self.figure.add_subplot(2, 2, 4)
        busiest_entrance_exit_graph(ax4, self.combo4.currentText())

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
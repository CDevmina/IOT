import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from DB_Scripts.vehicle_anaylitics import totalcount_graph

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
        self.combo4.addItems(['Hourly', 'Daily', 'Monthly', 'Yearly'])
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

        # Update the graph
        self.update_graph()

    def update_graph(self):
        # Clear the figure
        self.figure.clear()

        # Create the graphs
        ax1 = self.figure.add_subplot(2, 2, 1)
        totalcount_graph(ax1, self.filter_combo.currentText())

        ax2 = self.figure.add_subplot(2, 2, 2)
        # Add your code to generate the second graph here

        ax3 = self.figure.add_subplot(2, 2, 3)
        # Add your code to generate the third graph here

        ax4 = self.figure.add_subplot(2, 2, 4)
        # Add your code to generate the fourth graph here

        # Draw the canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnalyticsWindow()
    window.showMaximized()  # Change this line to open the window in full screen
    sys.exit(app.exec_())
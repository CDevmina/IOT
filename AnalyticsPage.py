import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox
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
        self.filter_combo.addItem('All')
        self.filter_combo.addItem('Tuesday')
        self.filter_combo.addItem('Wednesday')
        self.filter_combo.addItem('Thursday')
        self.filter_combo.addItem('Friday')
        self.filter_combo.addItem('Saturday')
        self.filter_combo.currentTextChanged.connect(self.update_graph)
        self.layout.addWidget(self.filter_combo)

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
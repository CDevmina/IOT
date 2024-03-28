from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QWidget, \
    QComboBox, QLineEdit
from PyQt5.QtCore import Qt
from DB_Scripts.Database_Vehicle import get_all_vehicles, get_all_vehicles_in, get_all_vehicles_out, \
    update_vehicle_report_status


class AdminVehicleView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vehicle View')
        self.resize(800, 600)

        self.title_label = QLabel('Vehicle View')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.vehicle_list = QTableWidget()
        self.vehicle_list.setColumnCount(10)
        self.vehicle_list.setHorizontalHeaderLabels(
            ["ID", "License Plate", "Entrance", "Entrance Time", "Report Status", "Status", "Average Speed", "Exit",
             "Exit Time", "Amount"])
        self.vehicle_list.setColumnWidth(2, 200)

        self.filter_selection = QComboBox()
        self.filter_selection.addItems(["In", "Out", "Both"])
        self.filter_selection.currentIndexChanged.connect(self.update_vehicle_list)

        self.update_vehicle_list()  # Moved this line to after the definition of filter_selection

        self.license_plate_input = QLineEdit()
        self.status_selection = QComboBox()
        self.status_selection.addItems(["Normal", "Stolen", "Reported", "Overspeeding"])

        self.add_status_button = QPushButton('Add Status')
        self.add_status_button.clicked.connect(self.add_status)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.go_back)

        status_layout = QHBoxLayout()
        status_layout.addWidget(self.filter_selection)
        status_layout.addWidget(self.license_plate_input)
        status_layout.addWidget(self.status_selection)
        status_layout.addWidget(self.add_status_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.vehicle_list)
        main_layout.addLayout(status_layout)
        main_layout.addWidget(self.back_button)
        self.setLayout(main_layout)

    def update_vehicle_list(self):
        self.vehicle_list.setRowCount(0)
        filter_option = self.filter_selection.currentText()
        if filter_option == "In":
            vehicles = get_all_vehicles_in()
        elif filter_option == "Out":
            vehicles = get_all_vehicles_out()
        else:
            vehicles = get_all_vehicles()
        for vehicle in vehicles:
            row = self.vehicle_list.rowCount()
            self.vehicle_list.insertRow(row)
            self.vehicle_list.setItem(row, 0, QTableWidgetItem(str(vehicle[0])))
            self.vehicle_list.setItem(row, 1, QTableWidgetItem(str(vehicle[1])))
            self.vehicle_list.setItem(row, 2, QTableWidgetItem(str(vehicle[2])))
            self.vehicle_list.setItem(row, 3, QTableWidgetItem(str(vehicle[3])))
            self.vehicle_list.setItem(row, 4, QTableWidgetItem(str(vehicle[4])))
            self.vehicle_list.setItem(row, 5, QTableWidgetItem(str(vehicle[5])))
            self.vehicle_list.setItem(row, 6, QTableWidgetItem(str(vehicle[6])))
            self.vehicle_list.setItem(row, 7, QTableWidgetItem(str(vehicle[7])))
            self.vehicle_list.setItem(row, 8, QTableWidgetItem(str(vehicle[8])))
            self.vehicle_list.setItem(row, 9, QTableWidgetItem(str(vehicle[9])))

    def add_status(self):
        license_plate = self.license_plate_input.text()
        status = self.status_selection.currentText()
        update_vehicle_report_status(license_plate, status)
        self.update_vehicle_list()

    def go_back(self):
        from AdminHome import AdminHome
        self.admin_home = AdminHome()
        self.admin_home.show()
        self.hide()

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from DB_Scripts.Database_User import get_user_view
from DB_Scripts.Database_Vehicle import get_vehicles
from AdminUserAdd import AdminUserAdd


class AdminHome(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Center')
        self.resize(800, 600)

        self.title_label = QLabel('Admin Center')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.user_list = QTableWidget()
        self.user_list.setColumnCount(2)
        self.user_list.setHorizontalHeaderLabels(["User ID", "Status"])
        self.update_user_list()

        self.vehicle_list = QTableWidget()
        self.vehicle_list.setColumnCount(6)
        self.vehicle_list.setHorizontalHeaderLabels(["ID", "License Plate", "Entrance", "Time", "Report Status", "Status"])
        self.update_vehicle_list()

        self.user_add_button = QPushButton('Add User')
        self.user_add_button.clicked.connect(self.go_to_user_add)

        self.vehicle_view_button = QPushButton('View Vehicles')
        self.vehicle_view_button.clicked.connect(self.go_to_vehicle_view)

        self.logout_button = QPushButton('Logout')
        self.logout_button.clicked.connect(self.logout)

        self.analytics_button = QPushButton('Analytics')
        self.analytics_button.clicked.connect(self.go_to_analytics)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.user_add_button)
        button_layout.addWidget(self.vehicle_view_button)
        button_layout.addWidget(self.analytics_button)  # add the new button here
        button_layout.addWidget(self.logout_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.user_list)
        main_layout.addWidget(self.vehicle_list)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def update_user_list(self):
        self.user_list.setRowCount(0)
        users = get_user_view()
        for user in users:
            row = self.user_list.rowCount()
            self.user_list.insertRow(row)
            self.user_list.setItem(row, 0, QTableWidgetItem(str(user[0])))
            self.user_list.setItem(row, 1, QTableWidgetItem(str(user[1])))

    def update_vehicle_list(self):
        self.vehicle_list.setRowCount(0)
        vehicles = get_vehicles()
        for vehicle in vehicles:
            row = self.vehicle_list.rowCount()
            self.vehicle_list.insertRow(row)
            self.vehicle_list.setItem(row, 0, QTableWidgetItem(str(vehicle[0])))
            self.vehicle_list.setItem(row, 1, QTableWidgetItem(str(vehicle[1])))
            self.vehicle_list.setItem(row, 2, QTableWidgetItem(str(vehicle[2])))
            self.vehicle_list.setItem(row, 3, QTableWidgetItem(str(vehicle[3])))
            self.vehicle_list.setItem(row, 4, QTableWidgetItem(str(vehicle[4])))
            self.vehicle_list.setItem(row, 5, QTableWidgetItem(str(vehicle[5])))

    def go_to_user_add(self):
        self.user_add_window = AdminUserAdd()
        self.user_add_window.show()
        self.hide()

    def go_to_vehicle_view(self):
        from AdminVehicleView import AdminVehicleView  # Move the import statement here
        self.vehicle_view_window = AdminVehicleView()
        self.vehicle_view_window.show()
        self.hide()

    def logout(self):
        from StartPage import StartPage
        self.start_page = StartPage()
        self.start_page.show()
        self.hide()

    def go_to_analytics(self):
        from AnalyticsPage import AnalyticsWindow
        self.analytics_window = AnalyticsWindow()
        self.analytics_window.show()
        self.hide()
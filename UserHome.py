from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from DB_Scripts.Database_Vehicle import select_vehicle, update_vehicle_report_status
from time import strftime, localtime
from Backend_Model.exit import Run
from PyQt5.QtGui import QPixmap, QImage
from DB_Scripts.Database_User import update_user_status
from UserLogin import UserLogin
from datetime import datetime

class Ui_MainWindow(object):
    def __init__(self, MainWindow, current_user_id):
        self.MainWindow = MainWindow
        self.current_user_id = current_user_id
        self.exit = 'Kadawatha'
        self.model_running = False

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1055, 719)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(10, 650, 75, 23))
        self.StartButton.setObjectName("StartButton")
        self.StopButton = QtWidgets.QPushButton(self.centralwidget)
        self.StopButton.setGeometry(QtCore.QRect(110, 650, 75, 23))
        self.StopButton.setObjectName("StopButton")
        self.ConfirmButton = QtWidgets.QPushButton(self.centralwidget)
        self.ConfirmButton.setGeometry(QtCore.QRect(460, 540, 121, 61))
        self.ConfirmButton.setObjectName("ConfirmButton")
        self.LogoutButton = QtWidgets.QPushButton(self.centralwidget)
        self.LogoutButton.setGeometry(QtCore.QRect(960, 640, 75, 23))
        self.LogoutButton.setObjectName("LogoutButton")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(600, 70, 411, 291))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.ConfirmLabel = QtWidgets.QLabel(self.centralwidget)
        self.ConfirmLabel.setGeometry(QtCore.QRect(460, 520, 121, 16))
        self.ConfirmLabel.setObjectName("ConfirmLabel")
        self.AmountLabel = QtWidgets.QLabel(self.centralwidget)
        self.AmountLabel.setGeometry(QtCore.QRect(470, 470, 121, 51))

        font = QtGui.QFont()
        font.setPointSize(16)

        self.AmountLabel.setFont(font)
        self.AmountLabel.setObjectName("AmountLabel")
        self.Licenseplate = QtWidgets.QLabel(self.centralwidget)
        self.Licenseplate.setGeometry(QtCore.QRect(100, 110, 200, 16))
        self.Licenseplate.setObjectName("Licenseplate")
        self.VehicleTypeLabel = QtWidgets.QLabel(self.centralwidget)
        self.VehicleTypeLabel.setGeometry(QtCore.QRect(100, 140, 200, 16))
        self.VehicleTypeLabel.setObjectName("VehicleTypeLabel")
        self.TimeEnterLabel = QtWidgets.QLabel(self.centralwidget)
        self.TimeEnterLabel.setGeometry(QtCore.QRect(100, 170, 200, 16))
        self.TimeEnterLabel.setObjectName("TimeEnterLabel")
        self.TimeExitLabel = QtWidgets.QLabel(self.centralwidget)
        self.TimeExitLabel.setGeometry(QtCore.QRect(100, 200, 200, 16))
        self.TimeExitLabel.setObjectName("TimeExitLabel")
        self.EntranceLabel = QtWidgets.QLabel(self.centralwidget)
        self.EntranceLabel.setGeometry(QtCore.QRect(100, 230, 200, 16))
        self.EntranceLabel.setObjectName("EntranceLabel")
        self.ExitLabel = QtWidgets.QLabel(self.centralwidget)
        self.ExitLabel.setGeometry(QtCore.QRect(100, 260, 200, 16))
        self.ExitLabel.setObjectName("ExitLabel")
        self.ReportLabel = QtWidgets.QLabel(self.centralwidget)
        self.ReportLabel.setGeometry(QtCore.QRect(100, 290, 200, 16))
        self.AverageSpeedLabel = QtWidgets.QLabel(self.centralwidget)
        self.AverageSpeedLabel.setGeometry(QtCore.QRect(100, 320, 200, 16))
        self.AverageSpeedLabel.setObjectName("AverageSpeedLabel")
        self.ReportLabel.setObjectName("ReportLabel")
        self.ModelLabel = QtWidgets.QLabel(self.centralwidget)
        self.ModelLabel.setGeometry(QtCore.QRect(40, 620, 200, 16))
        self.ModelLabel.setObjectName("ModelLabel")
        self.TitleLabel = QtWidgets.QLabel(self.centralwidget)
        self.TitleLabel.setGeometry(QtCore.QRect(360, 10, 261, 21))

        font = QtGui.QFont()
        font.setPointSize(12)

        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName("TitleLabel")
        self.Emplabel = QtWidgets.QLabel(self.centralwidget)
        self.Emplabel.setGeometry(QtCore.QRect(40, 20, 200, 16))
        self.Emplabel.setObjectName("Emplabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1055, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.image_label = QtWidgets.QLabel(self.frame)
        self.image_label.setGeometry(0, 0, self.frame.width(), self.frame.height())
        self.image_label.setScaledContents(True)  # Set the QLabel to scale its contents

        self.StartButton.clicked.connect(self.start_model)
        self.StopButton.clicked.connect(self.stop_model)
        self.LogoutButton.clicked.connect(self.logout_user)
        self.ConfirmButton.clicked.connect(self.confirm_exit)

        self.ConfirmLabel = QtWidgets.QLabel(self.centralwidget)
        self.ConfirmLabel.setGeometry(QtCore.QRect(460, 520, 121, 16))
        self.ConfirmLabel.setObjectName("ConfirmLabel")
        self.ConfirmLabel.setStyleSheet("font-size: 10px; color: gray;")  # Set the font size and color

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.StartButton.setText(_translate("MainWindow", "Start"))
        self.StopButton.setText(_translate("MainWindow", "Stop"))
        self.ConfirmButton.setText(_translate("MainWindow", "Confirm"))
        self.LogoutButton.setText(_translate("MainWindow", "Logout"))
        self.ConfirmLabel.setText(_translate("MainWindow", "Click to confirm payment ↓"))
        self.AmountLabel.setText(_translate("MainWindow", "Amount:"))
        self.Licenseplate.setText(_translate("MainWindow", "License plate:"))
        self.VehicleTypeLabel.setText(_translate("MainWindow", "Vehicle Type:"))
        self.TimeEnterLabel.setText(_translate("MainWindow", "Time Entered:"))
        self.TimeExitLabel.setText(_translate("MainWindow", "Time Exited:"))
        self.EntranceLabel.setText(_translate("MainWindow", "Entrance: "))
        self.ExitLabel.setText(_translate("MainWindow", "Exit: "))
        self.AverageSpeedLabel.setText(_translate("MainWindow", "Average Speed:"))
        self.ReportLabel.setText(_translate("MainWindow", "Report: "))
        self.ModelLabel.setText(_translate("MainWindow", "Model Status: Offline"))
        self.TitleLabel.setText(_translate("MainWindow", "Express Way Management System"))
        self.Emplabel.setText(_translate("MainWindow", f"Welcome Employee: {self.current_user_id}"))

    def update_model_status(self):
        if self.model_running:
            self.ModelLabel.setText("Model Status: Online")
        else:
            self.ModelLabel.setText("Model Status: Offline")

    def update_vehicle_info(self, license_plate):
        vehicle_info = select_vehicle(license_plate)
        if vehicle_info is not None:
            self.Licenseplate.setText(f'License Plate: {license_plate}')
            self.VehicleTypeLabel.setText(f'Vehicle Type: {vehicle_info[2]}')
            self.TimeEnterLabel.setText(f'Time Entered: {vehicle_info[3]}')
            self.TimeExitLabel.setText(f'Time Exited: {strftime("%Y-%m-%d %H:%M:%S", localtime())}')
            self.EntranceLabel.setText(f'Entrance: {vehicle_info[5]}')
            self.AverageSpeedLabel.setText(f'Average Speed: {vehicle_info[8]}')
            self.ExitLabel.setText(f'Exit: {vehicle_info[6]}')
            self.ReportLabel.setText(f'Report: {vehicle_info[9]}')

            # Get the amount for the vehicle and update the AmountLabel
            amount = self.get_amount(license_plate)
            self.AmountLabel.setText(f'Amount: {amount}')
        else:
            print("Error: Unable to retrieve vehicle information.")

    def get_amount(self, license_plate):
        return 100

    def logout_user(self):
        update_user_status(self.current_user_id, 'Logged out')
        print('User logged out successfully!')
        self.login_page = UserLogin()
        self.login_page.show()
        self.MainWindow.hide()

    def start_model(self):
        if not self.model_running:
            self.model_running = True
            self.update_model_status()

            # You can replace 'image_path' with the actual path to your image
            frame, self.license_plate = Run()

            if self.license_plate is not None:
                height, width, channel = frame.shape
                bytesPerLine = 3 * width
                qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

                pixmap = QPixmap.fromImage(qImg)
                self.image_label.setPixmap(pixmap)  # Set the QPixmap to the QLabel

                # Update the exit time and exit location in the database
                from DB_Scripts.Database_Vehicle import update_vehicle_exit, update_vehicle_status, \
                    update_vehicle_speed, \
                    update_exit_time

                update_vehicle_exit(self.license_plate, self.exit)
                update_exit_time(self.license_plate, strftime("%Y-%m-%d %H:%M:%S", localtime()))

                # Calculate the average speed
                average_speed = self.calculate_average_speed(self.license_plate)

                # If the average speed is over 100km/h, update the report status to 'Overspeeding'
                if average_speed > 100:
                    update_vehicle_report_status(self.license_plate, 'Overspeeding')

                # Update the vehicle's average speed in the database
                update_vehicle_speed(self.license_plate, average_speed)

                # Display the updated information
                self.update_vehicle_info(self.license_plate)
            else:
                print('Something went wrong!')


    def stop_model(self):
        if self.model_running:
            self.model_running = False
            self.update_model_status()
            print("Model stopped successfully!")

    def confirm_exit(self):
        from DB_Scripts.Database_Vehicle import update_vehicle_status, update_vehicle_exit, update_vehicle_amount

        # Update the vehicle's exit location
        update_vehicle_exit(self.license_plate, self.exit)

        # Get the amount for the vehicle
        amount = self.get_amount(self.license_plate)

        # Update the vehicle's amount in the database
        update_vehicle_amount(self.license_plate, amount)

        # Update the vehicle's status to 'Out'
        update_vehicle_status(self.license_plate, 'Out')

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"The Vehicle: {self.license_plate} has exited the Expressway")
        msg.setWindowTitle("Vehicle Exit Confirmation")
        msg.exec_()

        self.reset_labels_and_frame()

    def reset_labels_and_frame(self):
        # Reset all the labels
        self.Licenseplate.setText("License plate:")
        self.VehicleTypeLabel.setText("Vehicle Type:")
        self.TimeEnterLabel.setText("Time Entered:")
        self.TimeExitLabel.setText("Time Exited:")
        self.EntranceLabel.setText("Entrance: ")
        self.ExitLabel.setText("Exit: ")
        self.AverageSpeedLabel.setText("Average Speed:")
        self.ReportLabel.setText("Report: ")
        self.AmountLabel.setText("Amount:")

        # Clear the frame
        self.image_label.clear()

    def calculate_average_speed(self, license_plate):
        from DB_Scripts.Database_Vehicle import select_vehicle
        vehicle_info = select_vehicle(license_plate)
        time_entered = datetime.strptime(vehicle_info[3], "%Y-%m-%d %H:%M:%S")
        time_exited = datetime.now()
        total_time = (time_exited - time_entered).total_seconds() / 3600  # Convert to hours

        # Assume the length of the expressway is 100km
        expressway_length = 100
        average_speed = expressway_length / total_time  # Speed in km/h

        return average_speed
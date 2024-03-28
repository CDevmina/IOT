from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy


class StartPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Start Page')
        self.resize(600, 400)

        self.title_label = QLabel('Expressway Vehicle Management')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        self.user_button = QPushButton('User Login')
        self.user_button.setFixedSize(200, 50)
        self.admin_button = QPushButton('Admin Login')
        self.admin_button.setFixedSize(200, 50)

        layout = QVBoxLayout()
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addWidget(self.user_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.admin_button, alignment=Qt.AlignCenter)
        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.user_button.clicked.connect(self.show_user_login)
        self.admin_button.clicked.connect(self.show_admin_login)

        self.setLayout(layout)

    def show_user_login(self):
        from UserLogin import UserLogin
        self.user_login_window = UserLogin()
        self.user_login_window.show()
        self.hide()

    def show_admin_login(self):
        from AdminLogin import AdminLogin
        self.admin_login_window = AdminLogin()
        self.admin_login_window.show()
        self.hide()

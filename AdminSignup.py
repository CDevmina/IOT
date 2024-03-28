from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from DB_Scripts.Database_User import add_admin

class AdminSignup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Sign Up')
        self.resize(600, 400)

        self.admin_id_input = QLineEdit()
        self.admin_id_input.setPlaceholderText('Admin ID')
        self.admin_id_input.setAlignment(Qt.AlignCenter)
        self.admin_id_input.setStyleSheet("QLineEdit { border: 1px solid gray; border-radius: 5px; font-size: 16px; }")
        self.admin_id_input.setFixedSize(250, 30)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setStyleSheet("QLineEdit { border: 1px solid gray; border-radius: 5px; font-size: 16px; }")
        self.password_input.setFixedSize(250, 30)

        self.signup_button = QPushButton('Sign Up')
        self.signup_button.setStyleSheet("QPushButton { border: 1px solid gray; border-radius: 5px; font-size: 14px; }")
        self.signup_button.clicked.connect(self.signup)
        self.signup_button.setFixedSize(200, 40)

        self.back_button = QPushButton('Back')
        self.back_button.setStyleSheet("QPushButton { border: 1px solid gray; border-radius: 5px; font-size: 14px; }")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setFixedSize(200, 40)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.signup_button)
        button_layout.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        admin_label = QLabel('Admin Sign Up')
        admin_label.setAlignment(Qt.AlignCenter)
        admin_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(admin_label)
        layout.addSpacing(30)
        layout.addWidget(self.admin_id_input, alignment=Qt.AlignCenter)
        layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addLayout(button_layout)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

    def signup(self):
        admin_id = self.admin_id_input.text()
        password = self.password_input.text()

        if admin_id == '' or password == '':
            print('Please fill out all fields')
            return

        try:
            admin_id = int(admin_id)
        except ValueError:
            print('Admin ID must be an integer')
            return

        add_admin(admin_id, password)
        print('Admin signed up successfully!')

        self.close()
        self.go_back()

    def go_back(self):
        from AdminLogin import AdminLogin
        self.admin_login = AdminLogin()
        self.admin_login.show()
        self.hide()
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from DB_Scripts.Database_User import verify_admin_credentials

class AdminLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Login')
        self.resize(600, 400)

        self.admin_id_input = QLineEdit()
        self.admin_id_input.setPlaceholderText('Admin ID')
        self.admin_id_input.setAlignment(Qt.AlignCenter)
        self.admin_id_input.setStyleSheet("QLineEdit { border: 1px solid gray; border-radius: 5px; font-size: 16px; }")
        self.admin_id_input.setFixedWidth(250)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setStyleSheet("QLineEdit { border: 1px solid gray; border-radius: 5px; font-size: 16px; }")
        self.password_input.setFixedWidth(250)

        self.login_button = QPushButton('Login')
        self.login_button.setStyleSheet("QPushButton { border: 1px solid gray; border-radius: 5px; font-size: 14px; }")
        self.login_button.clicked.connect(self.login)
        self.login_button.setFixedSize(200, 40)

        self.signup_button = QPushButton('Sign Up')
        self.signup_button.setStyleSheet("QPushButton { border: 1px solid gray; border-radius: 5px; font-size: 14px; }")
        self.signup_button.clicked.connect(self.redirect_to_signup)
        self.signup_button.setFixedSize(200, 40)

        self.back_button = QPushButton('Back')
        self.back_button.setStyleSheet("QPushButton { border: 1px solid gray; border-radius: 5px; font-size: 14px; }")
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setFixedSize(200, 40)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.signup_button)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.admin_id_input)
        input_layout.addWidget(self.password_input)
        input_layout.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        admin_label = QLabel('Admin Login')
        admin_label.setAlignment(Qt.AlignCenter)
        admin_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(admin_label)
        main_layout.addSpacing(20)  # Add spacing below the title
        main_layout.addLayout(input_layout)
        main_layout.addSpacing(20)  # Add spacing between the text boxes and buttons
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)  # Add the back button centered
        main_layout.addStretch(1)
        main_layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(main_layout)

    def login(self):
        admin_id = self.admin_id_input.text()
        password = self.password_input.text()
        if verify_admin_credentials(admin_id, password):
            print('Admin logged in successfully!')
        else:
            print('Invalid admin credentials')

    def redirect_to_signup(self):
        from AdminSignup import AdminSignup
        self.admin_signup_window = AdminSignup()
        self.admin_signup_window.show()
        self.hide()

    def go_back(self):
        from StartPage import StartPage
        self.start_page = StartPage()
        self.start_page.show()
        self.hide()
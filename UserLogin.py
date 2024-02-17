from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from DB_Scripts.Database_User import verify_user_credentials
from DB_Scripts.Database_User import update_user_status

# Global variable to store the previous window
previous_window = None

class UserLogin(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('User Login')
        self.resize(600, 400)

        self.user_id_input = QLineEdit()
        self.user_id_input.setPlaceholderText('User ID')
        self.user_id_input.setAlignment(Qt.AlignCenter)
        self.user_id_input.setStyleSheet("QLineEdit { border: 1px solid gray; border-radius: 5px; font-size: 16px; }")
        self.user_id_input.setFixedWidth(250)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setStyleSheet("QLineEdit { border: 1px solid gray; border-radius: 5px; font-size: 16px; }")
        self.password_input.setFixedWidth(250)

        self.login_button = QPushButton('Login')
        self.login_button.setStyleSheet("QPushButton { border: 1px solid gray; border-radius: 5px; font-size: 14px; }")
        self.login_button.clicked.connect(self.login)
        self.login_button.setFixedSize(150, 40)

        self.back_button = QPushButton('Back')
        self.back_button.setStyleSheet("QPushButton { border: 1px solid gray; border-radius: 5px; font-size: 14px; }")
        self.back_button.clicked.connect(self.go_to_start_page)
        self.back_button.setFixedSize(150, 40)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.back_button)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.user_id_input)
        input_layout.addWidget(self.password_input)
        input_layout.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addStretch(1)
        user_label = QLabel('User Login')
        user_label.setAlignment(Qt.AlignCenter)
        user_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(user_label)
        main_layout.addSpacing(20)  # Add spacing below the title
        main_layout.addLayout(input_layout)
        main_layout.addSpacing(20)  # Add spacing between the text boxes and buttons
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        main_layout.setContentsMargins(50, 50, 50, 50)
        self.setLayout(main_layout)

    def login(self):
        user_id = self.user_id_input.text()
        password = self.password_input.text()
        if verify_user_credentials(user_id, password):
            update_user_status(user_id, 'Logged In')
            print('User logged in successfully!')
        else:
            print('Invalid user credentials')

    def go_to_start_page(self):
        from StartPage import StartPage
        self.start_page = StartPage()
        self.start_page.show()
        self.hide()
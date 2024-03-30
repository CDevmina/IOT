from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidgetItem, QFrame, \
    QTableWidget
from DB_Scripts.Database_User import add_user, get_all_users, delete_user


# noinspection PyUnresolvedReferences
class AdminUserAdd(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin User Add')
        self.resize(800, 600)

        self.user_list = QTableWidget()
        self.user_list.setColumnCount(2)
        self.user_list.setHorizontalHeaderLabels(["ID", "Password"])
        self.update_user_list()

        self.add_user_frame = QFrame()
        self.add_user_layout = QHBoxLayout(self.add_user_frame)
        self.add_user_id_input = QLineEdit()
        self.add_user_id_input.setPlaceholderText('User ID')
        self.add_user_password_input = QLineEdit()
        self.add_user_password_input.setPlaceholderText('Password')
        self.add_user_button = QPushButton('Confirm Add')
        self.add_user_button.clicked.connect(self.add_user)
        self.add_user_layout.addWidget(self.add_user_id_input)
        self.add_user_layout.addWidget(self.add_user_password_input)
        self.add_user_layout.addWidget(self.add_user_button)
        self.add_user_frame.hide()

        self.delete_user_frame = QFrame()
        self.delete_user_layout = QHBoxLayout(self.delete_user_frame)
        self.delete_user_id_input = QLineEdit()
        self.delete_user_id_input.setPlaceholderText('User ID')
        self.delete_user_button = QPushButton('Confirm Delete')
        # noinspection PyUnresolvedReferences
        self.delete_user_button.clicked.connect(self.delete_user)
        self.delete_user_layout.addWidget(self.delete_user_id_input)
        self.delete_user_layout.addWidget(self.delete_user_button)
        self.delete_user_frame.hide()

        self.show_add_user_button = QPushButton('Add User')
        self.show_add_user_button.clicked.connect(self.show_add_user_layout)

        self.show_delete_user_button = QPushButton('Delete User')
        self.show_delete_user_button.clicked.connect(self.show_delete_user_layout)

        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.go_back)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.show_add_user_button)
        button_layout.addWidget(self.show_delete_user_button)
        button_layout.addWidget(self.back_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.user_list)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.add_user_frame)
        main_layout.addWidget(self.delete_user_frame)
        self.setLayout(main_layout)

    def update_user_list(self):
        self.user_list.setRowCount(0)  # Clear the table
        users = get_all_users()
        for user in users:
            row = self.user_list.rowCount()
            self.user_list.insertRow(row)
            self.user_list.setItem(row, 0, QTableWidgetItem(str(user[0])))
            self.user_list.setItem(row, 1, QTableWidgetItem(str(user[1])))

    def show_add_user_layout(self):
        self.add_user_frame.show()
        self.delete_user_frame.hide()

    def show_delete_user_layout(self):
        self.delete_user_frame.show()
        self.add_user_frame.hide()

    def add_user(self):
        user_id = self.add_user_id_input.text()
        password = self.add_user_password_input.text()
        add_user(user_id, password)
        self.update_user_list()

    def go_back(self):
        from AdminHome import AdminHome
        self.admin_home = AdminHome()
        self.admin_home.show()
        self.hide()

    def delete_user(self):
        user_id = self.delete_user_id_input.text()
        delete_user(user_id)
        self.update_user_list()

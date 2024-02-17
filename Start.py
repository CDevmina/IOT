import sys
from PyQt5.QtWidgets import QApplication
from AdminHome import AdminHome

if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin_home =AdminHome ()
    admin_home.show()
    sys.exit(app.exec_())
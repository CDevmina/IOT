import sys
from PyQt5.QtWidgets import QApplication
from StartPage import StartPage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    StartPage = StartPage()
    StartPage.show()
    sys.exit(app.exec_())

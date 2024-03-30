from PyQt5.QtWidgets import QApplication, QInputDialog

def get_license_plate_manually():
    app = QApplication.instance()
    if not app:
        app = QApplication([])

    text, ok = QInputDialog.getText(None, "Enter License Plate",
                                    "License plate not detected. Please enter the license plate manually:")
    if ok and text:
        return str(text)
    else:
        return None
import sys

from PyQt6.QtWidgets import QApplication

from controller import MapController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = MapController()
    sys.exit(app.exec())

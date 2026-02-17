import sys

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel

Shirota = 55.752004
Dolgota = 37.617734
Zoom = 15


class ApiMapsApp(QWidget):

    def __init__(self):
        super().__init__()
        self.map_label = None
        self.shirota = Shirota
        self.dolgota = Dolgota
        self.zoom = Zoom
        self.initUI()

    def initUI(self):
        self.setWindowTitle('API Maps')
        self.setFixedSize(600, 450)
        self.map_label = QLabel(self)
        self.get_map()

    def get_map(self):
        api_server = "https://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{self.dolgota},{self.shirota}",
            "z": str(Zoom),
            "l": "map"
        }

        response = requests.get(api_server, params=params)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        self.map_label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.shirota += 0.01
            self.get_map()
        elif event.key() == Qt.Key.Key_Down:
            self.shirota -= 0.01
            self.get_map()
        elif event.key() == Qt.Key.Key_Left:
            self.dolgota -= 0.01
            self.get_map()
        elif event.key() == Qt.Key.Key_Right:
            self.dolgota += 0.01
            self.get_map()
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ApiMapsApp()
    ex.show()
    sys.exit(app.exec())

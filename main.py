import sys
import requests
from PyQt6.QtGui import QPixmap, QKeyEvent
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import Qt

Shirota = "55.752004"
Dolgota = "37.617734"
Zoom = 15

MIN_ZOOM = 0
MAX_ZOOM = 21


class ApiMapsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.map_label = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('API Maps')
        self.setFixedSize(600, 450)
        self.map_label = QLabel(self)
        self.map_label.setFixedSize(600, 450)
        self.get_map()

    def get_map(self):
        global Zoom
        api_server = "https://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{Dolgota},{Shirota}",
            "z": Zoom,
            "l": "map",
            "size": "600,450"
        }

        try:
            response = requests.get(api_server, params=params)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.map_label.setPixmap(pixmap)
            self.map_label.resize(pixmap.size())
        except Exception as e:
            print(f"Ошибка при загрузке карты: {e}")

    def keyPressEvent(self, event: QKeyEvent):
        global Zoom

        if event.key() == Qt.Key.Key_PageUp:
            if Zoom < MAX_ZOOM:
                Zoom += 1
                self.get_map()

        elif event.key() == Qt.Key.Key_PageDown:
            if Zoom > MIN_ZOOM:
                Zoom -= 1
                self.get_map()

        super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ApiMapsApp()
    ex.show()
    sys.exit(app.exec())
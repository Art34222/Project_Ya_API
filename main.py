import sys

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton

Shirota = 55.752004
Dolgota = 37.617734
Zoom = 15
MIN_ZOOM = 0
MAX_ZOOM = 21


class ApiMapsApp(QWidget):

    def __init__(self):
        super().__init__()
        self.theme_btn = None
        self.map_label = None
        self.theme = "light"
        self.api_key = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
        self.shirota = Shirota
        self.dolgota = Dolgota
        self.zoom = Zoom
        self.initUI()

    def initUI(self):
        self.setWindowTitle('API Maps')
        self.setFixedSize(600, 450)
        self.map_label = QLabel(self)
        self.get_map()

        self.theme_btn = QPushButton("Сменить тему", self)
        self.theme_btn.setGeometry(470, 410, 120, 30)
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.get_map()

    def get_map(self):
        api_server = "https://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{self.dolgota},{self.shirota}",
            "z": str(Zoom),
            "l": "map",
            "theme": self.theme,
            "api_key": self.api_key
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

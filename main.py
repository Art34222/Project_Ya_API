import sys
import requests
import traceback
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QPixmap, QPainter, QPen, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout

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
        self.search_input = None
        self.search_btn = None
        self.theme = "light"
        self.api_key = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
        self.apikey_geo = "8013b162-6b42-4997-9691-77b7074026e0"
        self.shirota = Shirota
        self.dolgota = Dolgota
        self.zoom = Zoom
        self.initUI()
        self.load_map_on_startup()  # Вызываем загрузку карты при старте

    def initUI(self):
        self.setWindowTitle('API Maps')
        self.setFixedSize(600, 500)
        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Введите адрес или объект...')
        layout.addWidget(self.search_input)

        self.search_btn = QPushButton('Искать', self)
        self.search_btn.clicked.connect(self.perform_search)
        layout.addWidget(self.search_btn)

        self.map_label = QLabel()
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.map_label)

        self.theme_btn = QPushButton("Сменить тему", self)
        self.theme_btn.setGeometry(470, 410, 120, 30)
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.theme_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.theme_btn)

        self.setLayout(layout)

    def load_map_on_startup(self):
        """Загружает карту сразу при запуске приложения с выводом ошибок через traceback."""
        try:
            self.get_map()
        except Exception as e:
            print("Ошибка при начальной загрузке карты:")
            traceback.print_exc()

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        try:
            self.get_map()
        except Exception as e:
            print("Ошибка при смене темы:")
            traceback.print_exc()

    def get_map(self):
        api_server = "https://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{self.dolgota},{self.shirota}",
            "z": str(self.zoom),
            "l": "map",
            "theme": self.theme,
            "api_key": self.api_key
        }

        response = requests.get(api_server, params=params)
        response.raise_for_status()  # Бросает исключение при HTTP-ошибках

        pixmap = QPixmap()
        pixmap.loadFromData(response.content)

        if pixmap.isNull():
            raise ValueError("Не удалось загрузить изображение карты")

        # Рисуем красную точку в центре
        painter = QPainter(pixmap)
        pen = QPen(QColor("red"))
        pen.setWidth(6)
        painter.setPen(pen)
        center_x = pixmap.width() // 2
        center_y = pixmap.height() // 2
        painter.drawPoint(center_x, center_y)
        painter.end()

        self.map_label.setPixmap(pixmap)
        self.map_label.resize(pixmap.size())

    def perform_search(self):
        query = self.search_input.text().strip()
        if not query:
            return

        geocode_api = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": self.apikey_geo,
            "geocode": query,
            "format": "json"
        }

        try:
            response = requests.get(geocode_api, params=params)
            response.raise_for_status()
            data = response.json()

            # Проверяем, есть ли результаты
            if not data["response"]["GeoObjectCollection"]["featureMember"]:
                raise ValueError("По запросу не найдено объектов")

            pos = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            lon, lat = map(float, pos.split())
            self.shirota = lat
            self.dolgota = lon
            self.get_map()
        except Exception as e:
            print("Ошибка при поиске:")
            traceback.print_exc()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_PageUp:
            if self.zoom < MAX_ZOOM:
                self.zoom += 1
                try:
                    self.get_map()
                except Exception as e:
                    print("Ошибка при увеличении масштаба:")
                    traceback.print_exc()
        elif event.key() == Qt.Key.Key_PageDown:
            if self.zoom > MIN_ZOOM:
                self.zoom -= 1
                try:
                    self.get_map()
                except Exception as e:
                    print("Ошибка при уменьшении масштаба:")
                    traceback.print_exc()
        elif event.key() == Qt.Key.Key_Up:
            self.shirota += 0.01
            try:
                self.get_map()
            except Exception as e:
                print("Ошибка при перемещении вверх:")
                traceback.print_exc()
        elif event.key() == Qt.Key.Key_Down:
            self.shirota -= 0.01
            try:
                self.get_map()
            except Exception as e:
                print("Ошибка при перемещении вниз:")
                traceback.print_exc()
        elif event.key() == Qt.Key.Key_Left:
            self.dolgota -= 0.01
            try:
                self.get_map()
            except Exception as e:
                print("Ошибка при перемещении влево:")
                traceback.print_exc()
        elif event.key() == Qt.Key.Key_Right:
            self.dolgota += 0.01
            try:
                self.get_map()
            except Exception as e:
                print("Ошибка при перемещении вправо:")
                traceback.print_exc()
        else:
            super().keyPressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ApiMapsApp()
    ex.show()
    sys.exit(app.exec())

import sys
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QComboBox

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
        self.view_combo = None
        self.theme = "light"
        self.api_key = ""
        self.shirota = Shirota
        self.dolgota = Dolgota
        self.zoom = Zoom
        self.map_types = {
            "Базовая карта": "map",
            "Автомобильная навигация": "map,trf",
            "Общественный транспорт": "map,trf,masstransit",
            "Спутниковая": "sat",
            "Гибридная": "sat,skl"
        }
        self.current_view = "map"
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

        self.view_combo = QComboBox(self)
        self.view_combo.setGeometry(10, 410, 200, 30)
        for display_name in self.map_types.keys():
            self.view_combo.addItem(display_name)
        default_index = list(self.map_types.keys()).index("Базовая карта")
        self.view_combo.setCurrentIndex(default_index)
        self.view_combo.currentTextChanged.connect(self.change_map_view)

    def change_map_view(self, selected_text):
        self.current_view = self.map_types[selected_text]
        self.get_map()

    def toggle_theme(self):
        self.get_map()

    def get_map(self):
        api_server = "https://static-maps.yandex.ru/1.x/"
        ll = f"{self.dolgota},{self.shirota}"

        params = {
            "ll": ll,
            "z": self.zoom,
            "l": self.current_view,
            "size": "600,450"
        }
        try:
            print(f"Запрос: {api_server}?ll={ll}&z={self.zoom}&l={self.current_view}")
            response = requests.get(api_server, params=params)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            if not pixmap.isNull():
                self.map_label.setPixmap(pixmap)
                self.map_label.resize(pixmap.size())
                self.map_label.move((600 - pixmap.width()) // 2, (450 - pixmap.height()) // 2)
            else:
                print("Не удалось загрузить изображение")

        except requests.exceptions.HTTPError as e:
            print(f"HTTP ошибка ({response.status_code}): {e}")
            print(f"URL запроса: {response.url}")
            if response.status_code == 400:
                print("Проверьте корректность параметров запроса")
        except Exception as e:
            print(f"Ошибка при загрузке карты: {e}")

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_PageUp:
            if self.zoom < MAX_ZOOM:
                self.zoom += 1
                self.get_map()
        elif event.key() == Qt.Key.Key_PageDown:
            if self.zoom > MIN_ZOOM:
                self.zoom -= 1
                self.get_map()
        elif event.key() == Qt.Key.Key_Up:
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
            super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ApiMapsApp()
    ex.show()
    sys.exit(app.exec())
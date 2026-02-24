from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QKeyEvent
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout


class MapView(QWidget):
    search_signal = pyqtSignal(str)
    theme_signal = pyqtSignal()
    move_signal = pyqtSignal(int, int)
    zoom_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('API Maps MVC')
        self.setFixedSize(600, 500)

        layout = QVBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Введите адрес...')
        layout.addWidget(self.search_input)

        self.search_btn = QPushButton('Искать')
        self.search_btn.clicked.connect(self._on_search_click)
        self.search_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.search_btn)

        self.map_label = QLabel()
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.map_label)

        self.theme_btn = QPushButton("Сменить тему", self)
        self.theme_btn.setGeometry(470, 410, 120, 30)
        self.theme_btn.clicked.connect(self._on_theme_click)
        self.theme_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self.theme_btn)

        self.setLayout(layout)
        self.setFocus()

    def update_image(self, image_data):
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)

        if not pixmap.isNull():
            painter = QPainter(pixmap)
            painter.setPen(QPen(QColor("red"), 6))
            painter.drawPoint(pixmap.width() // 2, pixmap.height() // 2)
            painter.end()
            self.map_label.setPixmap(pixmap)

    def show_error(self, message):
        print(f"Error: {message}")

    def _on_search_click(self):
        text = self.search_input.text().strip()
        self.search_signal.emit(text)
        self.setFocus()

    def _on_theme_click(self):
        self.theme_signal.emit()
        self.setFocus()

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            self.zoom_signal.emit(1)
        elif key == Qt.Key.Key_PageDown:
            self.zoom_signal.emit(-1)
        elif key == Qt.Key.Key_Up:
            self.move_signal.emit(0, 1)
        elif key == Qt.Key.Key_Down:
            self.move_signal.emit(0, -1)
        elif key == Qt.Key.Key_Left:
            self.move_signal.emit(-1, 0)
        elif key == Qt.Key.Key_Right:
            self.move_signal.emit(1, 0)
        else:
            super().keyPressEvent(event)

    def mousePressEvent(self, event):
        self.setFocus()
        super().mousePressEvent(event)
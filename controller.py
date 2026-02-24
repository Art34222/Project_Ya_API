import traceback

from model import MapModel
from view import MapView


class MapController:
    def __init__(self):
        self.model = MapModel()
        self.view = MapView()

        self.view.search_signal.connect(self.search)
        self.view.theme_signal.connect(self.toggle_theme)
        self.view.move_signal.connect(self.move)
        self.view.zoom_signal.connect(self.zoom)

        self.update_map()
        self.view.show()

    def update_map(self):
        try:
            data = self.model.get_map_image()
            self.view.update_image(data)
        except Exception:
            traceback.print_exc()
            self.view.show_error("Не удалось загрузить карту")

    def search(self, query):
        try:
            self.model.geocode(query)
            self.update_map()
        except Exception:
            traceback.print_exc()
            self.view.show_error("Объект не найден")

    def toggle_theme(self):
        self.model.toggle_theme()
        self.update_map()

    def move(self, dx, dy):
        self.model.move(dx, dy)
        self.update_map()

    def zoom(self, step):
        self.model.change_zoom(step)
        self.update_map()

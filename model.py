import requests

from settings import *


class MapModel:
    def __init__(self):
        self.lat = DEFAULT_LAT
        self.lon = DEFAULT_LON
        self.zoom = DEFAULT_ZOOM
        self.theme = "light"

    def move(self, dx, dy):
        """dx, dy: -1, 0 или 1. Умножаем на шаг."""
        self.lat += dy * STEP_COORD
        self.lon += dx * STEP_COORD

    def change_zoom(self, step):
        new_zoom = self.zoom + step
        if MIN_ZOOM <= new_zoom <= MAX_ZOOM:
            self.zoom = new_zoom

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"

    def get_map_image(self):
        """Возвращает байты картинки или вызывает ошибку."""
        api_server = "https://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": str(self.zoom),
            "l": "map",
            "theme": self.theme,
            "api_key": API_KEY_MAPS
        }
        response = requests.get(api_server, params=params)
        response.raise_for_status()
        return response.content

    def geocode(self, query):
        """Обновляет координаты по запросу или вызывает ошибку."""
        if not query:
            return

        geocode_api = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "apikey": API_KEY_GEO,
            "geocode": query,
            "format": "json"
        }

        response = requests.get(geocode_api, params=params)
        response.raise_for_status()
        data = response.json()

        if not data["response"]["GeoObjectCollection"]["featureMember"]:
            raise ValueError("Объект не найден")

        pos = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        lon, lat = map(float, pos.split())
        self.lat = lat
        self.lon = lon

# navigation.py

# Этот файл отвечает за логику перемещения от точки А до точки B.
# Тут мы считаем направление, угол и понимаем, куда ехать дальше.
# Никакой магии — просто немного геометрии и здравого смысла.

import math

class Navigation:
    """
    Простой навигационный модуль. Даёт направление движения.
    Точки подаются в формате (x, y) — как на карте.
    """

    def __init__(self, point_a, point_b):
        self.point_a = point_a  # Откуда стартуем
        self.point_b = point_b  # Куда хотим приехать

    def calculate_direction(self):
        """
        Возвращает угол между точками в градусах.
        0° — это строго на восток, дальше по часовой стрелке.
        """
        dx = self.point_b[0] - self.point_a[0]
        dy = self.point_b[1] - self.point_a[1]

        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)

        return angle_deg

    def distance(self):
        """
        Прямое расстояние от А до B (по теореме Пифагора).
        """
        dx = self.point_b[0] - self.point_a[0]
        dy = self.point_b[1] - self.point_a[1]
        return math.hypot(dx, dy)


# Пример использования:
# nav = Navigation((0, 0), (10, 10))
# print(nav.calculate_direction())  # → 45.0°
# print(nav.distance())             # → 14.14...

# steering_logic.py

# Этот файл — сердце поворота.
# Здесь считается, насколько сильно нужно повернуть колёса, чтобы попасть в линию между A и B.
# Можно заменить на Pure Pursuit, но пока делаем просто, наглядно и понятно.

import math

class SteeringLogic:
    """
    Простейшая логика руления: считаем отклонение от нужного курса.
    Предполагаем, что машина движется в направлении 'heading', а цель — точка B.
    """

    def __init__(self, current_pos, target_pos, heading_deg):
        self.current_pos = current_pos  # (x, y) текущие координаты
        self.target_pos = target_pos    # (x, y) цель
        self.heading_deg = heading_deg  # текущий курс (в градусах)

    def calculate_steering_angle(self):
        """
        Возвращает угол поворота руля.
        Если результат положительный — поворачиваем вправо,
        если отрицательный — влево.
        """

        dx = self.target_pos[0] - self.current_pos[0]
        dy = self.target_pos[1] - self.current_pos[1]

        target_angle = math.degrees(math.atan2(dy, dx))
        angle_diff = target_angle - self.heading_deg

        # Приводим угол к диапазону [-180, 180]
        while angle_diff < -180:
            angle_diff += 360
        while angle_diff > 180:
            angle_diff -= 360

        return angle_diff


# Пример:
# logic = SteeringLogic((0, 0), (10, 10), heading_deg=0)
# print(logic.calculate_steering_angle())  # → ≈ 45°

# ui_controller.py
#
# Тут живёт всё, что связано с кнопками, окнами и тем,
# как человек общается с автоподруливанием.
# Нажал кнопку — мотор поехал. Красота.

from PyQt5 import QtWidgets, uic
from src.modbus_controller import ModbusController
import sys


class MainWindow(QtWidgets.QMainWindow):
    """
    Главное окно управления автоподруливанием.

    Интерфейс простой: три кнопки (← → ■) и поле для логов.
    Это не дизайн Tesla, но свою работу делает честно.
    """
    def __init__(self):
        super().__init__()

        # Загружаем форму, собранную в Qt Designer
        uic.loadUi("ui/main_window.ui", self)

        # Подключаемся к мотору
        try:
            self.motor = ModbusController(port='COM12', baudrate=115200)
            self.log.append("🔌 Подключено к мотору на COM12")
        except Exception as e:
            self.log.append(f"❌ Ошибка подключения: {e}")
            return

        # Привязываем кнопки к действиям
        self.btnLeft.clicked.connect(self.turn_left)
        self.btnRight.clicked.connect(self.turn_right)
        self.btnStop.clicked.connect(self.stop_motor)

        # Приветственное сообщение
        self.log.append("🚜 FAB Autosteer запущен. Готов к подруливанию!")

    def turn_left(self):
        self.motor.turn_left(150)
        self.log.append("⬅️ Мотор повернул влево")

    def turn_right(self):
        self.motor.turn_right(150)
        self.log.append("➡️ Мотор повернул вправо")

    def stop_motor(self):
        self.motor.stop()
        self.log.append("⏹️ Мотор остановлен")


def launch_ui():
    """
    Просто запускаем окно.
    Можно даже пальцем в экран тыкнуть, если сенсорный :)
    """
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

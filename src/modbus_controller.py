# modbus_controller.py
#
# Это тот самый файл, где мы дергаем мотор направо-налево.
# Управление через Modbus RTU, ничего лишнего.
# Если порт не открывается — не бей по клавиатуре, просто проверь кабель :)


import serial
import time


class ModbusController:
    """
    Простой класс для общения с рулевым мотором по Modbus RTU.

    Наша задача — не заставить мотор "крутиться", а сделать это
    прозрачно, стабильно и по-человечески.
    """

    def __init__(self, port='COM12', baudrate=9600):
        """
        Инициализация COM-порта.

        Обычно мотор подключён через USB-UART адаптер.
        Настройки скорости и порта — по умолчанию стандартные.
        """
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        if self.ser.is_open:
            print(f"[✅] Подключено к {port} — всё готово к управлению.")
        else:
            raise Exception(f"[❌] Порт {port} не удалось открыть.")

    def send_command(self, data: bytes):
        """
        Добавляем к команде контрольную сумму (CRC16) и отправляем в мотор.
        """
        crc = self.crc16(data)
        packet = data + crc
        print(f"[TX] → {packet.hex(' ')}")  # Видим, что реально уходит в порт
        self.ser.write(packet)
        time.sleep(0.05)  # Дать мотору чуть "вдохнуть"

    def turn_left(self, speed: int = 100):
        """
        Повернуть влево с заданной скоростью.

        Значение скорости зависит от прошивки мотора — подбирается опытным путём.
        """
        command = bytes([
            0x01, 0x10,           # ID + функция (Write Multiple Registers)
            0x01, 0x35,           # Регистр "влево" (предположительно)
            0x00, 0x02,           # Пишем 2 регистра
            0x04,                 # Всего 4 байта данных
            0x00, speed >> 8,     # Старший байт скорости
            0x00, speed & 0xFF    # Младший байт скорости
        ])
        self.send_command(command)

    def turn_right(self, speed: int = 100):
        """
        Повернуть вправо. Вся структура команды та же — меняется только адрес.
        """
        command = bytes([
            0x01, 0x10,
            0x01, 0x36,           # Регистр "вправо" (предположительно)
            0x00, 0x02,
            0x04,
            0x00, speed >> 8,
            0x00, speed & 0xFF
        ])
        self.send_command(command)

    def stop(self):
        """
        Полная остановка: сбрасываем скорость на ноль.
        """
        command = bytes([
            0x01, 0x10,
            0x01, 0x35,
            0x00, 0x02,
            0x04,
            0x00, 0x00,
            0x00, 0x00
        ])
        self.send_command(command)

    @staticmethod
    def crc16(data: bytes) -> bytes:
        """
        Классическая Modbus CRC16 — без неё мотор просто молчит.
        """
        crc = 0xFFFF
        for b in data:
            crc ^= b
            for _ in range(8):
                if crc & 0x01:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc.to_bytes(2, byteorder='little')

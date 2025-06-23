# main.py
#
# Это самый ленивый способ проверить, крутится ли мотор.
# Без интерфейсов, без графики — просто вводим 1, 2 или 3.
# И если что-то не работает — виноват не ты, а кабель 😉

from src.modbus_controller import ModbusController

# Пробуем подключиться к мотору.
# Если COM-порт не тот — будет ор.
motor = ModbusController(port='COM12', baudrate=115200)

print("🚜 FAB Autosteer — ручной тест мотора")
print("──────────────────────────────────────\n")
print("Что можно делать:")
print(" [1] ← Повернуть влево")
print(" [2] → Повернуть вправо")
print(" [3] ■ Остановить")
print(" [q] Выйти\n")

while True:
    cmd = input("👉 Введите команду: ").strip()

    if cmd == '1':
        print("↪️  Влево на 150 скорости")
        motor.turn_left(150)
    elif cmd == '2':
        print("↩️  Вправо на 150 скорости")
        motor.turn_right(150)
    elif cmd == '3':
        print("⏹️  Стоп. Отдыхаем.")
        motor.stop()
    elif cmd.lower() == 'q':
        print("👋 Выход. Мотор прощается с тобой.")
        break
    else:
        print("❓ Я такого не знаю. Введи 1, 2, 3 или q.")

# main.py

import time
import board
import adafruit_dht

# Импортируем класс и константы из lcd_i2c.py
from lcd_i2c import LCD1602, LCD_LINE_1, LCD_LINE_2

# Инициализация датчика DHT22 на GPIO18 (D18 в terms of board)
# Если возникают ошибки, попробуйте dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
dhtDevice = adafruit_dht.DHT22(board.D18)

# Создаём объект LCD (адрес 0x27, ширина 16)
lcd = LCD1602(i2c_bus=1, i2c_addr=0x27, width=16)

def get_cpu_temp():
    """Возвращает температуру процессора Raspberry Pi, или None, если ошибка."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            t_str = f.read()
        return float(t_str) / 1000.0
    except:
        return None

try:
    while True:
        try:
            # Считываем показания DHT22
            temp_c = dhtDevice.temperature
            hum = dhtDevice.humidity

            # Считываем температуру CPU
            cpu_c = get_cpu_temp()

            # Формируем строки для LCD
            # (не используем "°", только "C", чтобы избежать проблем с символами)
            if temp_c is not None and hum is not None:
                line1 = f"T={temp_c:.1f}C H={hum:.1f}%"
            else:
                line1 = "DHT error"

            if cpu_c is not None:
                line2 = f"CPU={cpu_c:.1f}C"
            else:
                line2 = "CPU error"

            # Выводим на LCD
            lcd.message(line1, LCD_LINE_1)
            lcd.message(line2, LCD_LINE_2)

        except RuntimeError as err:
            # DHT22 нередко выбрасывает RuntimeError при некорректном чтении
            lcd.message("DHT RuntimeErr", LCD_LINE_1)
            lcd.message("Retry...", LCD_LINE_2)
            time.sleep(2)
            continue
        except Exception as e:
            # Если произошла нештатная ошибка — выведем на экран и выйдем из цикла
            lcd.clear()
            lcd.message("Fatal error", LCD_LINE_1)
            lcd.message(str(e), LCD_LINE_2)
            time.sleep(2)
            break

        # Спим 2 секунды перед следующим чтением
        time.sleep(2)

except KeyboardInterrupt:
    # При нажатии Ctrl+C
    lcd.clear()
    lcd.close()
    print("Exit by user")

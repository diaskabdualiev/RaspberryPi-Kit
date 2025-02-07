# lcd_i2c.py
#
# Простейшая библиотека управления 16x2 LCD по I2C (через PCF8574)
# Работает в 4-битном режиме, использует smbus2 для обмена по I2C.

import smbus2
import time

# Константы для режимов и команд LCD
LCD_CHR = 1       # Режим передачи данных (символов)
LCD_CMD = 0       # Режим передачи команд
LCD_BACKLIGHT = 0x08  # 0x08 для включённой подсветки, 0x00 — для выключенной
ENABLE = 0b00000100   # бит "E" в PCF8574
E_PULSE = 0.0005
E_DELAY = 0.0005

# Обычно для 16x2
LCD_WIDTH = 16         # ширина строки
LCD_LINE_1 = 0x80      # адрес начала 1-й строки
LCD_LINE_2 = 0xC0      # адрес начала 2-й строки

class LCD1602:
    def __init__(self, i2c_bus=1, i2c_addr=0x27, width=16):
        """
        i2c_bus  - номер шины I2C (обычно 1 на современных Raspberry Pi)
        i2c_addr - адрес модуля PCF8574 (часто 0x27 или 0x3F)
        width    - ширина LCD в символах (16 или 20)
        """
        self.bus = smbus2.SMBus(i2c_bus)
        self.i2c_addr = i2c_addr
        self.width = width
        
        self._lcd_init()

    def _toggle_enable(self, data):
        """Небольшой «тоггл», чтобы зафиксировать данные на ножке E."""
        self.bus.write_byte(self.i2c_addr, data | ENABLE)
        time.sleep(E_DELAY)
        self.bus.write_byte(self.i2c_addr, data & ~ENABLE)
        time.sleep(E_PULSE)

    def _lcd_byte(self, bits, mode):
        """
        Отправляет 1 байт (команду или данные) в два приёма по 4 бита (4-битный режим).
        bits: байт данных
        mode: LCD_CHR (данные) или LCD_CMD (команда)
        """
        # Высокая тетрада (старшие 4 бита)
        high = mode | (bits & 0xF0) | LCD_BACKLIGHT
        # Низкая тетрада (младшие 4 бита)
        low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT
        
        # Отправляем старшие 4 бита
        self.bus.write_byte(self.i2c_addr, high)
        self._toggle_enable(high)
        
        # Отправляем младшие 4 бита
        self.bus.write_byte(self.i2c_addr, low)
        self._toggle_enable(low)

    def _lcd_init(self):
        """Инициализация дисплея в 4-битном режиме."""
        self._lcd_byte(0x33, LCD_CMD)  # Переход в 4-бит
        self._lcd_byte(0x32, LCD_CMD)
        self._lcd_byte(0x06, LCD_CMD)  # Направление курсора (сдвиг)
        self._lcd_byte(0x0C, LCD_CMD)  # Включить дисплей, курсор выкл
        self._lcd_byte(0x28, LCD_CMD)  # 4-бит, 2 строки, 5x8 символы
        self.clear()

    def clear(self):
        """Очистка дисплея."""
        self._lcd_byte(0x01, LCD_CMD)  # Команда «clear display»
        time.sleep(E_DELAY)

    def message(self, text, line):
        """
        Вывод строки на указанную позицию (line — это LCD_LINE_1 или LCD_LINE_2).
        Если строка короче ширины дисплея, дополняется пробелами.
        """
        # Устанавливаем адрес строки
        self._lcd_byte(line, LCD_CMD)
        # Дополняем или обрезаем текст до нужной длины
        text = text.ljust(self.width, " ")
        # По символьно отправляем
        for char in text[:self.width]:
            self._lcd_byte(ord(char), LCD_CHR)

    def close(self):
        """Закрыть интерфейс I2C (если нужно)."""
        self.clear()
        self.bus.close()

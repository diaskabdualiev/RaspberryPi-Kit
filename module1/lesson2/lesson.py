from gpiozero import LED, Button  # Импортируем классы LED и Button
from signal import pause

led = LED(18)  # Определяем светодиод на GPIO17
button = Button(23)  # Определяем кнопку на GPIO2

# Функция, которая включит светодиод, когда нажмем кнопку
def led_on():
    print("Кнопка нажата! Включаем LED.")
    led.on()

# Функция, которая выключит светодиод, когда отпустим кнопку
def led_off():
    print("Кнопка отпущена! Выключаем LED.")
    led.off()

# Назначаем обработчики событий
button.when_pressed = led_on  # Когда кнопку нажали, включаем LED
button.when_released = led_off  # Когда кнопку отпустили, выключаем LED

# Бесконечный цикл ожидания, чтобы программа не завершалась
print("Нажми кнопку, чтобы включить светодиод!")
pause()

from gpiozero import LED  # Импортируем класс LED из библиотеки gpiozero
from time import sleep  # Импортируем sleep для задержек

led = LED(18)  # Определяем светодиод, подключенный к GPIO17

while True:  # Бесконечный цикл для мигания светодиода
    led.on()  # Включаем светодиод
    print("LED on")
    sleep(1)  # Ждём 1 секунду
    led.off()  # Выключаем светодиод
    print("LED off")
    sleep(1)  # Ждём 1 секунду

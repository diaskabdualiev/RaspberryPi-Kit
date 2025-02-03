import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Define the BCM pins
BUZZER_PIN = 18
BUTTON_PIN = 23

# Set the buzzer pin as an output
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Set the button pin as an input with an internal pull-down resistor
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        # Read the state of the button
        button_state = GPIO.input(BUTTON_PIN)
        
        if button_state == GPIO.HIGH:
            # If the button is pressed, turn the buzzer on
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            print("Button is pressed. Buzzer is ON.")
        else:
            # If the button is not pressed, turn the buzzer off
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            print("Button is not pressed. Buzzer is OFF.")
        
        # Delay to prevent excessive CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    # Cleanup GPIO settings when the program is interrupted (Ctrl+C)
    GPIO.cleanup()
    print("Program interrupted. GPIO cleaned up.")

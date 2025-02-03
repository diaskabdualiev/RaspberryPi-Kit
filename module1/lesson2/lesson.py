import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Set pin 18 (BCM) as an output for the LED
GPIO.setup(18, GPIO.OUT)

# Set pin 23 (BCM) as an input for the button, with a pull-down resistor
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        # Check if the button is pressed
        if GPIO.input(23) == GPIO.HIGH:
            # If the button is pressed, turn the LED on
            GPIO.output(18, GPIO.HIGH)
            print("Button is pressed, LED is ON")
        else:
            # Otherwise, turn the LED off
            GPIO.output(18, GPIO.LOW)
            print("Button is not pressed, LED is OFF")
        
        # Delay to prevent busy waiting
        time.sleep(0.1)

except KeyboardInterrupt:
    # Catch the Ctrl+C keyboard interrupt and cleanup
    GPIO.cleanup()
    print("Program interrupted and GPIO cleaned up.")


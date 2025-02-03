import RPi.GPIO as GPIO
import time

# Define the BCM pin number to which the LED is connected
LED_PIN = 18

print("Initializing RPi.GPIO and configuring the pin...")

# Set the GPIO mode to use BCM numbering
GPIO.setmode(GPIO.BCM)

# Set the LED_PIN as an output pin
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    print("Starting the main loop (press Ctrl+C to exit)")
    while True:
        print("Turning the LED on (HIGH)")
        # Set the LED pin output to HIGH (3.3V)
        GPIO.output(LED_PIN, GPIO.HIGH)
        # Wait for 1 second
        time.sleep(1)

        print("Turning the LED off (LOW)")
        # Set the LED pin output to LOW (0V)
        GPIO.output(LED_PIN, GPIO.LOW)
        # Wait for 1 second
        time.sleep(1)

except KeyboardInterrupt:
    # This block is executed when the user presses Ctrl+C to interrupt the program
    print("\nProgram interrupted by the user (Ctrl+C). Cleaning up GPIO...")

finally:
    # Reset the GPIO configuration to its default state
    GPIO.cleanup()
    print("GPIO configuration has been cleaned up. Exiting the program.")
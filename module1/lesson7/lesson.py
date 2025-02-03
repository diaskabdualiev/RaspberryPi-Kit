import RPi.GPIO as GPIO
import time

# We use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Define the BCM pins for the ultrasonic sensor (HC-SR04 or similar) and buzzer
TRIG = 23   # Trigger pin of the ultrasonic sensor
ECHO = 24   # Echo pin of the ultrasonic sensor
BUZZER = 18 # Buzzer pin

# Setup the pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)

def measure_distance():
    """
    Sends a short trigger pulse to the ultrasonic sensor
    and measures the time for the echo signal to return.
    Converts that time into a distance in centimeters.
    """
    # Send trigger pulse
    print("DEBUG: Sending trigger pulse...")
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG, False)
    
    # Initialize variables for start/end times
    start_time = 0
    end_time = 0
    
    # Wait for the ECHO pin to go HIGH (signal start)
    print("DEBUG: Waiting for ECHO to go HIGH...")
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    
    # Wait for the ECHO pin to go LOW (signal end)
    print("DEBUG: ECHO went HIGH, waiting to go LOW...")
    while GPIO.input(ECHO) == 1:
        end_time = time.time()
    
    # Calculate the duration of the pulse
    duration = end_time - start_time
    
    # Convert duration to distance (34300 cm/s is the speed of sound)
    distance = (duration * 34300) / 2
    
    print(f"DEBUG: Measured distance duration = {duration:.6f} s -> {distance:.2f} cm")
    return distance

try:
    print("INFO: Starting parking sensor loop (press Ctrl+C to quit)...")
    while True:
        dist = measure_distance()
        print(f"INFO: Current distance = {dist:.1f} cm")
        
        # Example thresholds — adjust as needed
        if dist <= 5:
            print("DEBUG: Distance <= 5 cm => Buzzer with very short OFF time (almost continuous)")
            GPIO.output(BUZZER, GPIO.HIGH)
            time.sleep(0.1)  # short ON
            GPIO.output(BUZZER, GPIO.LOW)
            time.sleep(0.05) # very short OFF
            
        elif dist <= 10:
            print("DEBUG: Distance <= 10 cm => Fast beeps")
            GPIO.output(BUZZER, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER, GPIO.LOW)
            time.sleep(0.1)
            
        elif dist <= 20:
            print("DEBUG: Distance <= 20 cm => Moderate beeps")
            GPIO.output(BUZZER, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(BUZZER, GPIO.LOW)
            time.sleep(0.3)
            
        elif dist <= 30:
            print("DEBUG: Distance <= 30 cm => Slower beeps")
            GPIO.output(BUZZER, GPIO.HIGH)
            time.sleep(0.3)
            GPIO.output(BUZZER, GPIO.LOW)
            time.sleep(0.5)
            
        else:
            print("DEBUG: Distance > 30 cm => No beep")
            GPIO.output(BUZZER, GPIO.LOW)
            time.sleep(1)
            
except KeyboardInterrupt:
    # On Ctrl+C, clean up GPIO
    print("\nINFO: Program interrupted by user. Cleaning up GPIO...")
    GPIO.cleanup()
    print("INFO: GPIO cleaned up. Exiting.")

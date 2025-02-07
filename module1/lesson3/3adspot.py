from ads1115_lib import ADS1115
from time import sleep
a = ADS1115()

def MAP(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


while True:
    # Loop infinitely
    try:
        # Print readings into rows
        print(a.read_adc(0), end="\t")
        print(int(MAP(a.read_adc(0), 0, 32767, 0, 180)))
        sleep(0.1)
    except KeyboardInterrupt:
        # Exit loop
        print("\nProgram Stopped")
        break
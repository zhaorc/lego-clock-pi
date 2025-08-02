from RPi import GPIO
import signal
import time
import sys

switch_pin = 17
steps = 0

def count_steps():
    global steps
    steps = steps + 1

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(switch_pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)
    GPIO.add_event_detect(switch_pin, GPIO.RISING, callback=count_steps, bouncetime=100)
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        print(steps)
        time.sleep(5)

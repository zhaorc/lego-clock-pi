from RPi import GPIO
import signal
import time
import sys

switch_pin = 14
steps = 0

def count_steps(channel):
    print("now_value={}".format(GPIO.input(channel)))
    global steps
    steps = steps + 1
    print("steps={}".format(steps))

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(switch_pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)
    GPIO.add_event_detect(switch_pin, GPIO.FALLING, callback=count_steps, bouncetime=300)
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        print("ori_value={}".format(GPIO.input(switch_pin)))
        time.sleep(5)

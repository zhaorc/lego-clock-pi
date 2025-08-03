from RPi import GPIO
from driver import stepper
import time
import logging

def test_stepper():
    dir_pin = 26
    step_pin = 20
    switch_pin = 17
    speed = 20
    steps = 200 * 32
    run_distance =1
    m1 = stepper.Stepper(dir_pin, step_pin, switch_pin, speed, steps)
    for i in range(10):
        m1.run(run_distance)
        time.sleep(6)

    GPIO.cleanup()

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    file_name = "/home/pi/lego-clock/time.txt"
    test_stepper()

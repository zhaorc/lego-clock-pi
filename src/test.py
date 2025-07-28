from RPi import GPIO
from driver import stepper
import time

def test_stepper():
    rate = 14.6
    dir_pin = 0
    step_pin = 1
    speed = 20
    steps = 200 * 32
    run_steps =int(rate * 200 * 32 / 10)
    m1 = stepper.Stepper(dir_pin, step_pin, speed, steps)
    for i in range(10):
        for j in range(10):
            m1.run(run_steps)
            time.sleep(6)

    GPIO.cleanup()

if __name__ == "__main__":
    test_stepper()

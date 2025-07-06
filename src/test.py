from RPi import GPIO
from driver import stepper

def test_stepper():
    dir_pin = 2
    step_pin = 3
    speed = 60
    steps = 200 * 32
    m1 = stepper.Stepper(dir_pin, step_pin, speed, steps)
    m1.run(speed, steps)

    GPIO.cleanup()

if __name__ == "__main__":
    test_stepper()

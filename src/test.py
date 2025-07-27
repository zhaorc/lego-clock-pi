from RPi import GPIO
from driver import stepper

def test_stepper():
    dir_pin = 0
    step_pin = 1
    relay_pin = 20
    speed = 20
    steps = 200 * 32
    run_steps = 1 * 200 * 32
    m1 = stepper.Stepper(dir_pin, step_pin, speed, steps, relay_pin)
    m1.run(run_steps)

    GPIO.cleanup()

if __name__ == "__main__":
    test_stepper()

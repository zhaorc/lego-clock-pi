import logging
import time
from driver import stepper

logger = logging.getLogger(__name__)
file_name = "/home/pi/lego-clock/time.txt"

m_speed = 30
m_steps = 21 * 20 * 80 * 200 * 32
motors = []

def read_time_str():
    with open(file_name, "r") as f:
        time_str = f.read()
        logger.info("read_time_str={}".format(time_str))
        return time_str

def save_time_str(hhmm):
    with open(file_name,"w") as f:
        f.write(hhmm)
        logger.info("save_time_str={}".format(hhmm))

def init_stepper():
    dir_pin = 2
    step_pin = 3
    relay_pin = [19, 16, 26, 20]
    motors = [
        stepper.Stepper(dir_pin, step_pin, m_speed, m_steps, relay_pin[0]),
        stepper.Stepper(dir_pin, step_pin, m_speed, m_steps, relay_pin[1]),
        stepper.Stepper(dir_pin, step_pin, m_speed, m_steps, relay_pin[2]),
        stepper.Stepper(dir_pin, step_pin, m_speed, m_steps, relay_pin[3]),
    ]

def calculate_steps(now_time, saved_time):
    now_time_value = int(now_time)
    saved_time_value = int(saved_time)
    if now_time_value == saved_time_value:
        return None
    distance = now_time_value - saved_time_value
    if distance < 0:
        distance += 10
    return m_steps / 10 * distance

def show_time():
    for motor_num in (3, 2, 1, 0):
        logger.info("motor_num={}".format(motor_num))
        saved_time_str = read_time_str()
        now_time = time.strftime("%H%M")[motor_num]
        saved_time = saved_time_str[motor_num]
        run_steps = calculate_steps(now_time, saved_time)
        if run_steps is not None:
            motors[motor_num].run(run_steps)
            hhmm = list(saved_time_str)
            hhmm[motor_num] = now_time
            save_time_str("".join(hhmm))

def main():
    logging.basicConfig(filename="/home/pi/lego-clock/log.txt", level=logging.DEBUG)
    init_stepper()
    while (True):
        show_time()
        time.sleep(1)

if __name__ == "__main__":
    main()
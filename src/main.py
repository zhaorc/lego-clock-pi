import logging
import time
from driver import stepper

logger = logging.getLogger(__name__)
file_name = "/home/pi/lego-clock/time.txt"

m_speed = 30
m_steps =  int((80 / 21) * (80 / 20) * 200 * 32)

def read_time_str():
    with open(file_name, "r") as f:
        time_str = f.read()
        return time_str

def save_time_str(hhmm):
    with open(file_name,"w") as f:
        f.write(hhmm)
        ## XXX
        logger.info("save_time_str={}".format(hhmm))

def init_stepper():
    dir_pin = 2
    step_pin = 3
    relay_pin = [19, 16, 26, 20]
    m_list = [
        stepper.Stepper(dir_pin, step_pin, m_speed, m_steps, relay_pin[0]),
        stepper.Stepper(dir_pin, step_pin, m_speed, m_steps, relay_pin[1]),
        stepper.Stepper(dir_pin, step_pin, m_speed, m_steps, relay_pin[2]),
        stepper.Stepper(dir_pin, step_pin, m_speed, m_steps, relay_pin[3]),
    ]

    return m_list

def calculate_steps(now_time, saved_time):
    now_time_value = int(now_time)
    saved_time_value = int(saved_time)
    if now_time_value == saved_time_value:
        return None
    distance = now_time_value - saved_time_value
    if distance < 0:
        distance += 10
    return int(m_steps / 10 * distance)

def show_time(m_list):
    for motor_num in (3, 2, 1, 0):
        saved_time_str = read_time_str()
        now_time = time.strftime("%H%M")[motor_num]
        saved_time = saved_time_str[motor_num]
        run_steps = calculate_steps(now_time, saved_time)

        if run_steps is not None:
            ## XXX
            logger.info("motor_num={}, saved_time_str={}, now_time={}, run_steps={}".format(motor_num, saved_time_str, now_time, run_steps))
            m_list[motor_num].run(run_steps)
            hhmm = list(saved_time_str)
            hhmm[motor_num] = now_time
            save_time_str("".join(hhmm))

def main():
    logging.basicConfig(level=logging.DEBUG)
    m_list = init_stepper()
    while (True):
        show_time(m_list)
        time.sleep(1)

if __name__ == "__main__":
    main()
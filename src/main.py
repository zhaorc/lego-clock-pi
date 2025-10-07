import time

from RPi import GPIO

from driver import stepper

file_name = "/home/pi/lego-clock/time.txt"

m_speed = [5, 5, 5, 20]
m_steps =  200 * 128
dir_pin = [0, 6, 19, 26]
step_pin = [1, 12, 16, 20]
switch_pin = [2, 3, 4, 17]
direction = [1, 1, 1, 1]

def read_time_str():
    with open(file_name, "r") as f:
        time_str = f.read()
        f.close()
        return time_str

def save_time_str(hhmm):
    with open(file_name,"w") as f:
        f.write(hhmm)
        f.close()
       
def init_stepper():
    m_list = [
        stepper.Stepper(dir_pin[0], step_pin[0], switch_pin[0], m_speed[0], m_steps),
        stepper.Stepper(dir_pin[1], step_pin[1], switch_pin[1], m_speed[1], m_steps),
        stepper.Stepper(dir_pin[2], step_pin[2], switch_pin[2], m_speed[2], m_steps),
        stepper.Stepper(dir_pin[3], step_pin[3], switch_pin[3], m_speed[3], m_steps),
    ]
    return m_list

def calculate_distance(motor_num, now_time, saved_time):
    now_time_value = int(now_time)
    saved_time_value = int(saved_time)
    if now_time_value == saved_time_value:
        return None
    distance = now_time_value - saved_time_value
    if distance < 0:
        distance += 10
    print("motor_num={}, now_time={}, saved_time={}, distance={}".format(motor_num, now_time, saved_time, distance))
    return direction[motor_num] * distance

def show_time(m_list, saved_time):
    for motor_num in (3, 2, 1, 0):
        now_time = time.strftime("%H%M")[motor_num]
        motor_time = saved_time[0][motor_num]
        if now_time == motor_time:
            continue
        distance = calculate_distance(motor_num, now_time, motor_time)
        if distance is not None:
            m_list[motor_num].run(distance)
            hhmm = list(saved_time[0])
            hhmm[motor_num] = now_time
            save_time_str("".join(hhmm))
            saved_time[0] = hhmm

def main():
    m_list = init_stepper()
    saved_time_str = read_time_str()
    saved_time =[saved_time_str]
    while True:
        show_time(m_list, saved_time)
        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    finally:
       GPIO.cleanup()
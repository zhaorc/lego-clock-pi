import logging
import time
from RPi import GPIO

class Stepper:
    """
    * 电流
    * 2.0A OFF OFF OFF OFF
    * 1.7A OFF OFF OFF ON
    * 1.5A OFF OFF ON  OFF
    * 1.3A OFF OFF ON  ON
    * 1.0A OFF ON  ON  ON
    * 0.7A ON  ON  ON  ON

    * 细分
    *     1 ON  ON  ON
    *     2 ON  ON  OFF
    *     4 ON  OFF ON
    *     8 ON  OFF OFF
    *   16 OFF ON  ON
    *   32 OFF ON  OFF
    *   64 OFF OFF ON
    * 128 OFF OFF OFF

    * A-B相
    * 红 A+
    * 蓝 A-
    * 绿 B+
    * 黑 B-

    https://www.embedded.com/generate-stepper-motor-speed-profiles-in-real-time/
    """
    __dir_pin = None
    __step_pin = None
    __switch_pin = None
    __steps = None
    __sleep_time = None  # milli_second
    __distance = 0
    __max_run_time = None #

    def __count_distance(self, channel):
        value1 = GPIO.input(channel)
        time.sleep(0.001)
        value2 = GPIO.input(channel)
        #print("value1={}, value2={}".format(value1, value2))
        if not value1 and not value2:
            self.__distance += 1

    def __init__(self, dir_pin, step_pin, switch_pin, speed, steps):
        """
        :param dir_pin:
        :param step_pin:
        :param speed: 转速 RPM
        :param steps: 步进电机一圈的步数
        """
        self.__dir_pin = dir_pin
        self.__step_pin = step_pin
        self.__switch_pin = switch_pin
        self.__steps = steps

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dir_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(step_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(switch_pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)
        #GPIO.add_event_detect(self.__switch_pin, GPIO.FALLING, callback=self.__count_distance, bouncetime=300)
        self.__sleep_time = 30000000 / speed / steps
        self.__max_run_time = 2 * self.__sleep_time * steps * 2 / 1000000

    def run(self, distance):
        """
        转steps步
        :param steps: steps>0正转, steps<0反转
        :return:
        """
        self.__distance = 0
        run_distance = distance
        if distance > 0:
            GPIO.output(self.__dir_pin, GPIO.HIGH)
        else:
            GPIO.output(self.__dir_pin, GPIO.LOW)
            run_distance = -distance
        GPIO.add_event_detect(self.__switch_pin, GPIO.FALLING, callback=self.__count_distance, bouncetime=300)
        start_time = time.time()
        while True:
            GPIO.output(self.__step_pin, GPIO.HIGH)
            self.__delay_microseconds(self.__sleep_time)
            GPIO.output(self.__step_pin, GPIO.LOW)
            self.__delay_microseconds(self.__sleep_time)
            if self.__distance >= run_distance or time.time() - start_time > self.__max_run_time:
                break

        GPIO.output(self.__step_pin, GPIO.LOW)
        GPIO.output(self.__dir_pin, GPIO.LOW)
        GPIO.remove_event_detect(self.__switch_pin)

    @staticmethod
    def __delay_microseconds(sleep_time):
        """
        sleep 微秒
        :param sleep_time: sleep的时间，微秒
        :return:
        """
        t = (sleep_time - 3) / 1000000  # -3微秒是修正值,测试发现树莓派多消耗了3微秒
        start, end = 0, 0
        start = time.time()
        while end - start < t:
            end = time.time()

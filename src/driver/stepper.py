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
    __steps = None
    __relay_pin = None
    __sleep_time = None  # milli_second

    def __init__(self, dir_pin, step_pin, speed, steps, relay_pin):
        """
        :param dir_pin:
        :param step_pin:
        :param speed: 转速 RPM
        :param steps: 步进电机一圈的步数
        """
        self.__dir_pin = dir_pin
        self.__step_pin = step_pin
        self.__steps = steps
        self.__relay_pin = relay_pin
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dir_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(step_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(relay_pin, GPIO.OUT, initial=GPIO.LOW)

        self.__sleep_time = 30000000 / speed / steps

    def run(self, steps):
        """
        转steps步
        :param steps: steps>0正转, steps<0反转
        :return:
        """
        run_steps = steps
        if steps > 0:
            GPIO.output(self.__dir_pin, GPIO.HIGH)
        else:
            GPIO.output(self.__dir_pin, GPIO.LOW)
            run_steps = -steps

        GPIO.output(self.__relay_pin, GPIO.HIGH)

        for i in range(run_steps):
            GPIO.output(self.__step_pin, GPIO.HIGH)
            self.__delay_microseconds(self.__sleep_time)
            GPIO.output(self.__step_pin, GPIO.LOW)
            self.__delay_microseconds(self.__sleep_time)

        GPIO.output(self.__relay_pin, GPIO.LOW)

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
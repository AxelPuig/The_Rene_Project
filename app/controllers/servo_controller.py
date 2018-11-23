import RPi.GPIO as GPIO
import time

def setup_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def clear():
    GPIO.cleanup()


class ServoController():

    def __init__(self, pin_number):
        """setup the GPIO_pin select as an output with a servo"""
        GPIO.setup(pin_number, GPIO.OUT)

        self.ratio = 0.
        self.pwm = GPIO.PWM(pin_number, 100)  # 100 is the frequency of the PWM signal
        self.pwm.start(10)  # 10 is 0 for a servo
        self.set_ratio(0.5)

    def set_ratio(self, ratio):
        """put the selected servo at the angle specified"""
        self.ratio = ratio
        duty_cycle = 10 + ratio * 10  # construction of a standard servo signal
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)
        self.rest()

    def get_ratio(self):
        return self.ratio

    def add_ratio(self, ratio):
        new_ratio = self.ratio + ratio
        if 1 >= new_ratio >= 0:
            self.set_ratio(new_ratio)

    def rest(self):
        self.pwm.ChangeDutyCycle(0)

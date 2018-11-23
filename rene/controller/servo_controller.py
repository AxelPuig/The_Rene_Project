import RPi.GPIO as GPIO
import time


def setup_GPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


def clear():
    GPIO.cleanup()


class ServoController():
    """
    Low level servo control class.
    Main method are set_ratio to move the camera to a specific position, and add_ratio for a relative move
    """

    def __init__(self, pin_number):
        """Setup the GPIO_pin select as an output with a servo"""
        GPIO.setup(pin_number, GPIO.OUT)

        self.ratio = 0.
        self.pwm = GPIO.PWM(pin_number, 100)  # 100 is the frequency of the PWM signal
        self.pwm.start(10)  # 10 is 0 for a servo
        self.set_ratio(0.5)

    def set_ratio(self, ratio):
        """
        Put the selected servo at the ratio specified
        :param ratio: 0 to go full left, 1 to go full right
        """
        self.ratio = ratio
        duty_cycle = 10 + ratio * 10  # Construction of a standard servo signal
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.25)
        self.rest()

    def get_ratio(self):
        return self.ratio

    def add_ratio(self, ratio):
        """ Relative move """
        new_ratio = self.ratio + ratio
        if 1 >= new_ratio >= 0:
            self.set_ratio(new_ratio)

    def rest(self):
        """ Stops forcing the servo to be at the right position. Can remove trembling issues """
        self.pwm.ChangeDutyCycle(0)

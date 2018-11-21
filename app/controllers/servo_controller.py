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

        self.pwm = GPIO.PWM(pin_number, 100)  # 100 is the frequency of the PWM signal
        self.pwm.start(10)  # 10% is 0 for a servo

    def set_percent(self, percent):
        """put the selected servo at the angle specified"""
        duty_cycle = 10 + percent * 10  # construction of a standard servo signal
        self.pwm.ChangeDutyCycle(duty_cycle)

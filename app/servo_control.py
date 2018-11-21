import RPi.GPIO as GPIO
import time


def init_servo(pin_number):
    """setup the GPIO_pin select as an output with a servo"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number, GPIO.OUT)
    GPIO.setwarnings(False)

    pwm=GPIO.PWM(pin_number, 100)  # 100 is the frequency of the PWM signal
    pwm.start(10)  # 10% is 0 for a servo

    return pwm


def set_angle(servo, percentage):
    """put the selected servo at the angle specified in percentage of the max angle"""
    duty_cycle = 10 + percentage/90 * 10  # construction of a standard servo signal
    servo.ChangeDutyCycle(duty_cycle)


def clean_pwm():
    """just to clear all the PWM"""
    GPIO.cleanup()


def test(pin_number):
    """test a servo plugged onto the select pin by making a moove"""
    servo1 = init_servo(pin_number)
    time.sleep(1)
    set_angle(servo1, 90)
    time.sleep(3)
    set_angle(servo1, 0)
    time.sleep(1)
    clean_pwm()


test(2)

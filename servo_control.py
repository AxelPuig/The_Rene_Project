import RPi.GPIO as GPIO
import time


def init_servo(pin_number):
    """setup the GPIO_pin select as an output with a servo"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_number, GPIO.OUT)
    GPIO.setwarnings(False)

    pwm=GPIO.PWM(pin_number, 100)  # 100 is the frequency of the PWM signal
    pwm.start(0)

    return pwm


def set_angle(servo, angle):
    """put the selected servo at the angle specified"""
    duty_cycle = 10 + angle/360 * 10  # construction of a standard servo signal
    servo.ChangeDutyCycle(duty_cycle)


def clean_pwm():
    """just to clear all the PWM"""
    GPIO.cleanup()


def test(pin_number):
    servo1 = init_servo(pin_number)
    time.sleep(1)
    set_angle(servo1, 100)
    time.sleep(3)
    set_angle(servo1, 0)
    time.sleep(1)
    clean_pwm()


test(2)

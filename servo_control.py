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


servo1 = init_servo(2)
time.sleep(1)
set_angle(servo1, 100)
time.sleep(3)
set_angle(servo1, 0)
clean_pwm()

a="""ajoutAngle = 5

print("Comment controler le Servo ?")
choix = int(input("1. Choisir un angle\n2. Faire tourner de 0 a 180\n"))

if choix == 2 :

    nbrTour = input ("Entrez le nombre d'aller-retour que fera le Servo :\n")

    pwm=GPIO.PWM(2,100)
    pwm.start(5)

    angle1 = 0
    duty1 = float(angle1)/10 + ajoutAngle

    angle2=180
    duty2= float(angle2)/10 + ajoutAngle

    i = 0

    while i <= nbrTour:
         pwm.ChangeDutyCycle(duty1)
         time.sleep(0.8)
         pwm.ChangeDutyCycle(duty2)
         time.sleep(0.8)
         i = i+1
    GPIO.cleanup()

if choix == 1 :
    angle = input("Entrez l'angle souhaite :\n")
    duree = input("Entrez la duree durant laquelle le Servo devra tenir sa position : ( en secondes )\n")

    pwm=GPIO.PWM(2,100)
    pwm.start(5)

    angleChoisi = float(angle)/10 + ajoutAngle
    pwm.ChangeDutyCycle(angleChoisi)
    time.sleep(float(duree))
    pwm.ChangeDutyCycle(0)
    GPIO.cleanup()"""

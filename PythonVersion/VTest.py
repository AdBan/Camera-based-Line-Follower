import RPi.GPIO as gpio
import time

def initialize_motors():
    gpio.setmode(gpio.BCM)
    gpio.setup(L_MOTOR_PIN, gpio.OUT)
    gpio.setup(R_MOTOR_PIN, gpio.OUT)
    l_motor = gpio.PWM(L_MOTOR_PIN, 50)
    r_motor = gpio.PWM(R_MOTOR_PIN, 50)
    l_motor.start(100)
    r_motor.start(100)
    return l_motor, r_motor

def drive_motor(motor, percent_speed):
    duty_cycle = percent_speed * 100
    motor.ChangeDutyCycle(duty_cycle)

####################################################################
LMotor, RMotor = initialize_motors

while 1:
    for i in range(100,1,-1):
        drive_motor(LMotor,i)
        drive_motor(RMotor,i)  
        print("Wypełnienie w procentach [%]" + str(i))
        time.sleep(1)

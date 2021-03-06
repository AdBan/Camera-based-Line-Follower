# import RPi.GPIO as gpio
# import math
# import cv2
# import io
# import numpy
# import PiCamera as picamera
#
# #Function for initializing motor pins
# def initializeMotors(lMotorPin,rMotorPin)
# 	gpio.setmode(gpio.board)
#
# 	gpio.setup(lMotorPin, gpio.out)
# 	gpio.setup(rMotorPin, gpio.out)
#
# 	lMotor = gpio.PWM(12 ,50)
# 	rMotor = gpio.PWM(19, 50)
#
#
# .start(100)
# 	rMotor.start(100)
# 	return (lMotor, rMotor)
#
# #Function for driving motors
# def driveMotors (motor, percentSpeed)
# 	dutyCycle = percentSpeed*100
# 	motor.ChangeDutyCycle(dutyCycle)
# 	return
#
# #Function for getting center of the line point
# def getLinePoint(frame, height)
# 	y = math.floor((1 - height) *
#
# #Initialize camera
# cameraWidth = 800
# cameraHeight = 600
# cameraFrame = 90
#
# cam = PiCamera()
# cam.resolution(cameraWidth,cameraHeight)
# cam.framerate(cameraFrame)
#
# #Initialize motor pins and pid parameters
# lMotorPin = 19
# rMotorPin = 12
#
# lMotor, rMotor = initializeMotors(lMotorPin,rMotorPin)
#
# Kp = 15
# Kd = 5
#
# #Initialize camera
#
# while (!stopCriteria)
#

##############################################


import RPi.GPIO as gpio
from picamera import PiCamera
from picamera.array import PiRGBArray
import math
import time
import numpy
import cv2

L_MOTOR_PIN = 19
R_MOTOR_PIN = 12

CAMERA_WIDTH = 800
CAMERA_HEIGHT = 600
CAMERA_FRAME_RATE = 90

KP = 15
KD = 5


def initialize_motors():
    gpio.setmode(gpio.board)
    gpio.setup(L_MOTOR_PIN, gpio.out)
    gpio.setup(R_MOTOR_PIN, gpio.out)
    l_motor = gpio.PWM(L_MOTOR_PIN, 50)
    r_motor = gpio.PWM(R_MOTOR_PIN, 50)
    l_motor.start(100)
    r_motor.start(100)


def drive_motor(motor, percent_speed):
    duty_cycle = percent_speed * 100
    motor.ChangeDutyCycle(duty_cycle)


##########################################

camera = PiCamera()
raw_capture = PiRGBArray(camera)
time_sleep(1)

for frame in camera.capture_continous(raw_capture, format="bgr", use_video_port=true):
    img = frame.array
    cv2.show('Raw image', img)
    raw_capture.truncate(0)

camera.close()
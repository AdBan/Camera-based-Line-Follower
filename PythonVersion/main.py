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
import numpy as np
import cv2
from scipy import ndimage

L_MOTOR_PIN = 19
R_MOTOR_PIN = 12

CAMERA_FRAME_RATE = 90
CAMERA_RESOLUTION = (640, 480)

KP = 15
KD = 5


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


def get_line_center(bin):
    row = ~(bin[CAMERA_RESOLUTION[1]/2, :])
    return ndimage.measurements.center_of_mass(row)





##########################################

camera = PiCamera()
camera.resolution = CAMERA_RESOLUTION
camera.framerate = CAMERA_FRAME_RATE
raw_capture = PiRGBArray(camera)
time.sleep(1)
l_motor, r_motor = initialize_motors()

while True:
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        rgb = frame.array
        raw_capture.truncate(0)
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        bin = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
        cv2.imshow('img', bin)

        center = get_line_center(bin)
        error = center[0] - CAMERA_RESOLUTION[1]/2

        error_percent = error/(CAMERA_RESOLUTION[0]/2)

        if error < 0:
            print("Turning left\n")
            drive_motor(l_motor, 1 - error_percent)
            drive_motor(r_motor, error_percent)
        else:
            print("Turning right\n")
            drive_motor(l_motor, error_percent)
            drive_motor(r_motor, 1 - error_percent)

        cv2.waitKey(1)

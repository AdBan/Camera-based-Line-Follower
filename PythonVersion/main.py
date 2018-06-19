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

MOTOR_STOP = 1.5

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
    duty_cycle = percent_speed * 60
    motor.ChangeDutyCycle(duty_cycle)


def get_line_center(bin):
    # only one row
    # row = ~(bin[CAMERA_RESOLUTION[1]/2, :])
    # if sum(row) == 0:
    #     return -1
    # else:
    #     return ndimage.measurements.center_of_mass(row)[0]

    # whole image
    if sum(sum(~bin)) == 0:
        return -1
    else:
        return ndimage.measurements.center_of_mass(~bin)[1]





##########################################

camera = PiCamera()
camera.resolution = CAMERA_RESOLUTION
camera.framerate = CAMERA_FRAME_RATE
raw_capture = PiRGBArray(camera)
time.sleep(1)
l_motor, r_motor = initialize_motors()


lookingRight = 1000
lookingLeft = 2000
nLooks = 2

camera.start_recording("video.h264")
time.sleep(1)
while True:
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        rgb = frame.array
        raw_capture.truncate(0)
        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        bin = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
        # cv2.imshow('img', bin)
        # cv2.waitKey(1)

        center = get_line_center(bin)
        if center < 0:
            if lookingRight > 0:
                drive_motor(r_motor, MOTOR_STOP)
                drive_motor(l_motor, 0)
                lookingRight = lookingRight - 1
                print("Turning right. " + str(lookingRight) + " to go")
                camera.stop_recording()
            elif lookingLeft > 0:
                drive_motor(r_motor, 0)
                drive_motor(l_motor, MOTOR_STOP)
                lookingLeft = lookingLeft - 1
                print("Turning left. " + str(lookingLeft) + " to go")
            elif lookingRight == 0 and lookingLeft == 0:
                nLooks = nLooks + 1
                lookingRight = nLooks*1000
                lookingLeft = 10000 + nLooks*1000
                print("Reset and go again")
        
            continue
            

        error = center - CAMERA_RESOLUTION[0]/2
        error_percent = abs(error/(CAMERA_RESOLUTION[0]/2))/2 

        #print("center: " + str(center) + "\nerror: " + str(error) + "\nerror_percent: " + str(error_percent))

        if error > 0:
            #print("Turning right\n")
            drive_motor(l_motor, 0.5 - error_percent)
            drive_motor(r_motor, 0.5 + error_percent)
        else:
            #print("Turning left\n")
            drive_motor(l_motor, 0.5 + error_percent)
            drive_motor(r_motor, 0.5 - error_percent)



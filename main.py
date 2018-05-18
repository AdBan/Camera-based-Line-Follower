import RPi.GPIO as gpio
import math
import cv2
import io
import numpy
import PiCamera as picamera

#Function for initializing motor pins
def initializeMotors(lMotorPin,rMotorPin)
	gpio.setmode(gpio.board)
	
	gpio.setup(lMotorPin, gpio.out)
	gpio.setup(rMotorPin, gpio.out)
	
	lMotor = gpio.PWM(12 ,50)
	rMotor = gpio.PWM(19, 50)
	
	lMotor.start(100)
	rMotor.start(100)
	return (lMotor, rMotor)
	
#Function for driving motors
def driveMotors (motor, percentSpeed)
	dutyCycle = percentSpeed*100
	motor.ChangeDutyCycle(dutyCycle)
	return

#Function for getting center of the line point
def getLinePoint(frame, height)
	y = math.floor((1 - height) * 

#Initialize camera
cameraWidth = 800
cameraHeight = 600
cameraFrame = 90

cam = PiCamera()
cam.resolution(cameraWidth,cameraHeight)
cam.framerate(cameraFrame)

#Initialize motor pins and pid parameters
lMotorPin = 19
rMotorPin = 12

lMotor, rMotor = initializeMotors(lMotorPin,rMotorPin)

Kp = 15
Kd = 5

#Initialize camera

while (!stopCriteria)
	


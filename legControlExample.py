"""
ECE 4600 - Group Design Project
G08 - ServoSentry
Author - Noah Stieler, 2025

This is currently my working file for testing features.
"""

from motor import LegMotor
from constants import *
from inverseKinematics import *

from adafruit_servokit import ServoKit

from time import time, sleep

#TODO initalize to standing pose, to set current angle for all motors.

servo_driver = ServoKit(channel=PCA9685_CHANNEL_COUNT)

motor0 = LegMotor(servo_driver, channel=0, flipped = False)
motor0.setAngle(0, lerp=False)
sleep(1)

#Testing inverse kinematics
stepSize = 5
x = [-30 + ((10 - (-30))/stepSize) * i for i in range(0, stepSize + 1)]
y = -120

for i in x:
    lowerMotorAngle, upperMotorAngle = inverseKinematics(i, y)
    print("lower= " + str(lowerMotorAngle) + " upper= " + str(upperMotorAngle - 180))

def main():
    curTime = time*1000
    sign = 1
    while True:
        motor0.update()

        if (time()*1000 > curTime + MOTOR_SPEED):
            sign = sign*-1
            if(sign == 1):
                motor0.seetAngle(90)
            else:
                motor0.setAngle(-90)
            curTime = time()*1000

main()


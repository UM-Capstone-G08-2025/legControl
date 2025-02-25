"""
ECE 4600 - Group Design Project
G08 - ServoSentry
Author - Noah Stieler, 2025

This is currently my working file for testing features.
"""

from motor import LegMotor
from constants import *
from inverseKinematics import *
from leg import Leg

from adafruit_servokit import ServoKit

from time import time, sleep

#TODO initalize to standing pose, to set current angle for all motors.

servoDriver = ServoKit(channels=PCA9685_CHANNEL_COUNT)

legBackRight = Leg(servoDriver, lowerMotorChannel=12, upperMotorChannel=13,
    rotationMotorChannel=14, isMirrored=False)

legFrontRight = Leg(servoDriver, lowerMotorChannel=8, upperMotorChannel=9,
    rotationMotorChannel=10, isMirrored=False)

legBackLeft = Leg(servoDriver, lowerMotorChannel=0, upperMotorChannel=1,
    rotationMotorChannel=2, isMirrored=True)

legFrontLeft = Leg(servoDriver, lowerMotorChannel=4, upperMotorChannel=5,
    rotationMotorChannel=6, isMirrored=True)
    
legBackRight.setPos(30, -140)
legFrontRight.setPos(30, -140)
legBackLeft.setPos(30, -140)
legFrontLeft.setPos(30, -140)

sleep(3)

#Testing inverse kinematics
"""stepSize = 5
x = [-30 + ((10 - (-30))/stepSize) * i for i in range(0, stepSize + 1)]
y = -120

for i in x:
    lowerMotorAngle, upperMotorAngle = inverseKinematics(i, y)
    print("lower= " + str(lowerMotorAngle) + " upper= " + str(upperMotorAngle - 180))
    
lowerMotorAngle, upperMotorAngle = inverseKinematics(20, -120)
print(str(lowerMotorAngle) + " " + str(upperMotorAngle))"""

def main():
    frame = 0
    
    while True:
        legBackLeft.setRotationMotorAngle(15)
        legBackRight.setRotationMotorAngle(-7.5)
        legFrontLeft.setRotationMotorAngle(20)
        legFrontRight.setRotationMotorAngle(20)
        
        legFrontRight.update()
        legBackLeft.update()
        legFrontLeft.update()
        legBackRight.update()
        
        if (not legBackRight.isAnimating() and not legFrontRight.isAnimating()
            and not legBackLeft.isAnimating() and not legFrontLeft.isAnimating()):
                
            if frame == 0:
                legBackRight._animPlay("animPullBack")
                legFrontRight._animPlay("animPullBack")
                legBackLeft._animPlay("animPullBack")
                legFrontLeft._animPlay("animPullBack")
            elif frame == 1:
                legFrontRight._animPlay("animLiftMoveForward")
            elif frame == 2:
                legFrontLeft._animPlay("animLiftMoveForward")
            elif frame == 3:
                legBackRight._animPlay("animLiftMoveForward")
            elif frame == 4:
                legBackLeft._animPlay("animLiftMoveForward")
                
            frame += 1
            if frame > 5:
                frame = 0
    
    """while True:
        motorLower.setAngle(lowerMotorAngle + 10, lerp=False)
        motorUpper.setAngle(upperMotorAngle + 10, lerp=False)
    curTime = time()*1000"""
    
    
    """sign = 1
    curTime = time()*1000
    while True:
        if (time()*1000 > curTime + MOTOR_SPEED):
            if sign == 1:
                lowerMotorAngle, upperMotorAngle = inverseKinematics(sign*40, -140)
            else:
                lowerMotorAngle, upperMotorAngle = inverseKinematics(sign*30, -140 - 30)
            print(str(lowerMotorAngle) + " " + str(upperMotorAngle))
            sign = sign*-1
            motorLower.setAngle(lowerMotorAngle, lerp=False)
            motorUpper.setAngle(upperMotorAngle, lerp=False)
            curTime = time()*1000"""
            
main()


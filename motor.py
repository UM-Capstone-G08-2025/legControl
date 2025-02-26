"""
ECE 4600 - Group Design Project
G08 - ServoSentry
Author - Noah Stieler, 2025

Provides classes that represent both types of leg motor.
"""

from .constants import *

class Motor:
    """
    Base class for all motor objects. Not meant to be instantiated.
    """
    def __init__(self, servoDriver, channel:int,
        motorMinDuration:int, motorMaxDuration:int,
        motorMinAngle:int, motorMaxAngle:int):

        self.servoDriver = servoDriver
        self.channel = channel
        
        self.motorMinAngle = motorMinAngle
        self.motorMaxAngle = motorMaxAngle

        try:#OSError is thrown when driver is disconnected
            servoDriver.servo[channel].set_pulse_width_range(motorMinDuration, motorMaxDuration)
            servoDriver.servo[channel].actuation_range = motorMaxAngle - motorMinAngle
        except:
            pass

    def _setAngle(self, angle:int) -> None:
        """
        Set the motor's angle as fast as possible. This results in jerky movement, 
        so interpolation should happend between positions to produce smoother results.

        The servo library maps motor angle on a range 0 to 180 degrees by default.
        By convention, this program will have the motor's middle position at 0 degrees instead,
        so we need to map from the range [-90, 90] to [0, 180]. This was done to reflect
        a more typical way of measuring angles.
        """
        if (angle < self.motorMinAngle or angle > self.motorMaxAngle):
            print("ERROR: motor on channel " + str(self.channel) + " tried moving out of bounds.")
            print("angle = " + str(angle))
            quit()
        try:#OSError is thrown when driver is disconnected
            self.servoDriver.servo[self.channel].angle = self.motorMaxAngle + angle
        except:
            pass

class LegMotor(Motor):
    """
    Represents the motor used to move the leg joints.
    """
    def __init__(self, servoDriver, channel:int, flipped:bool=False):
        Motor.__init__(self, servoDriver, channel,
            motorMinDuration=LEG_MOTOR_MIN_DUR,
            motorMaxDuration=LEG_MOTOR_MAX_DUR,
            motorMinAngle=LEG_MOTOR_MIN_ANGLE,
            motorMaxAngle=LEG_MOTOR_MAX_ANGLE)
        
        self.flipped = flipped
    
    def setAngle(self, angle:int) -> None:
        """
        Each leg has two motors, that when looked at from the front, will have one motor
        pointing in the positive x direction, and another motor pointing in the negative x direction.
        The motor in the negative x direction will vary from 90 to 270 degrees, so we have to accound
        for this with the flipped parameter.
        """
        if not self.flipped:
            Motor._setAngle(self, angle)
        if self.flipped:
            Motor._setAngle(self, -(180 - angle))
                
class RotationMotor(Motor):
    """
    Represents the motor used to move the entire leg.
    """
    def __init__(self, servoDriver, channel:int):
        Motor.__init__(self, servoDriver, channel,
            motorMinDuration=ROT_MOTOR_MIN_DUR,
            motorMaxDuration=ROT_MOTOR_MAX_DUR,
            motorMinAngle=ROT_MOTOR_MIN_ANGLE,
            motorMaxAngle=ROT_MOTOR_MAX_ANGLE)
            
    def setAngle(self, angle:int) -> None:
        Motor._setAngle(self, angle)

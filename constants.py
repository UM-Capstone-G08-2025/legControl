"""
ECE 4600 - Group Design Project
G08 - ServoSentry
Author - Noah Stieler, 2025

Provides all the constants which are determined by choice
of hardware and leg design.
"""

"""SOFTWARE LEVEL"""
#Time for motor to transition between keyframes, in milliseconds
MOTOR_SPEED = 1000
#Number of subframes used to interpolate between keyframes. More frames -> smoother movement.
MOTOR_SUB_FRAME_COUNT = 16

"""SERVO DRIVER"""
#The following constants are set by the hardware used
PCA9685_CHANNEL_COUNT = 16

"""MOTORS"""
LEG_MOTOR_MIN_DUR   = 500   #Minimum pulse duration, in microseconds
LEG_MOTOR_MAX_DUR   = 2500  #Maximum pulse duration, in microseconds
LEG_MOTOR_MIN_ANGLE = -90   #Minimum rotation angle, in degrees
LEG_MOTOR_MAX_ANGLE = 90    #Maximum rotation angle, in degrees

ROT_MOTOR_MIN_DUR   = 1000  #Minimum pulse duration, in microseconds
ROT_MOTOR_MAX_DUR   = 2000  #Maximum pulse duration, in microseconds
ROT_MOTOR_MIN_ANGLE = -60   #Minimum rotation angle, in degrees
ROT_MOTOR_MAX_ANGLE = 60    #Maximum rotation angle, in degrees

"""LEG GEOMETRY"""
#All units are in millimeters
LOWER_LEG_BONE_LENGTH = 120
LOWER_LEG_BONE_ATTACH_DIST = 39
LOWER_LEG_TENDON_LENGTH = 120

UPPER_LEG_BONE_LENGTH = 120
UPPER_LEG_BONE_ATTACH_DIST = 42
UPPER_LEG_TENDON_LENGTH = 33

MOTOR_CONNECTOR_LENGTH = 39
UPPER_MOTOR_POS = [-20, 20]
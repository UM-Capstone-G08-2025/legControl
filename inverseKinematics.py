"""
ECE 4600 - Group Design Project
G08 - ServoSentry
Author - Noah Stieler, 2025

Handles the inverse kinematic model of the leg.
"""
from constants import *

import math

def _circleIntersection(x1:float, y1:float, r1:float, x2:float, y2:float, r2:float):
    """
    Takes the position and radius of 2 circles, and returns a list of their intersection points.

    Formula is based on the following Stack Exchange post:
    https://math.stackexchange.com/questions/256100/how-can-i-find-the-points-at-which-two-circles-intersect
    """
    result = [[], []]
    
    R = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    term0 = 0.5
    term1 = 0.5*(r1**2 - r2**2)/R**2
    term2 = 0.5*math.sqrt(2*(r1**2 + r2**2)/(R**2) - ((r1**2 - r2**2)**2)/(R**4) - 1)

    sign = 1
    result[0] = [
        term0*(x1+x2) + term1*(x2-x1) + sign*term2*(y2-y1),
        term0*(y1+y2) + term1*(y2-y1) + sign*term2*(x1-x2)
    ]
    sign = -1
    result[1] = [
        term0*(x1+x2) + term1*(x2-x1) + sign*term2*(y2-y1),
        term0*(y1+y2) + term1*(y2-y1) + sign*term2*(x1-x2)
    ]

    return result

def inverseKinematics(x, y):
    """
    Takes a desired (x, y) position of the end-effector,
    and returns the required angles for the lower and upper motors.
    """
    #Start from end-effector location (x, y)
    posSol, negSol = _circleIntersection(x, y, LOWER_LEG_BONE_LENGTH, 0, 0, UPPER_LEG_BONE_LENGTH)

    #Take solution with smallest x value
    kneeJointPos = []
    if posSol[0] < negSol[0]:
        kneeJointPos = posSol
    else:
        kneeJointPos = negSol

    #Determine lower motor angle

    #Get lower leg attachment point
    lowerLegAttachPos = [x - kneeJointPos[0], y - kneeJointPos[1]]
    mag = math.sqrt(lowerLegAttachPos[0]**2 + lowerLegAttachPos[1]**2)
    lowerLegAttachPos = [lowerLegAttachPos[0]/mag, lowerLegAttachPos[1]/mag]#Normalize
    lowerLegAttachPos = [
        lowerLegAttachPos[0]*LOWER_LEG_BONE_ATTACH_DIST + kneeJointPos[0],
        lowerLegAttachPos[1]*LOWER_LEG_BONE_ATTACH_DIST + kneeJointPos[1]]

    posSol, negSol = _circleIntersection(lowerLegAttachPos[0], lowerLegAttachPos[1], LOWER_LEG_TENDON_LENGTH,
        0, 0, MOTOR_CONNECTOR_LENGTH)

    #Take solution with largest x value
    lowerMotorEndPoint = []
    if posSol[0] > negSol[0]:
        lowerMotorEndPoint = posSol
    else:
        lowerMotorEndPoint = negSol

    lowerMotorAngle = (180/math.pi)*math.atan2(lowerMotorEndPoint[1], lowerMotorEndPoint[0])

    #Determine upper motor angle

    #Get upper leg attachment point
    upperLegAttachPos = [kneeJointPos[0] - 0, kneeJointPos[1] - 0]
    mag = math.sqrt(upperLegAttachPos[0]**2 + upperLegAttachPos[1]**2)
    upperLegAttachPos = [upperLegAttachPos[0]/mag, upperLegAttachPos[1]/mag]#Normalize
    upperLegAttachPos = [
        upperLegAttachPos[0]*UPPER_LEG_BONE_ATTACH_DIST,
        upperLegAttachPos[1]*UPPER_LEG_BONE_ATTACH_DIST]

    posSol, negSol = _circleIntersection(upperLegAttachPos[0], upperLegAttachPos[1], UPPER_LEG_TENDON_LENGTH,
        UPPER_MOTOR_POS[0], UPPER_MOTOR_POS[1], MOTOR_CONNECTOR_LENGTH)

    #Take solution with smallest x value
    upperMotorEndPoint = []
    if posSol[0] < negSol[0]:
        upperMotorEndPoint = posSol
    else:
        upperMotorEndPoint = negSol

    upperMotorAngle = (180/math.pi)*math.atan2(upperMotorEndPoint[1] - UPPER_MOTOR_POS[1], upperMotorEndPoint[0] - UPPER_MOTOR_POS[0])
    upperMotorAngle = (upperMotorAngle + 360)%360

    return [lowerMotorAngle, upperMotorAngle]
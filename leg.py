"""
ECE 4600 - Group Design Project
G08 - ServoSentry
Author - Noah Stieler, 2025
"""

from .motor import LegMotor, RotationMotor
from .inverseKinematics import *

from time import time
from math import sin

class Leg:
	def __init__(self, servoDriver, lowerMotorChannel:int, upperMotorChannel:int,
		rotationMotorChannel:int, isMirrored:bool = False):
			
		self.isMirrored = isMirrored
			
		self.servoDriver = servoDriver
		self.lowerMotor = None
		self.upperMotor = None	
		
		if not isMirrored:
			self.lowerMotor = LegMotor(servoDriver, channel=lowerMotorChannel, flipped = False)
			self.upperMotor = LegMotor(servoDriver, channel=upperMotorChannel, flipped = True)
		else:
			self.lowerMotor = LegMotor(servoDriver, channel=lowerMotorChannel, flipped = True)
			self.upperMotor = LegMotor(servoDriver, channel=upperMotorChannel, flipped = False)
			
		self.rotationMotor = RotationMotor(servoDriver, channel=rotationMotorChannel)
		
		self.animTimer = 0
		self.animLength = 0
		self.animName = ""
		self.timeStep = 0
		self.frameCount = 64
		self.curFrame = -1
		
		self.animPullBackLength = 1000
		self.animLiftMoveForwardLength = 500
	
	"""
	These functions specify the position of the end-effector as a function of time.
	
	foward
	pull back
	"""
	def _animPullBack(self, t) -> list[float, float]:
		#Determined experimentally to produce motion at constant y value
		#Total travel is 7cm
		startPos = [20, -110]
		endPos = [-40, -110-30]
		#Linearly interpolate between positions
		x = startPos[0] + (endPos[0] - startPos[0])*t
		y = startPos[1] + (endPos[1] - startPos[1])*t

		return inverseKinematics(x, y)
		
	def _animLiftMoveForward(self, t) -> list[float, float]:
		startPosX = -40
		endPosX = 20
		initialY = -110
		maxY = -70

		x = startPosX + (endPosX - startPosX)*t
		y = initialY + (maxY - initialY)*sin(t*3.14159)
		if y < -140:
			y = -140
		
		return inverseKinematics(x, y)
		
	def _animPlay(self, animName:str) -> None:
		self.animName = animName
		
		if animName == "animPullBack":
			self.animLength = self.animPullBackLength
		if animName == "animLiftMoveForward":
			self.animLength = self.animLiftMoveForwardLength
		
		self.animTimer = time()*1000
		self.timeStep = self.animLength / self.frameCount
		self.curFrame = 0
		
	def setPos(self, x, y) -> None:
		lowerMotorAngle, upperMotorAngle = inverseKinematics(x, y)
		
		if not self.isMirrored:
			self.lowerMotor.setAngle(lowerMotorAngle)
			self.upperMotor.setAngle(upperMotorAngle)
		else:
			#Extra angles added to try and correct observed error.
			self.lowerMotor.setAngle(180 + (-1*lowerMotorAngle) + 30)
			self.upperMotor.setAngle(-(upperMotorAngle - 180) + 10)
		
	def setRotationMotorAngle(self, angle:int) -> None:
		self.rotationMotor.setAngle(angle)
			
	def isAnimating(self) -> bool:
		if self.curFrame != -1:
			return True
		else:
			return False
	
	def update(self) -> None:
		if (time()*1000 > self.animTimer + self.curFrame*(self.timeStep + 1) and self.curFrame != -1):
			
			lowerMotorAngle = 0
			upperMotorAngle = 0
			
			if self.animName == "animPullBack":
				lowerMotorAngle, upperMotorAngle = self._animPullBack(self.curFrame*self.timeStep/self.animLength)
			if self.animName == "animLiftMoveForward":
				lowerMotorAngle, upperMotorAngle = self._animLiftMoveForward(self.curFrame*self.timeStep/self.animLength)
			
			if not self.isMirrored:
				self.lowerMotor.setAngle(lowerMotorAngle)
				self.upperMotor.setAngle(upperMotorAngle)
			else:
				self.lowerMotor.setAngle(180 + (-1*lowerMotorAngle) + 30)
				self.upperMotor.setAngle(-(upperMotorAngle - 180) + 10)
			
			self.curFrame += 1
			#Stop animating
			if (self.curFrame > self.frameCount):
				self.curFrame = -1
			
			
			
			
			
			
			
			
	

"""
ECE 4600 - Group Design Project
G08 - ServoSentry
Author - Noah Stieler, 2025
"""

from .constants import *
from .inverseKinematics import *
from .leg import Leg

from adafruit_servokit import ServoKit

class LegControl:
	"""
	This is the public interface for management of the quadrupedal system.
	
	The prefix animation refers to different movement configurations for the robot,
	like walking, standing, and turning. The robot can not turn on the spot,
	it can only turn by moving forwards at the same time.
	"""
	
	def __init__(self):
		self._servoDriver 	= None
		self._legBackRight 	= None
		self._legFrontRight = None
		self._legBackLeft 	= None
		self._legFrontLeft 	= None
		
		self._state = "stand"
		self._walkingPatternIndex = 0
		
		#Used for animations
		self._frame = 0
		
	def connect(self) -> None:
		"""
		Establishes a connection to the servo driver board. This
		function should be called as soon as the Raspberry Pi detects that quadrupedal
		system is selected.
		"""
		self._servoDriver = ServoKit(channels=PCA9685_CHANNEL_COUNT)

		self._legBackRight = Leg(self._servoDriver, lowerMotorChannel=12, upperMotorChannel=13,
			rotationMotorChannel=14, isMirrored=False)

		self._legFrontRight = Leg(self._servoDriver, lowerMotorChannel=8, upperMotorChannel=9,
			rotationMotorChannel=10, isMirrored=False)

		self._legBackLeft = Leg(self._servoDriver, lowerMotorChannel=0, upperMotorChannel=1,
			rotationMotorChannel=2, isMirrored=True)

		self._legFrontLeft = Leg(self._servoDriver, lowerMotorChannel=4, upperMotorChannel=5,
			rotationMotorChannel=6, isMirrored=True)
			
		self._state = "stand"
		
	def isConnected(self) -> bool:
		if self._servoDriver is not None:
			return True
		else:
			return False
		
	def disconnect(self) -> None:
		"""
		Disconnects quadrupedal system. This function should be called
		as soon as the quadrupedal system is no longer in use.
		"""
		self._servoDriver = None
	
	def animationStand(self) -> None:
		if self._servoDriver is None:
			return
			
		self._state = "stand"
		
		self._legBackRight.setPos(30, -140)
		self._legFrontRight.setPos(30, -140)
		self._legBackLeft.setPos(30, -140)
		self._legFrontLeft.setPos(30, -140)
		
	def animationWalk(self, walkingPatternIndex:int = 3) -> None:
		"""
		walkingPatternIndex is an optional parameter used for testing different walking
		animations. It takes on a default value so no arguments need to be passed to this function.
		"""
		if self._servoDriver is None:
			return
			
		self._frame = 0
		self._state = "walk"
		self._walkingPatternIndex = walkingPatternIndex
		
	def animationTurnLeft(self) -> None:
		if self._servoDriver is None:
			return
			
		self._frame = 0
		self._state = "walk"
		self._walkingPatternIndex = 2

	def animationTurnRight(self) -> None:
		if self._servoDriver is None:
			return
			
		self._frame = 0
		self._state = "walk"
		self._walkingPatternIndex = 1
	
	def animationSetAngle(self, angle:int) -> None:
		"""
		Sets the angle in degrees of all legs for the robot to turn.
		"""
		if self._servoDriver is None:
			return

		#The angle offsets are used to correct for the error with the servo motors.
		#These values were found to produce the most leg alignment when angle = 0.
		self._legBackLeft.setRotationMotorAngle(12 + angle)
		self._legBackRight.setRotationMotorAngle(-7.5 + angle)
		self._legFrontLeft.setRotationMotorAngle(12 + angle)
		self._legFrontRight.setRotationMotorAngle(12 + angle)
		
	def update(self) -> None:
		"""
		Call this function in the main control loop, it is needed to animate
		the legs and produce smooth motion.
		"""
		if self._servoDriver is None:
			return
			
		if self._state == "stand":
			self._legBackRight.setPos(30, -140)
			self._legFrontRight.setPos(30, -140)
			self._legBackLeft.setPos(30, -140)
			self._legFrontLeft.setPos(30, -140)
			
		elif (self._state == "walk" and not self._legBackRight.isAnimating()
			and not self._legFrontRight.isAnimating()
            and not self._legBackLeft.isAnimating()
            and not self._legFrontLeft.isAnimating()):
				
			if self._walkingPatternIndex == 0:
				self._walkPattern0()
			elif self._walkingPatternIndex == 1:
				self._walkPattern1()
			elif self._walkingPatternIndex == 2:
				self._walkPattern2()
			elif self._walkingPatternIndex == 3:
				self._walkPattern3()

		self._legFrontRight.update()
		self._legBackLeft.update()
		self._legFrontLeft.update()
		self._legBackRight.update()

	def _walkPattern0(self) -> None:
		"""
		Walking forwards.
		"""
		self.animationSetAngle(0)
		if self._frame == 0:
			self._legBackRight._animPlay("animPullBack")
			self._legFrontRight._animPlay("animPullBack")
			self._legBackLeft._animPlay("animPullBack")
			self._legFrontLeft._animPlay("animPullBack")
		elif self._frame == 1:
			self._legFrontRight._animPlay("animLiftMoveForward")
		elif self._frame == 2:
			self._legFrontLeft._animPlay("animLiftMoveForward")
		elif self._frame == 3:
			self._legBackRight._animPlay("animLiftMoveForward")
		elif self._frame == 4:
			self._legBackLeft._animPlay("animLiftMoveForward")
			
		self._frame += 1
		if self._frame > 5:
			self._frame = 0
			
	def _walkPattern1(self) -> None:
		"""
		This is for turning right.
		"""
		angle = 45
		self._legBackLeft.setRotationMotorAngle(12 + angle)
		self._legBackRight.setRotationMotorAngle(-7.5)
		self._legFrontLeft.setRotationMotorAngle(12 + angle)
		self._legFrontRight.setRotationMotorAngle(12)
		if self._frame == 0:
			self._legBackLeft._animPlay("animPullBack")
			self._legFrontLeft._animPlay("animPullBack")
		elif self._frame == 1:
			self._legBackLeft._animPlay("animLiftMoveForward")
		elif self._frame == 2:
			self._legFrontLeft._animPlay("animLiftMoveForward")
			
		self._frame += 1
		if self._frame > 3:
			self._frame = 0
			
	def _walkPattern2(self) -> None:
		"""
		This is for turning left.
		"""
		angle = -45
		self._legBackLeft.setRotationMotorAngle(12)
		self._legBackRight.setRotationMotorAngle(-7.5 + angle)
		self._legFrontLeft.setRotationMotorAngle(12)
		self._legFrontRight.setRotationMotorAngle(12 + angle)
		if self._frame == 0:
			self._legBackRight._animPlay("animPullBack")
			self._legFrontRight._animPlay("animPullBack")
		elif self._frame == 1:
			self._legBackRight._animPlay("animLiftMoveForward")
		elif self._frame == 2:
			self._legFrontRight._animPlay("animLiftMoveForward")
			
		self._frame += 1
		if self._frame > 3:
			self._frame = 0
			
	def _walkPattern3(self) -> None:
		"""
		Walking forwards.
		"""
		self.animationSetAngle(0)
		if self._frame == 0:
			self._legBackRight._animPlay("animPullBack")
			self._legFrontRight._animPlay("animPullBack")
			self._legBackLeft._animPlay("animPullBack")
			self._legFrontLeft._animPlay("animPullBack")
		elif self._frame == 1:
			self._legFrontRight._animPlay("animLiftMoveForward")
			self._legBackLeft._animPlay("animLiftMoveForward")
		elif self._frame == 2:
			self._legFrontLeft._animPlay("animLiftMoveForward")
			self._legBackRight._animPlay("animLiftMoveForward")
			
		self._frame += 1
		if self._frame > 3:
			self._frame = 0
		
		

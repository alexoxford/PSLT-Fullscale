import math
import RPi.GPIO as GPIO

class MotorController(object):
	
	def stopRotation(self):
		#this function will be called ~20 times per second
		#the goal of this function is to reduce the rotaion rate to as close to 0 as possible

		done = False

		diff = self.rotRate - self.burnoutRoll
		if(math.fabs(diff) > 20):
			speed = 1.0 if diff >= 0.0 else -1.0
		elif(math.fabs(diff) > 2):
			speed = diff / 20.0
		else:
			speed = 0.0
			done = True
		self.setMotorSpeed(speed) #positive is a CCW moment; negative is CW

		#if the rotation rate is 0 (or very close to it) return True, else return False
		return done

	def startRotation(self, rotation, rollRate):
		#starts the rotation and initializes the variables
		#rotation is the current rotation in degrees
		self.rotate = 1
		self.startRot = rotation
		self.burnoutRoll = rollRate
		if(rollRate > 0.0): #CW
			self.setMotorSpeed(1.0)
		else: #CCW
			self.setMotorSpeed(-1.0)
		self.distRot = 0

	def setMotorSpeed(self, speed):
		#sets the motor to the given speed
		if(speed > 1.0):
			speed = 1.0
		if(speed < -1.0):
			speed = -1.0
		self.speed = speed
		if(speed < 0.0):
			GPIO.output(21,0)
			self.p.start(speed*-100.0)
		elif(speed > 0.0):
			GPIO.output(21,1)
			self.p.start(speed*100.0)
		elif(speed == 0.0):
			GPIO.output(21,0)
			self.p.stop()

	def __init__(self):
		print("MotorController is starting")
		self.startRot = -1  #the rotation when the reaction wheel started
		self.rot = -1  #the current rotation; this will be updated from outside this class
		self.distRot = -1  #how far the rocket has rotated since the motor started
		self.rotRate = -1  #the current rotation rate; this will be updated from outside this class
		self.rotate = 0
		self.speed = 0
		self.burnoutRoll = 0.0
		
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup([21,23], GPIO.OUT)
		self.p = GPIO.PWM(23, 5120)

	def Update(self, rot, delta, rotRate):
		self.rot = rot
		self.rotRate = rotRate
		self.distRot += delta
		
		if(self.rotate == 1):
			if(math.fabs(self.distRot) >= 720.0):
				self.rotate = 2
		elif(self.rotate == 2):
			if(self.stopRotation()):
				self.setMotorSpeed(0.0)
				self.rotate = 3
		elif(self.rotate == 3):
			self.setMotorSpeed(0.0)

	def End(self):
		GPIO.cleanup()
		print("MotorController is ending")
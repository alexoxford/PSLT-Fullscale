class MotorController(object):
	
	def stopRotation(self):
		#this function will be called ~20 times per second
		#the goal of this function is to reduce the rotaion rate to as close to 0 as possible

		#calculate speed
		self.setMotorSpeed(speed)

		#if the rotation rate is 0 (or very close to it) return True, else return False

	def startRotation(self, rotation):
		#starts the rotation and initializes the variables
		#rotation is the current rotation in degrees
		self.rotate = 1
		self.setMotorSpeed(1)
		self.startRot = rotation
		self.distRot = 0
		self.rotations = 0
		self.lastTheta = 0

	def updateDistance(self):
		#this function updates distRot
		theta = (self.rot - self.startRot) if(self.rot >= self.startRot) else (self.rot + (360.0 - self.startRot))
		if(theta < self.lastTheta):  #a full rotation has occured
			self.rotations += 1
		self.distRot = (theta + (360.0*rotations))
		self.lastTheta = theta

	def setMotorSpeed(self, speed):
		#sets the motor to the given speed
		#I'll fill this in later
		self.speed = speed

	def __init__(self):
		self.startRot = -1  #the rotation when the reaction wheel started
		self.rot = -1  #the current rotation; this will be updated from outside this class
		self.distRot = -1  #how far the rocket has rotated since the motor started
		self.rotRate = -1  #the current rotation rate; this will be updated from outside this class
		self.rotations = -1  #the number of full rotations the rocket has completed since the motor started
		self.lastTheta = -1  #the last value of theta (see updateDistance())
		self.rotate = 0
		self.speed = 0

	def Update(self, rot, rotRate):
		self.rot = rot
		self.rotRate = rotRate
		self.updateRotation()
		if(self.rotate == 1):
			if(self.distRot >= 720.0):
				self.rotate = 2
		elif(self.rotate == 2):
			if(self.stopRotation()):
				self.setMotorSpeed(0)
				self.rotate = 3

	def End(self):
		print("MotorController is ending")
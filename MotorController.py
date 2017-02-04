#the way in which these functions will be run is:
#
#startRotation(rotation)
#while(distRot < 720):
#	#update rot and rotRate
#	updateRotation()
#	time.sleep(0.05)
#while(not stopRotation()):
#	#update rot and rotRate
#	updateDistance()
#	time.sleep(0.05)

startRot = -1  #the rotation when the reaction wheel started
rot = -1  #the current rotation; this will be updated from outside this class
distRot = -1  #how far the rocket has rotated since the motor started
rotRate = -1  #the current rotation rate; this will be updated from outside this class
rotations = -1  #the number of full rotations the rocket has completed since the motor started
lastTheta = -1  #the last value of theta (see updateDistance())

def stopRotation():
	#this function will be called ~20 times per second
	#the goal of this function is to reduce the rotaion rate to as close to 0 as possible
	
	#calculate speed
	setMotorSpeed(speed)
	
	#if the rotation rate is 0 (or very close to it) return True, else return False


def startRotation(rotation):
	#starts the rotation and initializes the variables
	#rotation is the current rotation in degrees
	setMotorSpeed(1)
	startRot = rotation
	distRot = 0
	rotations = 0
	lastTheta = 0


def updateDistance():
	#this function updates and returns distRot
	theta = (rot - startRot) if(rot >= startRot) else (rot + (360.0 - startRot))  #theta is the angle of the current rotation
	if(theta < lastTheta):  #a full rotation has occured
		rotations += 1
	distRot = (theta + (360.0*rotations))
	lastTheta = theta
	return distRot


def setMotorSpeed(speed):
	#sets the motor to the given speed
	#I'll fill this in later
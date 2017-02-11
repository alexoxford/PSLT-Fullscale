import time
from lsm.altimu import AltIMU
import math

class ReadIMU(object):

	def __init__(self):
		print("ReadIMU is starting")
		self.imu = AltIMU()
		self.imu.enable(True, True, True, True, True)
		self.start = time.time()
		self.motorState = 0
		self.lastAccList = [0.0, 0.0, 0.0]
		self.lastGyroList = [0.0, 0.0, 0.0]
		self.lastMagList = [0.0, 0.0, 0.0]
		self.lastAlt = 0.0
		self.data = {}

	def Update(self):
		errs = 0
		accList = self.imu.getAccelerometerRaw()#factor is 4098.0

		for i, acc in enumerate(accList):
			if(not acc == None):
				self.lastAccList[i] = acc
			else:
				errs += 1

		stop = time.time() - self.start
		self.start = time.time()
		deltaT = stop
		gyroList = self.imu.getComplementaryAngles(deltaT=deltaT)

		for i, gyro in enumerate(gyroList):
			if(not gyro == None):
				self.lastGyroList[i] = gyro
			else:
				errs += 1

		magList = self.imu.getMagnetometerRaw()

		for i, mag in enumerate(magList):
			if(not mag == None):
				self.lastMagList[i] = mag
			else:
				errs += 1

		rot = math.degrees(math.atan2(self.lastMagList[1], self.lastMagList[2]) + math.pi)

		alt = self.imu.getAltitude()
		if(not alt == None):
			self.lastAlt = alt
		else:
			errs += 1

		self.data["accX"] = self.lastAccList[0]
		self.data["accY"] = self.lastAccList[1]
		self.data["accZ"] = self.lastAccList[2]
		self.data["gyroX"] = self.lastGyroList[0]
		self.data["gyroY"] = self.lastGyroList[1]
		self.data["gyroZ"] = self.lastGyroList[2]
		self.data["magX"] = self.lastMagList[0]
		self.data["magY"] = self.lastMagList[1]
		self.data["magZ"] = self.lastMagList[2]
		self.data["alt"] = self.lastAlt
		self.data["rot"] = rot
		self.data["errs"] = errs
		self.data["time"] = time.time()

	def End(self):		
		print("ReadIMU is ending")

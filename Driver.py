import time
import subprocess
import os
import math
import threading
import numpy as np
from RecordVideo import RecordVideo
from ReadIMU import ReadIMU
from ReadGPS import ReadGPS
from SendData import SendData
from MotorController import MotorController
from TargetID import TargetID

class Driver(object):

	def StartGPS(self):	
		print("Starting GPS Daemon")

		subprocess.call(["sudo", "killall", "gpsd"])
		subprocess.call(["sudo", "gpsd", "/dev/ttyS0", "-F", "/var/run/gpsd.sock"])

		print("5...")
		time.sleep(1)
		print("4...")
		time.sleep(1)
		print("3...")
		time.sleep(1)
		print("2...")
		time.sleep(1)
		print("1...")
		time.sleep(1)

	def WriteData(self, dictGPS, dictIMU, dictVid):
		data = str(self.index) + ','
		
		data += str(dictGPS["lat"]) + ','
		data += str(dictGPS["lon"]) + ','
		#data += str(dictGPS["climb"]) + ','
		#data += str(dictGPS["alt"]) + ','
		#data += str(dictGPS["speed"]) + ','
		#data += str(dictGPS["track"]) + ','
		#data += str(dictGPS["errs"]) + ','
		#data += str(dictGPS["time"]) + ','
		
		data += str(dictIMU["accX"]) + ','
		data += str(dictIMU["accY"]) + ','
		data += str(dictIMU["accZ"]) + ','
		#data += str(dictIMU["gyroX"]) + ','
		#data += str(dictIMU["gyroY"]) + ','
		#data += str(dictIMU["gyroZ"]) + ','
		#data += str(dictIMU["magX"]) + ','
		data += str(dictIMU["magY"]) + ','
		data += str(dictIMU["magZ"]) + ','
		data += str(dictIMU["alt"]) + ','
		data += str(dictIMU["rot"]) + ','
		data += str(dictIMU["errs"]) + ','
		data += str(dictIMU["time"]) + ','
		
		#data += str(dictVid["rTop"]) + ','
		#data += str(dictVid["rBottom"]) + ','
		#data += str(dictVid["rLeft"]) + ','
		#data += str(dictVid["rRight"]) + ','
		data += str(dictVid["bTop"]) + ','
		data += str(dictVid["bBottom"]) + ','
		data += str(dictVid["bLeft"]) + ','
		data += str(dictVid["bRight"]) + ','
		#data += str(dictVid["yTop"]) + ','
		#data += str(dictVid["yBottom"]) + ','
		#data += str(dictVid["yLeft"]) + ','
		#data += str(dictVid["yRight"]) + ','
		data += str(dictVid["index"]) + ','
		data += str(dictVid["time"]) + ','
		
		data += str(self.mc.speed) + ','
		
		data += str(time.time())
		data += '\n'

		with open("/home/pi/Desktop/PSLT-Fullscale/Data/FlightData.csv", "ab") as dataFile:
			dataFile.write(data)
			dataFile.flush()
			os.fsync(dataFile.fileno())
			
	def VideoThread(self):
		self.vidProc = True
		#testStart = time.time()
		try:
			self.vid.Update(picture=True)
			#print("Pic: " + str(time.time() - testStart))

			#testStart = time.time()
			if(self.flightState > 0):
				self.tid.Update()
			#print("Target ID: " + str(time.time() - testStart))

			#testStart = time.time()
			self.vid.Update(flush=True)
			#print("Flush: " + str(time.time() - testStart))
		except:
			pass
		self.vidProc = False
		
	def GPSThread(self):
		self.gpsProc = True
		try:
			self.gps.Update()
		except:
			pass
		self.gpsProc = False

	def angle_between(self, v1, v2):
		v1_a = math.atan2(v1[0], v1[1])
		v2_a = math.atan2(v2[0], v2[1])
		diff = math.degrees(v1_a - v2_a)
		if(diff > 180):
			diff -= 360
		elif(diff < -180):
			diff += 360
		return diff

	def __init__(self):
		self.vid = RecordVideo()
		self.imu = ReadIMU()
		self.StartGPS()
		self.gps = ReadGPS()
		self.tx = SendData()
		self.mc = MotorController()
		self.tid = TargetID()
		self.gpsHeader = "Lat,Lon"
		self.imuHeader = "Acc X,Acc Y,Acc Z,Mag Y,Mag Z,Alt,Roll,IMU Errors,IMU Time"
		#self.vidHeader = "R Top,R Bottom,R Left,R Right,B Top,B Bottom,B Left,B Right,Y Top,Y Bottom,Y Left,Y Right,Vid Index,Vid Time"
		self.vidHeader = "B Top,B Bottom,B Left,B Right,Vid Index,Vid Time"
		self.index = 0
		self.vidProc = False
		self.gpsProc = False
		self.flightState = 0
		self.launchTime = -1
		with open("/home/pi/Desktop/PSLT-Fullscale/Data/FlightData.csv", "wb") as dataFile:
			dataFile.write("Index," + self.gpsHeader + ',' + self.imuHeader + ',' + self.vidHeader + ',' + "Motor Speed," + "Driver Time" + '\n')
			dataFile.flush()
			os.fsync(dataFile.fileno())
		self.vid.Update(picture=True)
		self.gps.Update()
		self.imu.Update()
		
		self.lastMagY = self.imu.data["magY"]
		self.lastMagZ = self.imu.data["magZ"]
		self.lastIMUTime = self.imu.data["time"]
		
		self.tid.Update()
		print("Initialization finished")
		quit = False
		while(not quit):
			try:
				print "Updating"
				self.Update()
			except KeyboardInterrupt:
				self.End()
				quit = True
			except:
				print("Unexpected error:", sys.exc_info()[0])

	def Update(self):
		if(not self.vidProc):
			videoThread = threading.Thread(name="video-thread", target=self.VideoThread)
			videoThread.start()
		
		try:
			self.imu.Update()
		except:
			pass
		
		if((math.fabs(self.imu.data["accX"]) > 2.0) & (self.flightState == 0)):
			self.flightState = 1
			self.launchTime = time.time()
			print("LAUNCH")
		if((math.fabs(self.imu.data["accX"]) < 2.0) & (self.flightState == 1)):
			print("BURNOUT")
			self.mc.startRotation(self.imu.data["rot"])
			print("ROLL")
			self.flightState = 2
		if(((self.flightState == 2) & ((time.time() - self.launchTime) > 9))):
			self.mc.rotate = 2
			print("COUNTER ROLL")
		if(((self.flightState == 2) & ((self.mc.rotate == 3) | ((time.time() - self.launchTime) > 12.5)))):
			self.flightState = 3
			self.mc.rotate = 3
			print("END ROTATION")
		
		if(not self.gpsProc):
			gpsThread = threading.Thread(name="gps-thread", target=self.GPSThread)
			gpsThread.start()
		
		rotRate = 0
		rotThreshold = 1
		rot = self.imu.data["rot"]
		magY = self.imu.data["magY"]
		magZ = self.imu.data["magZ"]
		imuTime = self.imu.data["time"]
		
		delta = self.angle_between((magY, magZ), (self.lastMagY, self.lastMagZ))
		if(math.fabs(delta) < rotThreshold):
			delta = 0
		deltaTime = imuTime - self.lastIMUTime
		if(deltaTime == 0):
			deltaTime = 0.05
		rotRate = delta / (deltaTime)
		
		try:
			self.mc.Update(rot, delta, rotRate)
		except:
			pass
		#print(self.mc.speed, self.mc.distRot, rotRate)
		self.lastIMUTime = imuTime
		self.lastMagY = magY
		self.lastMagZ = magZ
		
		try:
			self.WriteData(self.gps.data, self.imu.data, self.tid.data)
		except:
			pass
		
		try:
			self.tx.Update()
		except:
			pass
		
		self.index += 1
		
		#time.sleep(0.01)
		#print("Update: " + str(time.time() - testStart))

	def End(self):
		self.vid.End()
		self.imu.End()
		self.gps.End()
		self.tx.End()
		self.mc.End()
		self.tid.End()
		print("Driver is ending")
		
if __name__ == "__main__": Driver()
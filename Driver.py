import time
import subprocess
import os
import math
import RecordVideo
import ReadIMU
import ReadGPS
import SendData
import MotorController
import TargetID

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
		data = index + ','
		
		data += str(dictGPS["lat"]) + ','
		data += str(dictGPS["lon"]) + ','
		data += str(dictGPS["climb"]) + ','
		data += str(dictGPS["alt"]) + ','
		data += str(dictGPS["speed"]) + ','
		data += str(dictGPS["track"]) + ','
		data += str(dictGPS["errs"]) + ','
		data += str(dictGPS["time"]) + ','
		
		data += str(dictIMU["accX"]) + ','
		data += str(dictIMU["accY"]) + ','
		data += str(dictIMU["accZ"]) + ','
		data += str(dictIMU["gyroX"]) + ','
		data += str(dictIMU["gyroY"]) + ','
		data += str(dictIMU["gyroZ"]) + ','
		data += str(dictIMU["magX"]) + ','
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

	def __init__(self):
		self.vid = RecordVideo()
		self.imu = ReadIMU()
		self.gps = ReadGPS()
		self.tx = SendData()
		self.mc = MotorController()
		self.tid = TargetID()
		self.gpsHeader = "Lat,Lon,Climb,Alt,Speed,Heading,GPS Errors,GPS Time"
		self.imuHeader = "Acc X,Acc Y,Acc Z,Gyro X,Gyro Y,Gyro Z,Mag X,Mag Y,Mag Z,Alt,Roll,IMU Errors,IMU Time"
		#self.vidHeader = "R Top,R Bottom,R Left,R Right,B Top,B Bottom,B Left,B Right,Y Top,Y Bottom,Y Left,Y Right,Vid Index,Vid Time"
		self.vidHeader = "B Top,B Bottom,B Left,B Right,Vid Index,Vid Time"
		self.index = 0
		self.elapsed = 0
		self.start = time.time()
		self.stop = time.time()
		self.flightState = 0
		StartGPS()
		with open("/home/pi/Desktop/PSLT-Fullscale/Data/FlightData.csv", "wb") as dataFile:
			dataFile.write("Index," + gpsHeader + ',' + imuHeader + ',' + vidHeader + ',' + "Motor Speed," + "Driver Time" + '\n')
			dataFile.flush()
			os.fsync(dataFile.fileno())
		self.vid.Update(picture=True)
		self.gps.Update()
		self.imu.Update()
		self.lastRot = self.imu.data["rot"]
		self.lastIMUTime = self.imu.data["time"]
		self.tid.Update()
		print("Initialization finished")
		quit = False
		while(not quit):
			try:
				Update()

			except KeyboardInterrupt:
				End()
				quit = True

	def Update(self):
		self.stop = time.time()
		self.elapsed = self.stop - self.start
		if(self.elapsed > 1):
			self.start = time.time()
			self.elapsed = 0
			self.vid.Update(picture=True)
			self.tid.Update()
		else:
			self.vid.Update()
		self.imu.Update()
		if(math.fabs(self.imu.data["accX"]) > 2.0 & flightState == 0):
			flightState = 1
		if(math.fabs(self.imu.data["accX"]) < 2.0 & flightState == 1):
			self.mc.startRotation(self.imu.data["rot"])
			flightState = 2
		if(flightState == 2 & self.mc.rotate = 3):
			flightState = 3
		self.gps.Update()
		rotRate = 0
		rot = self.imu.data["rot"]
		imuTime = self.imu.data["time"]
		if(rot >= lastRot):
			rotRate = ((rot - lastRot) / (imuTime - lastIMUTime))
		else:
			rotRate = (((360.0 - lastRot) + rot) / (imuTime - lastIMUTime))
		self.mc.Update(rot, rotRate)
		WriteData(self.gps.data, self.imu.data, self.tid.data)
		self.tx.Update()
		self.index += 1
		#time.sleep(0.01)

	def End(self):
		self.vid.End()
		self.imu.End()
		self.gps.End()
		self.tx.End()
		self.mc.End()
		self.tid.End()
		print("Driver is ending")
		
if __name__ == "__main__": Driver()
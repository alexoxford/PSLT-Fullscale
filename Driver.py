import time
from datetime import datetime
import subprocess
import os
import RecordVideo
import ReadIMU
import ReadGPS
import SendData
import MotorController

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

	def WriteData(self, dictGPS, dictIMU):
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
		data += str(datetime.now())
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
		self.header = "Index,Lat,Lon,Climb,Alt,Speed,Heading,GPS Errors,GPS Time,Acc X,Acc Y,Acc Z,Gyro X,Gyro Y,Gyro Z,Mag X,Mag Y,Mag Z,Alt,Roll,IMU Errors,IMU Time,Driver Time\n"
		self.index = 0
		StartGPS()
		with open("/home/pi/Desktop/PSLT-Fullscale/Data/FlightData.csv", "wb") as dataFile:
			dataFile.write(header)
			dataFile.flush()
			os.fsync(dataFile.fileno())
		quit = False
		while(not quit):
			try:
				Update()

			except KeyboardInterrupt:
				End()
				quit = True

	def Update(self):
		self.vid.Update()
		self.imu.Update()
		self.gps.Update()
		WriteData(self.gps.data, self.imu.data)
		self.tx.Update()
		self.mc.Update()
		self.index += 1
		#time.sleep(0.01)

	def End(self):
		self.vid.End()
		self.imu.End()
		self.gps.End()
		self.tx.End()
		print("Driver is ending")
		
if __name__ == "__main__":__init__()
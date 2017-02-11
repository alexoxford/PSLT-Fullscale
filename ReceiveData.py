import serial
import time
import os
from socket import *

ser = serial.Serial("COM3", 9600, timeout=10)
host = "192.168.1.11" # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
lastAlt = 0.0
lastIMUTime = 0.0
quit = False

while(not quit):
	try:
		data = ser.readline()
		if(len(data.split(',')) == 30):
			with open("exData.csv", 'ab') as f:
				f.write(data)

			dataList = data.split(',')
			alt = float(dataList[18]) * 3.2808399
			imuTime = float(dataList[21])
			vel = (alt - lastAlt) / (imuTime - lastIMUTime)
			lastAlt = alt
			lastIMUTime = imuTime
			
			os.system("cls")
			print("Altitude: {0}ft AGL".format(alt))
			print("Velocity: {0}ft/s".format(vel))
			
			#gpsData = dataList[1] + "," + dataList[2]
			#print gpsData
			#UDPSock.sendto(gpsData, addr)
		
	except KeyboardInterrupt:
		quit = True
		
UDPSock.close()
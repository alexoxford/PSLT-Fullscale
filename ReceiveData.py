import serial
import time
import os
from socket import *

ser = serial.Serial("COM3", 9600, timeout=10)
host = "192.168.1.11" # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
quit = False

while(not quit):
	try:
		data = ser.readline()
		if(len(data.split(',')) == 23):
			with open("exData.csv", 'ab') as f:
				f.write(data)

			dataList = data.split(',')
			gpsData = dataList[1] + "," + dataList[2]
			#print gpsData
			UDPSock.sendto(gpsData, addr)
				
		time.sleep(0.01)
		
	except KeyboardInterrupt:
		quit = True
		
UDPSock.close()
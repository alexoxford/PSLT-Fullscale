import serial
import time
import os
import math

ser = serial.Serial("COM3", 9600, timeout=10)
lastAlt = 0.0
lastIMUTime = 0.0
ground = 0.0
launchTime = 0
flightState = 0
quit = False

while(not quit):
	try:
		data = ser.readline()
		if(len(data.split(',')) == 20):
			with open("exData.csv", 'ab') as f:
				f.write(data)

			dataList = data.split(',')
			acc = float(dataList[3])
			motor = float(dataList[18])
			alt = float(dataList[8]) * 3.2808399
			if(ground == 0.0):
				ground = alt
			alt -= ground
			imuTime = float(dataList[11])
			vel = (alt - lastAlt) / (imuTime - lastIMUTime)
			lastAlt = alt
			lastIMUTime = imuTime
			if((flightState == 0) & (math.fabs(acc) > 2.0)):
				launchTime = time.time()
				flightState = 1
			if((flightState == 1) & (vel < 0.0)):
				flightState == 2
			if((flightState == 2) & (vel > -50.0)):
				flightState = 3
			if((flightState == 3) & (math.fabs(vel) < 5.0)):
				flightState = 4
			
			os.system("cls")
			print("Altitude: {0} ft ASL".format(int(alt)))
			print("Velocity: {0} ft/s".format(int(vel)))
			if(motor == 0.0):
				print("Motor: Off")
			else:
				print("Motor: {0}%".format(motor * 100.0))
			if(flightState == 0):
				print("State: Pre-launch")
				print("Safe?: Yes")

			elif(flightState == 1):
				print("State: Ascent")
				print("Safe?: Yes")

			elif(flightState == 2):
				print("State: Drogue")
				if(vel > -150.0):
					print("Safe?: Yes")
				else:
					print("Safe?: No")

			elif(flightState == 3):
				print("State: Main")
				if(vel > -50.0):
					print("Safe?: Yes")
				else:
					print("Safe?: No")

			elif(flightState == 4):
				print("State: Landed")
				print("Safe?: Yes")
					
			if(flightState == 0):
				print("T+: N/A")
			else:
				print("T+: {0}".format(int(time.time() - launchTime)))
		
	except KeyboardInterrupt:
		quit = True
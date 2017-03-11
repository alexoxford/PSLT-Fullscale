import time
import serial
import csv
from collections import deque

class SendData(object):

	def get_last_row(self, csv_filename):
		try:
			with open(csv_filename, "rb") as f:
				try:
					lastrow = deque(csv.reader(f), 1)[0]
				except IndexError:  # empty file
					lastrow = None
		except IOError:
			lastrow = None

		return lastrow

	def __init__(self):
		print("SendData is starting")
		self.fails = 0
		success = False
		while(not success):
			try:
				self.ser = serial.Serial("/dev/ttyUSB0", 9600)
				success = True
			except KeyboardInterrupt:
				raise
			except:
				pass

	def Update(self):
		data = self.get_last_row("/home/pi/Desktop/PSLT-Fullscale/Data/FlightData.csv")

		if(not data == None):
			data = ','.join(data)
			data += '\n'
			#print data
			try:
				self.ser.write(data)
			except KeyboardInterrupt:
				raise
			except:
				self.fails += 1
				if(fails > 5):
					print("Attempting to restart serial connection")
					try:
						self.ser = serial.Serial("/dev/ttyUSB0", 9600)
						print("Connection reestablished")
						fails = 0
					except:
						print("Connection failed")

	def End(self):
		print "SendData is ending"
import time
import serial
import csv
from collections import deque

class SendData(object):

def get_last_row(csv_filename):
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
	print "SendData is starting"
	self.ser = serial.Serial("/dev/ttyUSB0", 9600)
	
def Update(self):
	data = get_last_row("/home/pi/Desktop/PSLT-Fullscale/Data/FlightData.csv")

	if(not data == None):
		#print data
		ser.write(data)

def End(self):
	print "SendData is ending"
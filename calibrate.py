import time
from lsm.altimu import AltIMU
import math

imu = AltIMU()
yList = []
zList = []

print "Starting Calibration..."
startTime = time.time()
done = False

print "Begin Rotation"

while(not done):
	magList = imu.getMagnetometerRaw()
	yList += magList[1]
	zList += magList[2]
	if((time.time() - startTime) > 10):
		done = True

print "End Rotation"

yMax = max(yList)
yMin = min(yList)
yRange = yMax - yMin
yOffset = yMin + (yRange / 2.0)

zMax = max(zList)
zMin = min(zList)
zRange = zMax - zMin
zOffset = zMin + (zRange / 2.0)

offsetStr = str(yOffset) + "," + str(zOffset)

with open("/home/pi/Desktop/PSLT-Fullscale/Data/magOffsets.txt", "wb") as f:
	f.write(offsetStr)
	
print "Finished Calibration: " + offsetStr
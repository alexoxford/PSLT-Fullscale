import time
import cv2
import numpy as np
import copy

class TargetID(object):

	def __init__(self):
		print("TargetID is starting")
		self.data = {}
		self.index = 0
		self.rocketMask = cv2.imread("/home/pi/Desktop/PSLT-Fullscale/Data/mask.jpg")
		#self.rocketMask = cv2.imread("C:\\Users\\admin\\Desktop\\mask.jpg")
		#self.Update()
		
	def Update(self):
		#start = time.time()
		#frame = cv2.imread("C:\\Users\\admin\\Desktop\\test.jpg")
		frame = cv2.imread("/home/pi/Desktop/PSLT-Fullscale/Data/img.jpg")
		#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		hsv = frame
		boundaries = [
		([70, 20, 0], [110, 40, 50]),#blue
		([50, 0, 150], [70, 20, 180]),#red
		([0, 150, 150], [100, 255, 255])#yellow
		]
		output = copy.copy(frame)
		for i, (lower, upper) in enumerate(boundaries):
			lower = np.array(lower, dtype = "uint8")
			upper = np.array(upper, dtype = "uint8")
			
			hsv = cv2.bitwise_and(hsv, self.rocketMask)
			mask = cv2.inRange(hsv, lower, upper)
			#output = cv2.bitwise_and(frame, frame, mask = mask)
			
			pxs = cv2.countNonZero(mask)
			
			stop = False
			failed = False
			height, width = mask.shape
			top = 1
			bottom = 1
			left = 1
			right = 1
			threshold = 2
			while(not stop and not failed):
				if(top < height):
					tempMask = mask[top:,:]
					tempPxs = cv2.countNonZero(tempMask)
					if(pxs - tempPxs >= threshold):
						top -= 1
						stop = True
					else:
						top += 1
				else:
					stop = True
					failed = True
			
			stop = False		
			while(not stop and not failed):
				if(bottom < height):
					tempMask = mask[:-bottom,:]
					tempPxs = cv2.countNonZero(tempMask)
					if(pxs - tempPxs >= threshold):
						bottom -= 1
						stop = True
					else:
						bottom += 1
				else:
					stop = True
					failed = True
					
			stop = False		
			while(not stop and not failed):
				if(left < height):
					tempMask = mask[:,left:]
					tempPxs = cv2.countNonZero(tempMask)
					if(pxs - tempPxs >= threshold):
						left -= 1
						stop = True
					else:
						left += 1
				else:
					stop = True
					failed = True
					
			stop = False		
			while(not stop and not failed):
				if(right < height):
					tempMask = mask[:,:-right]
					tempPxs = cv2.countNonZero(tempMask)
					if(pxs - tempPxs >= threshold):
						right -= 1
						stop = True
					else:
						right += 1
				else:
					stop = True
					failed = True
			
			iHeight = height - (top + bottom)
			iWidth = width - (left + right)
			
			#print top
			#print bottom
			#print left
			#print right
			#print iHeight
			#print iWidth
			#print failed			
			
				
			if(not failed):
				cv2.rectangle(output,(left, top),(left+iWidth, top+iHeight),(0,255,0))

			else:
				top = -1
				bottom = -1
				left = -1
				right = -1
				
			if(i == 0):
				self.data["bTop"] = top
				self.data["bBottom"] = bottom
				self.data["bLeft"] = left
				self.data["bRight"] = right
			elif(i == 1):
				self.data["rTop"] = top
				self.data["rBottom"] = bottom
				self.data["rLeft"] = left
				self.data["rRight"] = right
			elif(i == 2):
				self.data["yTop"] = top
				self.data["yBottom"] = bottom
				self.data["yLeft"] = left
				self.data["yRight"] = right
				
		#print(time.time() - start)
		#cv2.imshow("images", np.hstack([frame, output]))
		#cv2.waitKey(0)
		cv2.imwrite("/home/pi/Desktop/PSLT-Fullscale/Data/output{0}.jpg".format(self.index), output)
		self.data["index"] = self.index
		self.index += 1
		self.data["time"] = time.time()
		#print self.data
	
	def End(self):
		print("TargetID is ending")
		
#if __name__ == "__main__": TargetID()
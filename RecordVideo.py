from picamera import PiCamera
import time
import os

class RecordVideo(object):
	
	def __init__(self):
		print("RecordVideo is starting")
		self.quit = False
		self.videoFile = open("/media/pi/Samsung USB/video.h264", "wb")
		self.camera = PiCamera()
		self.camera.resolution = (800, 600)
		self.camera.start_recording(videoFile)
		print("Camera warmup...")
		print("2...")
		time.sleep(1)
		print("1...")
		time.sleep(1)

	def Update(self, picture=False):
		if(picture):
			self.camera.capture("/home/pi/Desktop/PSLT-Fullscale/Data/img.jpg", use_video_port=True)
		self.videoFile.flush()
		os.fsync(self.videoFile.fileno())
		
	def End(self):
		camera.stop_recording()
		print("RecordVideo is ending")
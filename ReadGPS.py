import gps
import time

class ReadGPS(object):

	def __init__(self):
		print("ReadGPS is starting")

		self.session = gps.gps("localhost", "2947")
		self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
		report = self.session.next()
		report = self.session.next()
		report = self.session.next()
		report = self.session.next()

		self.lastLat = 0.0
		self.lastLon = 0.0
		#self.lastClimb = 0.0
		#self.lastAlt = 0.0
		#self.lastSpeed = 0.0
		#self.lastTrack = 0.0
		self.data = {}
		self.data["lat"] = self.lastLat
		self.data["lon"] = self.lastLon
		#self.data["climb"] = self.lastClimb
		#self.data["alt"] = self.lastAlt
		#self.data["speed"] = self.lastSpeed
		#self.data["track"] = self.lastTrack
		#self.data["errs"] = 0
		#self.data["time"] = time.time()

	def Update(self):
		errs = 0
		report = self.session.next()
		if report["class"] == "TPV":
			if hasattr(report, "lat"):
				self.lastLat = report.lat
			else:
				errs += 1

			if hasattr(report, "lon"):
				self.lastLon = report.lon
			else:
				errs += 1

			#if hasattr(report, "climb"):
			#	self.lastClimb = report.climb
			#else:
			#	errs += 1
			#
			#if hasattr(report, "alt"):
			#	self.lastAlt = report.alt
			#else:
			#	errs += 1
			#
			#if hasattr(report, "speed"):
			#	self.lastSpeed = report.speed
			#else:
			#	errs += 1
			#
			#if hasattr(report, "track"):
			#	self.lastTrack = report.track
			#else:
			#	errs += 1
			#
			self.data["lat"] = self.lastLat
			self.data["lon"] = self.lastLon
			#self.data["climb"] = self.lastClimb
			#self.data["alt"] = self.lastAlt
			#self.data["speed"] = self.lastSpeed
			#self.data["track"] = self.lastTrack
			#self.data["errs"] = errs
			#self.data["time"] = time.time()

	def End(self):
		print("ReadGPS is ending")
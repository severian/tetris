import time

class Clock(object):
	def __init__(self, interval):
		self.time = time.time()
		self.interval = interval
		
	def time_elapsed(self):
		return time.time() - self.time
		
	def time_remaining(self):
		return self.interval - self.time_elapsed()
		
	def tick(self):
		self.time = time.time()
		
		
if __name__ == "__main__":
	c = Clock(0.5)
	print time.time()
	print c.time_elapsed()
	time.sleep(2)
	print time.time()
	print c.time_elapsed()
	
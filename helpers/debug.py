class Debugger:
	def __init__(self):
		self.i = 0

	def d(self):
		print('debug '+str(self.i))
		self.i += 1

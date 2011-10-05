# -*- coding: utf-8 -*-
import time, string, threading

class Stop_Watch(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
	

	def start(self):
		self.t_start = time.time()
	
	def stop(self):
		self.t_stop = time.time()
	
	def __str__(self):
		return str(self.t_stop - self.t_start)


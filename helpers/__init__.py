# -*- coding: utf-8 -*-
import time, string, threading, pygame
from pygame.locals import *

class Stop_Watch(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
	

	def start(self):
		self.t_start = time.time()
	
	def stop(self):
		self.t_stop = time.time()
	
	def __str__(self):
		return str(self.t_stop - self.t_start)

	def get_time(self,i=4):
		return round(self.t_stop-self.t_start,i)


class Instruction:

	def play(self,instr,clean=True):

		self.instr = instr
		self.instr = instr
		pygame.mixer.music.load(instr)
		pygame.mixer.music.set_volume(1.0)
		pygame.mixer.music.play()

		if clean:
			self.surface.fill(self.bg_blank)
			pygame.display.update()

		while True:
			for event in pygame.event.get():
				self.standart_event(event)

			if not pygame.mixer.music.get_busy():
				break

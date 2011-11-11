# -*- coding: utf-8 -*-
import time, string, threading, pygame, random
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


class Trail_Data:

	def __init__(self,data_source):

		with open(data_source, mode='r') as data_file:
			data_str = data_file.read()

		data_list = string.split(data_str,'\n')
		self.data = []
		for i in data_list:
			if i != '':
				par_list = string.split(i,'\t')
				self.data.append(par_list)

#		print self.data

	
	def __str__(self):
		out = ''
		for i in range(len(self.data)-1):
			for j in self.data[i]:
				out += str(j) +'\t'
			out += self.data[i].__str__()
			out += '\n'
		return out


	def get_n_trails(self):
		return len(self.data)


	def get_trail(self):
		if len(self.data)-1 >= 0:
			i = random.randint(0,len(self.data)-1)
			#print(len(self.data))
			#print(i)
			out = self.data[i]
			#self.data = self.data[:i] + self.data[i+1:]
			return i,out
		else:
			return None,None

	def accept(self,i):
		self.data = self.data[:i] + self.data[i+1:]

# -*- coding: utf-8 -*-
import time, string, threading, pygame, random
from pygame.locals import *

class Stop_Watch(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.first = False
	

	def start(self):
		self.t_start = time.time()
		self.first = True
	
	def stop(self):
		self.t_stop = time.time()
		if self.first:
			self.first_time = self.t_stop - self.t_start
			self.first = False
	
	def __str__(self):
		return str(self.t_stop - self.t_start)

	def get_time(self,i=4):
		return round(self.t_stop-self.t_start,i)

	def get_first_time(self,i=4):
		return round(self.first_time,i)


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


class Trial_Data:

	def __init__(self,data_source):

		with open(data_source, mode='r') as data_file:
			data_str = data_file.read()

		data_list = string.split(data_str,'\n')
		self.data = []
		for i in data_list:
			if i != '':
				par_list = string.split(i,'\t')
				self.data.append(par_list)


	
	def __str__(self):
		out = ''
		for i in range(len(self.data)-1):
			for j in self.data[i]:
				out += str(j) +'\t'
			out += self.data[i].__str__()
			out += '\n'
		return out


	def get_n_trials(self):
		return len(self.data)


	def get_trial(self):
		if len(self.data)-1 >= 0:
			i = random.randint(0,len(self.data)-1)
			out = self.data[i]
			return i,out
		else:
			return None,None

	def accept(self,i):
		self.data = self.data[:i] + self.data[i+1:]

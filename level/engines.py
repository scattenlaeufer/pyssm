# -*- coding: utf-8 -*-
import pygame, random, sys, string
from helpers import Stop_Watch, Trial_Data
from helpers.log import Trail_Logger
from helpers.debug import Debugger
from pygame.locals import *

class Engine:

	def __init__(self, surface, bg, syllables, syllable_sounds, syllable_images, random_order, order):
		self.miss = 0
		self.frames = 40
		self.surface = surface
		self.bg = bg
		self.random_order = random_order
		self.order = order
		self.mainClock = pygame.time.Clock()
		self.curser_unvisible = False

		self.syllable_images = syllable_images
		self.syllables = syllables.keys()
		self.syllables_allowed = syllables
		self.syllable_sounds = syllable_sounds
		self.n_syllables = len(self.syllables)
		self.syllables_called = {}

		for syllable in self.syllables:
			self.syllables_called[syllable] = 0


	def toggle_fullscreen(self):

		pygame.display.toggle_fullscreen()
		self.curser_unvisible = pygame.mouse.set_visible(self.curser_unvisible)


	def standart_event(self,event):

		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.quit()
				sys.exit()
			if event.key == ord('f'):
				self.toggle_fullsreen()


	def get_miss(self): return self.miss
	
	def get_frams(self): return self.frames

	
	def set_frames(self,frames):
		self.frames = frames


	def move(self,start,stop,time,position):

		speed = (stop - stop) / time
		#have to find a way to get the frame rate, so i can evolve the actuel pixels to move at a frame
		return int(position + speed/40.)


	def draw_sprite(self,sprite):
		self.surface.blit(sprite,(self.position_center_width(sprite),self.surface.get_size()[1]-sprite.get_size()[1]))


	def enter_sprite(self,sprite,direction,time=1):
		if direction == 0:
			start = -1*sprite.get_size()[0]
		else:
			start = self.surface.get_size()[0]

		stop = self.position_center_width(sprite)
		move = float(stop - start)/float(time*40)

		p = start
		for i in range(time*40):
			self.surface.blit(self.bg,(0,0))
			p += move
			self.surface.blit(sprite,(p,self.surface.get_size()[1]-sprite.get_size()[1]))
			pygame.display.update()
			self.mainClock.tick(40)
		
		self.surface.blit(self.bg,(0,0))
		self.draw_sprite(sprite)
		pygame.display.update()


	def exit_sprite(self,sprite,direction,time=1):

		if direction == 0:
			stop = self.surface.get_size()[0]
		else:
			stop = -1*sprite.get_size()[0]

		start = self.position_center_width(sprite)
		move = float(stop - start)/float(time*40)
		
		p = start
		for i in range(time*40):
			self.surface.blit(self.bg,(0,0))
			p += move
			self.surface.blit(sprite,(p,self.surface.get_size()[1]-sprite.get_size()[1]))
			pygame.display.update()
			self.mainClock.tick(40)

		self.surface.blit(self.bg,(0,0))
		pygame.display.update()


	def draw_syllable_left(self,syllable):

		self.surface.blit(syllable,(150,300))


	def draw_syllable_right(self,syllable):

		self.surface.blit(syllable,(self.surface.get_size()[0]-syllable.get_size()[0]-150,300))


	def choose_two(self,source):

		out1 = random.randint(0,source-1)
		out2 = random.randint(0,source-2)

		if out1 <= out2:
			out2 = out2 + 1

		return (out1,out2)

	def check_correct_syllable(self,syllable):

		if self.syllables_called[syllable] < self.syllables_allowed[syllable]:
			self.syllables_called[syllable] += 1
			return True
		else:
			return False


	def position_center_width(self,item):

		return self.surface.get_size()[0]/2 - item.get_size()[0]/2

	def reset_syllables_called(self):
		
		for syllable in self.syllables:
			self.syllables_called[syllable] = 0


class OneOutOfTwo(Engine):

	def __init__(self, log, surface, bg, sprites, syllables, syllable_images, syllable_sounds, random_order=True, order=None, neo=True):
		Engine.__init__(self,surface,bg,syllables,syllable_sounds,syllable_images,random_order,order)
		self.log = log
		self.sprites = sprites
		self.n_sprites = len(self.sprites)

		if neo:
			self.left = u'xvlcwuiaeoüöäpzXVLCWUIAEOÜÖÄPZ'
			self.right = u'khgfqßsnrtdybm,.jKHGFQẞSNRTDYBM–•J'
		else:
			self.left = u'qwertasdfgyxcvbQWERTASDFGYXCVB'
			self.right = u'zuiopühjklöänmm,.-ZUIOPÜHJKLÖÄNM'


	def start(self,n=10):

		sw = Stop_Watch()
		self.reset_syllables_called()
		self.log.set_top('trail_nr\tsyllable_l\tsyllable_r\tsound\tkey_pressed\tresponse\tresponsetime\tsprite')

		if not self.random_order:
			trials = Trial_Data(self.order)
			n = trials.get_n_trials()
			site = []

		for i in range(n):
			size = self.surface.get_size()
			self.bg = pygame.transform.scale(self.bg,size)
			self.surface.blit(self.bg,(0,0))

			if self.random_order:
				correct = random.randint(0,1)
				direction = random.randint(0,1)
				if direction == 0:
					direction_str = 'l'
				else:
					direction_str = 'r'

				sprite_str = self.sprites.keys()[random.randint(0,self.n_sprites-1)]

				check = True
				while check:
					syllable = self.choose_two(self.n_syllables)
					check = not self.check_correct_syllable(self.syllables[syllable[correct]])
				syllable_str = [self.syllables[syllable[0]],self.syllables[syllable[1]]]

			else:
				accept = False
				i = 0
				while not accept:
					
					trial_nr,trial = trials.get_trial()
					syllable_correct = trial[4][:2]
					syllable_left = string.lower(trial[5][:2])
					syllable_right = string.lower(trial[6][:2])
					syllable_str = [syllable_left,syllable_right]
					if syllable_correct == syllable_left:
						correct = 0
					else:
						correct = 1
					if len(site) == 0 or trials.get_n_trials() <= 1 or i > 20:
						site.append(correct)
						accept = True
					else:
						if site[len(site)-1] != correct:
							site = [correct]
							accept = True
						else:
							if len(site) < 2:
								site.append(correct)
								accept = True
					i += 1
					if i > 1:
						print(str(trails.get_n_trails())+' => '+str(i))

				trials.accept(trial_nr)
				sprite = trial[1][:-4]
				sprite_str = sprite[:-2]
				direction_str = string.lower(sprite[-1:])
				if direction_str == 'l':
					direction = 0
				else:
					direction = 1

			sprite = self.sprites[sprite_str][direction_str]
			#self.draw_sprite(sprite)
			self.enter_sprite(sprite,direction)
			pygame.event.clear()
			self.draw_syllable_left(self.syllable_images[syllable_str[0]]['l'])
			self.draw_syllable_right(self.syllable_images[syllable_str[1]]['r'])
			pygame.display.update()

			self.syllable_sounds[syllable_str[correct]][str(random.randint(1,3))].play()
			sw.start()

			key_pressed = False
			press = 0

			while True:

				for event in pygame.event.get():
					self.standart_event(event)
					if event.type == KEYDOWN:
						try:
							if self.left.find(chr(event.key))>= 0:
								sw.stop()
								press = 0
								key_pressed = True
							if self.right.find(chr(event.key)) >=0:
								sw.stop()
								press = 1
								key_pressed = True
						except UnicodeDecodeError:
							print(event.key)

				
				if press == correct and key_pressed:
					log_line = [i,syllable_str[0],syllable_str[1],syllable_str[correct],press,int(press==correct),sw.get_time(),sprite_str]
					self.log.add(log_line)
					self.syllable_sounds[syllable_str[correct]]['pos'+str(random.randint(1,4))].play()
					self.surface.blit(self.bg,(0,0))
					self.draw_sprite(sprite)
					if correct == 0:
						self.draw_syllable_left(self.syllable_images[syllable_str[0]]['l'])
					else:
						self.draw_syllable_right(self.syllable_images[syllable_str[1]]['r'])
					pygame.display.update()
					pygame.time.wait(3700)
					pygame.event.clear()
					break

				if press != correct and key_pressed:
					log_line = [i,syllable_str[0],syllable_str[1],syllable_str[correct],press,int(press==correct),sw.get_time(),sprite_str]
					self.log.add(log_line)
					key_pressed = False
					self.syllable_sounds[syllable_str[correct]]['neg'+str(random.randint(1,2))].play() 
					self.surface.blit(self.bg,(0,0))
					self.draw_sprite(sprite)
					if correct == 0:
						self.draw_syllable_left(self.syllable_images[syllable_str[0]]['l'])
					else:
						self.draw_syllable_right(self.syllable_images[syllable_str[1]]['r'])
					pygame.display.update()
					pygame.time.wait(4500)
					self.miss += 1
					
					if correct == 0:
						self.draw_syllable_right(self.syllable_images[syllable_str[1]]['r'])
					else:
						self.draw_syllable_left(self.syllable_images[syllable_str[0]]['l'])
					pygame.display.update()
					self.syllable_sounds[syllable_str[correct]][str(random.randint(1,3))].play()
					sw.start()
					pygame.event.clear()

				self.mainClock.tick(40)
			self.exit_sprite(sprite,direction)

		return self.miss




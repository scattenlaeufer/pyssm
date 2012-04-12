# -*- coding: utf-8 -*-
import pygame, random, sys, string
from helpers import Stop_Watch, Trial_Data
from helpers.log import Trial_Logger
from helpers.debug import Debugger
from pygame.locals import *

class Engine:

	def __init__(self, surface, bg, syllables, syllable_sounds, syllable_images, random_order, order, neo=True):
		self.miss = 0
		self.frames = 40
		self.surface = surface
		self.bg = bg
		self.random_order = random_order
		self.order = order
		self.mainClock = pygame.time.Clock()
		self.curser_unvisible = False

		self.syllable_images = syllable_images
		self.syllables_allowed = syllables
		self.syllable_sounds = syllable_sounds
		self.syllables_called = {}

		if syllables != None:
			self.n_syllables = len(syllables)
			self.syllables = syllables.keys()
			for syllable in self.syllables:
				self.syllables_called[syllable] = 0

		if neo:
			self.left = u'xvlcwuiaeoüöäpzXVLCWUIAEOÜÖÄPZ'
			self.right = u'khgfqßsnrtdybm,.jKHGFQẞSNRTDYBM–•J'
		else:
			self.left = u'qwertasdfgyxcvbQWERTASDFGYXCVB'
			self.right = u'zuiopühjklöänmm,.-ZUIOPÜHJKLÖÄNM'


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
			if event.key == K_F10:
				self.toggle_fullscreen()


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


	def sprite_fly_in(self,s_l,s_r,time=1):

		y_l = self.position_center_height(s_l)
		y_r = self.position_center_height(s_r)
		p_l = -1*s_l.get_size()[0]
		p_r = self.surface.get_size()[0]
		m = float(p_r/2.2)/float(time*40)

		for i in range(time*40):
			self.surface.blit(self.bg,(0,0))
			p_l += m
			p_r -= m
			self.surface.blit(s_l,(p_l,y_l))
			self.surface.blit(s_r,(p_r,y_r))
			pygame.display.update()
			self.mainClock.tick(40)

		return (int(p_l),y_l),(int(p_r),y_r)


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


	def position_center_height(self,item):

		return self.surface.get_size()[1]/2 - item.get_size()[1]/2

	def reset_syllables_called(self):
		
		for syllable in self.syllables:
			self.syllables_called[syllable] = 0

	class Sprite:

		def __init__(self,surface,sprite,(x,y)):
			self.surface = surface
			self.pic = sprite
			self.position = (x,y)

		def move(self,dx,dy):
			self.position = (self.position[0]+dx,self.position[1]+dy)

		def draw(self):
			self.surface.blit(self.pic,self.position)

		def get_position(self):
			return self.position

		def set_position(self,x,y):
			self.position = (x,y)

		def get_sprite(self):
			return self.pic


class OneOutOfTwo(Engine):

	def __init__(self, log, surface, bg, sprites, syllables, syllable_images, syllable_sounds, random_order=True, order=None, neo=True):
		Engine.__init__(self,surface,bg,syllables,syllable_sounds,syllable_images,random_order,order,neo)
		self.log = log
		self.sprites = sprites
		self.n_sprites = len(self.sprites)


	def start(self,n=10):

		sw = Stop_Watch()
		self.reset_syllables_called()
		self.log.set_top('trial_nr\tsyllable_l\tsyllable_r\tsound\tkey_pressed\tresponse\tresponsetime\tsprite')

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
				while not accept:
					
					trial_index,trial = trials.get_trial()
					syllable_correct = trial[2]
					syllable_left = string.lower(trial[3])
					syllable_right = string.lower(trial[4])
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

				trials.accept(trial_index)
				sprite = trial[1]
				sprite_str = sprite[:-2]
				direction_str = string.lower(sprite[-1:])
				if direction_str == 'l':
					direction = 0
				else:
					direction = 1

			sprite = self.sprites[sprite_str][direction_str]
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
							if self.left.find(unichr(event.key))>= 0:
								sw.stop()
								press = 0
								key_pressed = True
							if self.right.find(unichr(event.key)) >=0:
								sw.stop()
								press = 1
								key_pressed = True
						except UnicodeDecodeError:
							print(event.key)

				
				if press == correct and key_pressed:
					log_line = [trial[0],syllable_str[0],syllable_str[1],syllable_str[correct],press,int(press==correct),sw.get_time(),sprite_str]
#					print(log_line)
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


class Space_Engine(Engine):

	def __init__(self,log,surface,bg,syllables,syllable_sounds,sprites,order,neo=True):
		Engine.__init__(self, surface, bg, syllables, syllable_sounds, None, False, order,neo)

		self.sprites = sprites
		self.log = log


	def start(self):

		sw = Stop_Watch()
		self.log.set_top('trial_nr\tsyllable_l\tsyllable_r\tsound\tkey_pressed\tresponse\tresponsetime')

		trials = Trial_Data(self.order)
		n = trials.get_n_trials()
		side = []
		miss = 0
		for i in range(n):
			size = self.surface.get_size()
			self.bg = pygame.transform.scale(self.bg,size)
			self.surface.blit(self.bg,(0,0))

			accept = False
			while not accept:

				trial_index,trial = trials.get_trial()
				syllable = trial[1]
				sprite = trial[2],trial[3]
				if syllable == sprite[0]:
					correct = 0
				else:
					correct = 1
				if len(side) == 0 or trials.get_n_trials() <= 1 or i > 20:
					side.append(correct)
					accept = True
				elif side[len(side)-1] != correct:
					side = [correct]
					accept = True
				elif len(side) < 2:
					side.append(correct)
					accept = True

			trials.accept(trial_index)

			position = self.sprite_fly_in(self.sprites[sprite[0]],self.sprites[sprite[1]])
			pygame.display.update()
			self.syllable_sounds[syllable][str(random.randint(1,3))].play()
			sw.start()

			key_pressed = False
			f = True
			pressed = -1

			while f:

				for event in pygame.event.get():
					self.standart_event(event)
					if event.type == KEYDOWN:
						try:
							if self.left.find(unichr(event.key)) >= 0:
								sw.stop()
								pressed = 0
								key_pressed = True
							elif self.right.find(unichr(event.key)) >= 0:
								sw.stop()
								pressed = 1
								key_pressed = 1
						except UnicodeDecodeError:
							print(event.key)

				if key_pressed:
					log_line = [trial[0],sprite[0],sprite[1],syllable,pressed,int(pressed==correct),sw.get_time()]
					self.log.add(log_line)
					self.surface.blit(self.bg,(0,0))
					self.surface.blit(self.sprites[sprite[correct]],position[correct])
					pygame.display.update()
					if pressed == correct:
						self.syllable_sounds[syllable]['pos'+str(random.randint(1,4))].play()
						pygame.time.wait(3700)
						pygame.event.clear()
						f = False

					if pressed != correct:
						key_pressed = False
						self.syllable_sounds[syllable]['neg'+str(random.randint(1,2))].play()
						pygame.time.wait(4500)
						miss += 1
						self.surface.blit(self.sprites[sprite[pressed]],position[pressed])
						pygame.display.update()
						self.syllable_sounds[syllable][str(random.randint(1,3))].play()
						sw.start()
						pygame.event.clear()

				self.mainClock.tick(24)

		return miss


class Balloon_Engine(Engine):

	def __init__(self,log,surface,bg,syllables,syllable_sound,sprites,data,neo=True):

		Engine.__init__(self,surface,bg,syllables,syllable_sound,None,False,data,neo)
		self.log = log
		self.sprites = sprites

	def start(self):

		sw = Stop_Watch()
		self.log.set_top('trial_nr\tsyllable_l\tsyllable_m\tsyllable_r\tsound\tkey_pressed\tresponse\trespones_time')
		trials = Trial_Data(self.order)
		n = trials.get_n_trials()
		side = []
		miss = 0
		for i in range(n):
			size = self.surface.get_size()
			bg = pygame.transform.scale(self.bg,size)
			self.surface.blit(bg,(0,0))

			accept = False
			k = 0
			while not accept:
				++k
				trial_index, trial = trials.get_trial()
				syllable = trial[1]
				sprite = trial[2],trial[3],trial[4]
				if syllable == sprite[0]:
					correct = 0
				elif syllable == sprite[1]:
					correct = 1
				else:
					correct = 2
				if len(side) == 0 or trials.get_n_trials() <= 1 or k > 20:
					side.append(correct)
					accept = True
				elif side[len(side)-1] != correct:
					side = [correct]
					accept = True
				elif len(side) < 2:
					side.append(correct)
					accept = True

			trials.accept(trial_index)
			left = Engine.Sprite(self.surface,self.sprites[sprite[0]]['r'],(self.position_center_width(self.sprites[sprite[0]]['r'])-300,self.surface.get_size()[1]))
			middle = Engine.Sprite(self.surface,self.sprites[sprite[1]]['y'],(self.position_center_width(self.sprites[sprite[1]]['y']),self.surface.get_size()[1]))
			right = Engine.Sprite(self.surface,self.sprites[sprite[2]]['g'],(self.position_center_width(self.sprites[sprite[2]]['g'])+300,self.surface.get_size()[1]))
			
			if correct == 0:
				sprite_correct = left
				sprite_wrong = [middle,right]
			elif correct == 1:
				sprite_correct = middle
				sprite_wrong = [left,right]
			elif correct == 2:
				sprite_correct = right
				sprite_wrong = [left,middle]
			
			self.surface.blit(bg,(0,0))
			[x.draw() for x in [left,middle,right]]
			pygame.display.update()

			while (left.get_position()[1] > self.position_center_height(left.get_sprite())):
				self.surface.blit(bg,(0,0))
				[x.move(0,-13) for x in [left,middle,right]]
				[x.draw() for x in [left,middle,right]]
				pygame.display.update()
				self.mainClock.tick(24)
			#raw_input('press any key to proceed')

			self.syllable_sounds[syllable][str(random.randint(1,3))].play()
			sw.start()

			f = True
			key_pressed = False
			pressed = -1

			while f:

				for event in pygame.event.get():
					self.standart_event(event)
					if event.type == KEYDOWN:
						try:
							if self.left.find(unichr(event.key)) >= 0:
								sw.stop()
								key_pressed = True
								pressed = 0
							elif self.right.find(unichr(event.key)) >= 0:
								sw.stop()
								key_pressed = True
								pressed = 2
							elif event.key == K_SPACE:
								sw.stop()
								key_pressed = True
								pressed = 1
						except ValueError:
							print(event.key)

				if key_pressed:
					log_line = [trial[0],sprite[0],sprite[1],sprite[2],syllable,pressed,int(pressed==correct),sw.get_time()]
					self.log.add(log_line)
					if pressed == correct:
						self.syllable_sounds[syllable]['pos'+str(random.randint(1,4))].play()
						self.balloon_wrong_exit(sprite_correct,sprite_wrong)
						pygame.time.wait(2100)
						self.balloon_correct_exit(sprite_correct)
						f = False
					else:
						self.syllable_sounds[syllable]['neg'+str(random.randint(1,2))].play()
						miss += 1
						self.balloon_wrong_exit(sprite_correct,sprite_wrong)
						pygame.time.wait(2600)
						self.balloon_wrong_enter(sprite_correct,sprite_wrong)
						pygame.event.clear()
						self.syllable_sounds[syllable][str(random.randint(1,3))].play()
						sw.start()
						key_pressed = False

		return miss
	
	def balloon_wrong_exit(self,right,wrong):

		while wrong[0].get_position()[1] > -1*(wrong[0].get_sprite().get_size()[1]):
			self.surface.blit(self.bg,(0,0))
			[x.move(0,-13) for x in [wrong[0],wrong[1]]]
			[x.draw() for x in [right,wrong[0],wrong[1]]]
			pygame.display.update()
			self.mainClock.tick(24)

	def balloon_wrong_enter(self,right,wrong):

		[x.set_position(x.position[0],self.surface.get_size()[1]) for x in [wrong[0],wrong[1]]]
		while wrong[0].get_position()[1] > right.get_position()[1]:
			self.surface.blit(self.bg,(0,0))
			[x.move(0,-13) for x in [wrong[0],wrong[1]]]
			[x.draw() for x in [right,wrong[0],wrong[1]]]
			pygame.display.update()
			self.mainClock.tick(24)

	def balloon_correct_exit(self,sprite):

		while sprite.position[1] > -1*sprite.pic.get_size()[1]:
			self.surface.blit(self.bg,(0,0))
			sprite.move(0,-13)
			sprite.draw()
			pygame.display.update()
			self.mainClock.tick(24)


class CatchMeIfYouCan(Engine):

	def __init__(self,log,surface,bg,syllable_sounds,sprites,order,neo=True):

		Engine.__init__(self,surface,bg,None,syllable_sounds,None,False,order,neo)
		self.log = log
		self.sprites = sprites

	def play_instruction(self,instr1,instr2,instr_image):
		self.surface.blit(instr_image,(0,0))
		pygame.display.update()
		instr1.play()
		pygame.time.wait(5000)
		instr2.play()
		pygame.time.wait(18000)
	
	def start(self):

		self.sw = Stop_Watch()
		self.log.set_top('trial_nr\tsound\tsprite\tdirection\tpressed\tresponse_time')
		trials = Trial_Data(self.order)
		n = trials.get_n_trials()
		miss = 0

		for i in range(n):
			trial_index, trial = trials.get_trial()
			trials.accept(trial_index)
			sprite = self.sprites[trial[1]][trial[3]]
			sound = trial[2]
			correct = trial[1] == trial[2]
			retry = True
			while retry:
				pressed = self.fly_through(sprite,trial[3],self.syllable_sounds[sound][str(random.randint(1,3))])
				log_line = [trial[0],sound,trial[1],trial[3],pressed,self.sw.get_first_time()]
				if correct:
					self.surface.blit(self.bg,(0,0))
					self.surface.blit(sprite,(self.position_center_width(sprite),self.position_center_height(sprite)))
					pygame.display.update()
					if pressed:
						retry = False
						self.syllable_sounds[sound]['pos'+str(random.randint(1,4))].play()
						pygame.time.wait(3700)
					else:
						self.syllable_sounds[sound]['miss'].play()
						pygame.time.wait(5500)
						miss += 1
				else:
					if pressed:
						self.surface.blit(self.bg,(0,0))
						self.surface.blit(self.sprites[trial[2]][trial[3]],(self.position_center_width(sprite),self.position_center_height(sprite)))
						pygame.display.update()
						self.syllable_sounds[sound]['neg'+str(random.randint(1,2))].play()
						pygame.time.wait(4500)
						miss += 1
					else:
						retry = False

		return miss


	def fly_through(self,sprite,direction,sound):

		size_sprite = sprite.get_size()[0]
		size_surface = self.surface.get_size()[0]

		if direction == 'r':
			x0 = -1*size_sprite
			dx = 5
		else:
			x0 = size_surface
			dx = -5

		s = Engine.Sprite(self.surface,sprite,(x0,self.position_center_height(sprite)))
		move = True
		moved = 0
		while move:
			s.move(dx,0)
			self.surface.blit(self.bg,(0,0))
			s.draw()
			pygame.display.update()
			moved += abs(dx)
			if moved > size_sprite:
				move = False
			self.mainClock.tick(36)

		pygame.event.clear()
		self.sw.start()
		sound.play()

		move = True
		pressed = False
		while move:
			s.move(dx,0)
			self.surface.blit(self.bg,(0,0))
			s.draw()
			pygame.display.update()
			if direction == 'r':
				if s.get_position()[0] > size_surface + size_sprite:
					move = False
			else:
				if s.get_position()[0] < -1*size_sprite:
					move = False

			for event in pygame.event.get():
				self.standart_event(event)
				if event.type == KEYDOWN:
					if event.key == K_SPACE:
						self.sw.stop()
						pressed = True
					else:
						print(chr(event.key))
			self.mainClock.tick(36)
		self.sw.stop()

		return pressed


class OneOutOfThree(Engine):

	def __init__(self,log,surface,bg,syllable_sound,syllable_sprites,sprites,order,neo=True):

		Engine.__init__(self,surface,bg,None,syllable_sound,syllable_sprites,False,order,neo)
		
		self.log = log
		self.sprites = sprites


	def start(self):

		sw = Stop_Watch()
		self.log.set_top('trial_nr\tsyllable_l\tsyllable_m\tsyllable_r\tsound\tkey_pressed\tresponse\tresponsetime')
		trials = Trial_Data(self.order)
		n = trials.get_n_trials()
		side = []
		miss = 0

		for i in range(n):
			size = self.surface.get_size()
			self.bg = pygame.transform.scale(self.bg,size)
			self.surface.blit(self.bg,(0,0))

			accept = False
			while not accept:
				trial_index, trial = trials.get_trial()
				syllable = trial[1]
				syllable_sprite = trial[2],trial[3],trial[4]
				if syllable_sprite[0] == syllable:
					correct = 0
				elif syllable_sprite[1] == syllable:
					correct = 1
				else:
					correct = 2
				if len(side) == 0 or trials.get_n_trials() <= 1 or i > 20:
					side.append(correct)
					accept = True
				elif side[len(side)-1] != correct:
					side = [correct]
					accept = True
				elif len(side) < 2:
					side.append(correct)
					accept = True

			trials.accept(trial_index)
#			print(syllable+'\t'+str(correct)+'\t'+str(syllable_sprite))
			sprite = self.sprites[trial[5]][trial[6]]
			if trial[6] == 'l':
				direction = 1
			else:
				direction = 0
			self.enter_sprite(sprite,direction)

			self.surface.blit(self.syllable_images[syllable_sprite[0]]['l'],(size[0]/4-self.syllable_images[syllable_sprite[0]]['l'].get_size()[0]/2,self.surface.get_size()[1]/3))
			self.surface.blit(self.syllable_images[syllable_sprite[1]]['m'],(self.position_center_width(self.syllable_images[syllable_sprite[1]]['m']),self.surface.get_size()[1]/3))
			self.surface.blit(self.syllable_images[syllable_sprite[2]]['r'],(3*size[0]/4-self.syllable_images[syllable_sprite[2]]['r'].get_size()[0]/2,self.surface.get_size()[1]/3))
			pygame.display.update()

			self.syllable_sounds[trial[1]][str(random.randint(1,3))].play()
			sw.start()

			key_pressed = False
			repeat = True
			pressed = 0
			pygame.event.clear()

			while repeat:

				for event in pygame.event.get():
					self.standart_event(event)
					if event.type == KEYDOWN:
						try:
							if self.left.find(unichr(event.key)) >= 0:
								sw.stop()
								pressed = 0
								key_pressed = True
							elif self.right.find(unichr(event.key)) >= 0:
								sw.stop()
								pressed = 2
								key_pressed = True
							elif event.key == K_SPACE:
								sw.stop()
								pressed = 1
								key_pressed = True
						except UnicodeDecodeError:
							print(event.key)

				if key_pressed:
					log_line = [trial[0],trial[2],trial[3],trial[4],trial[1],pressed,int(pressed==correct),sw.get_time()]
					self.log.add(log_line)
					self.surface.blit(self.bg,(0,0))
					self.draw_sprite(sprite)
					if correct == 0:
						self.surface.blit(self.syllable_images[syllable_sprite[0]]['l'],(size[0]/4-self.syllable_images[syllable_sprite[0]]['l'].get_size()[0]/2,self.surface.get_size()[1]/3))
					elif correct == 1:
						self.surface.blit(self.syllable_images[syllable_sprite[1]]['m'],(self.position_center_width(self.syllable_images[syllable_sprite[1]]['m']),self.surface.get_size()[1]/3))
					else:
						self.surface.blit(self.syllable_images[syllable_sprite[2]]['r'],(3*size[0]/4-self.syllable_images[syllable_sprite[2]]['r'].get_size()[0]/2,self.surface.get_size()[1]/3))
					pygame.display.update()

					if pressed == correct:
						self.syllable_sounds[syllable_sprite[correct]]['pos'+str(random.randint(1,4))].play()
						pygame.time.wait(4000)
						repeat = False
					else:
						self.syllable_sounds[syllable_sprite[correct]]['neg'+str(random.randint(1,2))].play()
						pygame.time.wait(4500)
						miss += 1
						if correct == 0:
							self.surface.blit(self.syllable_images[syllable_sprite[1]]['m'],(self.position_center_width(self.syllable_images[syllable_sprite[1]]['m']),self.surface.get_size()[1]/3))
							self.surface.blit(self.syllable_images[syllable_sprite[2]]['r'],(3*size[0]/4-self.syllable_images[syllable_sprite[2]]['r'].get_size()[0]/2,self.surface.get_size()[1]/3))
						elif correct == 1:
							self.surface.blit(self.syllable_images[syllable_sprite[0]]['l'],(size[0]/4-self.syllable_images[syllable_sprite[0]]['l'].get_size()[0]/2,self.surface.get_size()[1]/3))
							self.surface.blit(self.syllable_images[syllable_sprite[2]]['r'],(3*size[0]/4-self.syllable_images[syllable_sprite[2]]['r'].get_size()[0]/2,self.surface.get_size()[1]/3))
						else:
							self.surface.blit(self.syllable_images[syllable_sprite[0]]['l'],(size[0]/4-self.syllable_images[syllable_sprite[0]]['l'].get_size()[0]/2,self.surface.get_size()[1]/3))
							self.surface.blit(self.syllable_images[syllable_sprite[1]]['m'],(self.position_center_width(self.syllable_images[syllable_sprite[1]]['m']),self.surface.get_size()[1]/3))
						pygame.display.update()
						self.syllable_sounds[syllable_sprite[correct]][str(random.randint(1,3))].play()
						sw.start()
						key_pressed = False
						pygame.event.clear()

				self.mainClock.tick(40)


			self.exit_sprite(sprite,direction)

		return miss


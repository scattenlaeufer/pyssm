# -*- coding: utf-8 -*-

import pygame, sys, random, time, os
from pygame.locals import *
from engines import OneOutOfTwo, Space_Engine, Balloon_Engine, CatchMeIfYouCan
from helpers.log import Log_Handler
from helpers.log import Trail_Logger
from helpers import Stop_Watch


#generic form of a stage. all actual stages should inherit from this

class Stage:

	def __init__(self,bla=True):
		
		self.path = __file__[:-10]
		self.miss = 0
		self.instr = None
		self.mainClock = pygame.time.Clock()

		# init pygame
		pygame.init()

		# set window
		self.windowwidth = 1024
		self.windowheight = 768
		self.curser_unvisible = False
#		info = pygame.display.Insfo()
#		self.desktopwidth = info.current_w
#		self.desktopheight = info.current_h
#		print(str(self.desktopwidth)+' '+str(self.desktopheight))
		self.surface = pygame.display.set_mode((self.windowwidth,self.windowheight),0,32)
		pygame.display.set_caption('SSM Test v0.1') 

		self.bg_blank = (194,194,194)
		self.surface.fill(self.bg_blank)
		self.font1 = pygame.font.Font(None,70)
		if bla:
			self.text = self.font1.render('Willkommen zum Silbenlernspiel',True,(0,0,0))
			self.surface.blit(self.text,(self.position_center_width(self.text),100))


	def get_path(self,path):
		return os.path.join(self.path,path)


	def toggle_fullsreen(self):
		
		pygame.display.toggle_fullscreen()
		self.curser_unvisible = pygame.mouse.set_visible(self.curser_unvisible)
		
#		if self.curser_unvisible:
#			self.windowwidth = self.desktopwidth
#			self.windowheight = self.desktopheight
#		else:
#			self.windowwidth = 1024
#			self.windowheight = 768

#		self.surface = pygame.transform.scale(self.surface,(self.windowwidth,self.windowheight))
#		pygame.display.update()


	def start(self,modul,inst):
	
		text = self.font1.render(modul,True,(0,0,0))
		self.surface.blit(text,(self.position_center_width(text),250))
		pygame.display.update()

		self.play_instruction(inst,False)

		text = self.font1.render(u'bitte Enter-Taste drücken',True,(0,0,0))
		self.surface.blit(text,(self.position_center_width(text),400))
		pygame.display.update()

		bla = True

		while bla:
			for event in pygame.event.get():
				self.standart_event(event)
				if event.type == KEYDOWN:
					if event.key == K_RETURN:
						bla = False

			self.mainClock.tick(20)


	def stop(self):
		
		self.surface.fill(self.bg_blank)
		text = self.font1.render('Bitte nehmen Sie Kontakt mit uns auf.',True,(0,0,0))
		self.surface.blit(text,(self.position_center_width(text),self.position_center_height(text)))
		pygame.display.update()

		pygame.event.clear()
		bla = True
		while bla:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						bla = False
			self.mainClock.tick(10)

		pygame.quit()
		sys.exit()
		

	def end(self):
		
		image = pygame.image.load('images/bg/bg_wave.jpg')
		self.surface.blit(image,(0,0))
		pygame.display.update()
		self.play_instruction('audio/final/final1.ogg',False)
		pygame.quit()
		sys.exit()

	def load_sound(self,name):
		
		class NoneSound:
			def play(self): pass
		if not pygame.mixer:
			return NoneSound()
		try:
			sound = pygame.mixer.Sound(name)
		except pygame.error, message:
			print 'Cannot load sound:', ogg 
			raise SystemExit, message
		return sound


	def load_syllable_sound(self,syllable):

		dic = {}
		
		dic['1'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'1.ogg'))
		dic['2'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'2.ogg'))
		dic['3'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'3.ogg'))
		
		dic['miss'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'miss.ogg'))
		
		dic['neg1'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'neg1.ogg'))
		dic['neg2'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'neg2.ogg'))
		
		dic['pos1'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'pos1.ogg'))
		dic['pos2'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'pos2.ogg'))
		dic['pos3'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'pos3.ogg'))
		dic['pos4'] = self.load_sound(os.path.join(self.path,'audio/syllable/'+syllable+'pos4.ogg'))
		
		return dic

	
	def play_instruction(self,instr,clean=True):
		
		self.instr = instr
		pygame.mixer.music.load(os.path.join(self.path,instr))
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
			
			self.mainClock.tick(20)


	def position_center_width(self,item):

		return self.windowwidth/2 - item.get_size()[0]/2


	def position_center_height(self,item):

		return self.windowheight/2 - item.get_size()[1]/2


	def draw(self,image,dest=(0,0)):

		self.surface.blit(image,dest)
		pygame.display.update()


	def draw_left(self,image):

		self.surface.blit(image,(self.windowwidth/12,self.position_center_height(image)))


	def draw_right(self,image):

		self.surface.blit(image,(self.windowwidth*7/12,self.position_center_height(image)))


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
			if event.key == ord('q') and pygame.mixer.music.get_busy():
				pygame.mixer.music.stop()


	def watch_keypress(self):

		for event in pygame.event.get():
			self.standart_event(event)

	
	def teach_syllable(self,image,sound):
 
		self.surface.fill(self.bg_blank)

		sound.play()

		im = pygame.image.load(os.path.join(self.path,image))
		dimension = (self.windowwidth/3,self.transform_height(im,self.windowwidth/3))
		im = pygame.transform.scale(im,dimension)
		self.surface.blit(im,(self.position_center_width(im),self.position_center_height(im)))
		pygame.display.update()
		pygame.time.wait(3000)
		self.watch_keypress()

	def transform_height(self,item,width):

		x = item.get_size()[0]
		y = item.get_size()[1]
		ratio = float(y)/float(x)
		return int(width * ratio)


	def test_syllable(self,syllable,dic,n=8):

		miss = 0
		sw = Stop_Watch()
		log = Trail_Logger('test_'+syllable)
		log.set_top('trail_nr\tkey_pressed\tresponse\tresponse_time')
		m = 1

		for i in range(n):
			self.surface.fill(self.bg_blank)
			correct = random.randint(1,2)

			image = pygame.image.load(os.path.join(self.path,'images/syllables/'+syllable.upper()+'.gif'))
			dimension = (self.windowwidth/3,self.transform_height(image,self.windowwidth/3))
			image = pygame.transform.scale(image,dimension)

			distr = pygame.image.load(os.path.join(self.path,'images/distr/DISTR'+str(random.randint(1,10))+'.gif'))
			distr = pygame.transform.scale(distr,dimension)
			
			if correct == 1:
				self.draw_left(image)
				self.draw_right(distr)
			else:
				self.draw_left(distr)
				self.draw_right(image)

			pygame.display.update()
			dic[str(random.randint(1,3))].play()
			sw.start()

			key_pressed = False
			press = 0

			while True:
				for event in pygame.event.get():
					self.standart_event(event)

					if event.type == KEYDOWN:
						if event.key == ord('u'):
							sw.stop()
							press = 1
							key_pressed = True
						if event.key == ord('d'):
							sw.stop()
							press = 2
							key_pressed = True
						if event.key == K_F1:
							self.play_instruction(self.instr,False)

				if press == correct and key_pressed:
					log.add([m,press,int(press==correct),sw.get_time()])
					dic['pos'+str(random.randint(1,4))].play()
					self.surface.fill(self.bg_blank)
					if correct == 1:
						self.draw_left(image)
					else:
						self.draw_right(image)
					pygame.display.update()
					pygame.time.wait(3700)
					pygame.event.clear()
					break
				if press != correct and key_pressed:
					log.add([m,press,int(press==correct),sw.get_time()])
					key_pressed = False
					dic['neg'+str(random.randint(1,2))].play()
					self.surface.fill(self.bg_blank)

					if correct == 1:
						self.draw_left(image)
					else:
						self.draw_right(image)

					pygame.display.update()
					miss += 1
					pygame.time.wait(4500)
					
					if correct == 1:
						self.draw_right(distr)
					else:
						self.draw_left(distr)
					pygame.display.update()
					dic[str(random.randint(1,3))].play()
					sw.start()
					pygame.event.clear()
				
				self.mainClock.tick(40)

			pygame.time.wait(500)
			m += 1

		log.save()
		return miss



class Stage_A(Stage):

	def __init__(self,log,teach=False,test=False,rep=False):
	   
		if teach or test:
			Stage.__init__(self,False)
		else:
			Stage.__init__(self,True)

		#load sounds
		if not (teach and test):
			self.init_syllable_sound()
			repitition = 0

		if not rep:
			if not (teach or test):
				#edit title for modul A
				self.start('Modul A','audio/instr/instr1.ogg')

				#teach and test LO
				self.teach_syllable('images/syllables/KO.gif',self.load_sound(os.path.join(self.path,'audio/pres/preslo.ogg')))
				self.play_instruction('audio/instr/instr2.ogg')
				self.teach_syllable('images/syllables/KO.gif',self.lo['1'])
				
				self.play_instruction('audio/instr/instr3.ogg')

			if not test:
				miss = 0
				miss = self.test_syllable('ko',self.lo,8)
				if miss > 2 and not teach:
					miss = 0
					miss = self.test_syllable('ko',self.lo,8)
					repitition += 1
					if miss > 2:
						log.add('A',0,-1)
						log.save()
						self.stop()

			if not (teach or test):
				#teach and test MA
				self.play_instruction('audio/instr/instr4.ogg')

				self.teach_syllable('images/syllables/ME.gif',self.load_sound(os.path.join(self.path,'audio/pres/presma.ogg')))
				self.play_instruction('audio/instr/instr2.ogg')
				self.teach_syllable('images/syllables/ME.gif',self.ma['1'])

				self.play_instruction('audio/instr/instr3.ogg')

			if not test:
				miss = 0
				miss = self.test_syllable('me',self.ma,8)
				if miss > 2 and not teach:
					miss = 0
					repitition += 1
					miss = self.test_syllable('me',self.ma,8)
					if miss > 2:

						log.add('A',0,-1)
						log.save()
						self.stop()
				res_teach = 1
				
				if repitition == 2:
					log.add('A',0,-1)
					log.sale()
					self.end()

			else:
				res_teach = -1
		else:
			res_teach = -1
			self.start('Modul R','audio/instr/instr7.ogg')
			self.teach_syllable('images/syllables/KO.gif',self.load_sound(os.path.join(self.path,'audio/pres/preslo.ogg')))
			self.teach_syllable('images/syllables/ME.gif',self.load_sound(os.path.join(self.path,'audio/pres/presma.ogg')))

		if not (teach or test):
			image = pygame.image.load(os.path.join(self.path,'images/bg/bg_smiley.jpg'))
			self.draw(image)
			self.play_instruction('audio/instr/instr5.ogg',False)

			image = pygame.image.load(os.path.join(self.path,'images/bg/bg_landscape.jpg'))
			self.draw(image)
			self.play_instruction('audio/instr/instr6.ogg',False)

		if not teach:
			syllables = {'lo':6,'ma':6}
			syllable_sound = {}
			syllable_images = {}
			syllable_sound['ko'] = self.lo
			syllable_images['ko'] = {}
			syllable_images['ko']['l'] = pygame.image.load(os.path.join(self.path,'images/syllables/ko_left_trans.gif'))
			syllable_images['ko']['r'] = pygame.image.load(os.path.join(self.path,'images/syllables/ko_right_trans.gif'))
			syllable_sound['me'] = self.ma
			syllable_images['me'] = {}
			syllable_images['me']['l'] = pygame.image.load(os.path.join(self.path,'images/syllables/me_left_trans.gif'))
			syllable_images['me']['r'] = pygame.image.load(os.path.join(self.path,'images/syllables/me_right_trans.gif'))

			sprites = {}
			sprites['dog'] = {}
			sprites['dog']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_a/dog_l.gif'))
			sprites['dog']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_a/dog_r.gif'))
			sprites['duck'] = {}
			sprites['duck']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_a/duck_l.gif'))
			sprites['duck']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_a/duck_r.gif'))
			sprites['mouse'] = {}
			sprites['mouse']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_a/mouse_l.gif'))
			sprites['mouse']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_a/mouse_r.gif'))
			sprites['pig'] = {}
			sprites['pig']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_a/pig_l.gif'))
			sprites['pig']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_a/pig_r.gif'))

			bg_stage = pygame.image.load(os.path.join(self.path,'images/bg/bg_landscape_2.jpg'))

			log_a = Trail_Logger('test_a')
			stage = OneOutOfTwo(log_a,self.surface,bg_stage,sprites,syllables,syllable_images,syllable_sound,random_order=False,order=os.path.join(self.path,'data/modul_a'))

			miss = 0
			miss = stage.start(12)
			if miss > 2:
				if repitition == 0:
					miss = 0
					miss = stage.start(12)
					if miss > 2:
						log.add('A',res_teach,0)
						log.save()
						log_a.save()
						if rep:
							self.stop()
						else:
							self.end()
				else:
					log_a.save()
					log.add('A',res_teach,0)
					log.save()
					self.end()
			res_test = 1
			log_a.save()
						
		else:
			res_test = -1

		log.add('A',res_teach,res_test)
		log.save()

		if not (teach or test):
			image = pygame.image.load(os.path.join(self.path,'images/bg/bg_wave.jpg'))
			self.draw(image)
			self.play_instruction('audio/final/final1.ogg',False)


	def init_syllable_sound(self):
		self.lo = self.load_syllable_sound('ko')
		self.ma = self.load_syllable_sound('me')

class Stage_U(Stage):

	def __init__(self,log,teach=False,test=False,rep=False):
	   
		if teach or test:
			Stage.__init__(self,False)
		else:
			Stage.__init__(self,True)

		if not (teach and test):
			a = self.load_syllable_sound('a')
			i = self.load_syllable_sound('i')
			ko = self.load_syllable_sound('ko')
			me = self.load_syllable_sound('me')

	# TODO change instruction to instr7 with syllables and letters
		if not (teach or test):
			if rep:
				self.start('Modul C','audio/instr/instr9b.ogg')
			else:
				self.start('Modul U',self.get_path('audio/instr/instr9.ogg'))
			res_teach = -1
			self.teach_syllable('images/syllables/A.gif',self.load_sound(os.path.join(self.path,'audio/pres/preslo.ogg')))
			self.teach_syllable('images/syllables/I.gif',self.load_sound(os.path.join(self.path,'audio/pres/presma.ogg')))
			self.teach_syllable('images/syllables/KO.gif',self.load_sound(os.path.join(self.path,'audio/pres/preske.ogg')))
			self.teach_syllable('images/syllables/ME.gif',self.load_sound(os.path.join(self.path,'audio/pres/presbu.ogg')))

		res_teach = -1

		if not (test or teach):
			image = pygame.image.load(os.path.join(self.path,'images/bg/bg_underwater.gif'))
			self.draw(image)
			self.play_instruction('audio/instr/instr11b.ogg',False)

		if not teach:
			syllables = {'a':5,'i':5,'ko':4,'me':4}
			syllable_sound = {}
			syllable_images = {}
			syllable_sound['a'] = a
			syllable_images['a'] = {}
			syllable_images['a']['l'] = pygame.image.load(os.path.join(self.path,'images/syllables/a_uw_left.gif'))
			syllable_images['a']['r'] = pygame.image.load(os.path.join(self.path,'images/syllables/a_uw_right.gif'))
			syllable_sound['i'] = i
			syllable_images['i'] = {}
			syllable_images['i']['l'] = pygame.image.load(os.path.join(self.path,'images/syllables/i_uw_left.gif'))
			syllable_images['i']['r'] = pygame.image.load(os.path.join(self.path,'images/syllables/i_uw_right.gif'))
			syllable_sound['ko'] = ko
			syllable_images['ko'] = {}
			syllable_images['ko']['l'] = pygame.image.load(os.path.join(self.path,'images/syllables/ko_uw_left.gif'))
			syllable_images['ko']['r'] = pygame.image.load(os.path.join(self.path,'images/syllables/ko_uw_right.gif'))
			syllable_sound['me'] = me
			syllable_images['me'] = {}
			syllable_images['me']['l'] = pygame.image.load(os.path.join(self.path,'images/syllables/me_uw_left.gif'))
			syllable_images['me']['r'] = pygame.image.load(os.path.join(self.path,'images/syllables/me_uw_right.gif'))

			sprites = {}
			sprites['fish1'] = {}
			sprites['fish1']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_u/Delphin_R.gif'))
			sprites['fish1']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_u/Delphin_L.gif'))
			sprites['fish2'] = {}
			sprites['fish2']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_u/Fisch_blau_R.gif'))
			sprites['fish2']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_u/Fisch_blau_L.gif'))
			sprites['fish3'] = {}
			sprites['fish3']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_u/Fisch_orange_R.gif'))
			sprites['fish3']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_u/Fisch_orange_L.gif'))
			sprites['fish4'] = {}
			sprites['fish4']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_u/fisch_pink_R.gif'))
			sprites['fish4']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_u/fisch_pink_L.gif'))
			sprites['fish5'] = {}
			sprites['fish5']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_u/Fisch_tuerkis_R.gif'))
			sprites['fish5']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_u/Fisch_tuerkis_L.gif'))
			sprites['fish6'] = {}
			sprites['fish6']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_u/Hai_R.gif'))
			sprites['fish6']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_u/Hai_L.gif'))

			bg_stage = pygame.image.load(os.path.join(self.path,'images/bg/bg_underwater.gif'))
			
			log_u = Trail_Logger('test_u')
			stage = OneOutOfTwo(log_u,self.surface,bg_stage,sprites,syllables,syllable_images,syllable_sound,random_order=False,order=os.path.join(self.path,'data/modul_u'))
			miss = 0
			miss = stage.start(15)
			if miss > 4 and not test:
				miss = 0
				miss = stage.start(15)
				if miss > 4:
					log_u.save()
					if rep:
						log.add('U',res_teach,0)
						log.save()
						self.stop()
					else:
						log.add('U',res_teach,0)
						log.save()
						f.end()
			res_test = 1
			log_u.save()
		else:
			res_test = -1

		log.add('U',res_teach,res_test)
		log.save()
		
		if not (teach or test):
			image = pygame.image.load(os.path.join(self.path,'images/bg/bg_wave.jpg'))
			self.draw(image)
			self.play_instruction('audio/final/final1.ogg',False)
 

class Stage_F(Stage):

	def __init__(self,log,teach=False,test=False,rep=False):
		
		if teach or test:
			Stage.__init__(self,False)
		else:
			Stage.__init__(self,True)

		if not (teach and test):
			a = self.load_syllable_sound('a')
			i = self.load_syllable_sound('i')
		#	ke = self.load_syllable_sound('ke')

		if not rep:
			if not (teach or test):
				self.start('Modul F','audio/instr/instr9b.ogg')

				self.teach_syllable(self.get_path('images/syllables/A.gif'),self.load_sound(self.get_path('audio/pres/preske.ogg')))
				self.play_instruction(self.get_path('audio/instr/instr2.ogg'))
				self.teach_syllable(self.get_path('images/syllables/A.gif'),a['1'])
				self.play_instruction('audio/instr/instr3.ogg')

			if not test:
				miss = 0
				miss = self.test_syllable('a',a,8)
				if miss > 2 and not teach:
					miss = 0
					self.play_instruction('audio/instr/instr3.ogg')
					miss = self.test_syllable('a',a,8)
					if miss > 2:
						log.add('F',0,-1)
						log.save()
						self.stop()
				res_teach = 1
			else:
				res_teach = -1

			if not (teach or test):
				self.play_instruction('audio/instr/instr4.ogg')

				self.teach_syllable(self.get_path('images/syllables/I.gif'),self.load_sound(self.get_path('audio/pres/preske.ogg')))
				self.play_instruction(self.get_path('audio/instr/instr2.ogg'))
				self.teach_syllable(self.get_path('images/syllables/I.gif'),i['1'])
				self.play_instruction('audio/instr/instr3.ogg')

			if not test:
				miss = 0
				miss = self.test_syllable('i',i,8)
				if miss > 2 and not teach:
					miss = 0
					self.play_instruction('audio/instr/instr3.ogg')
					miss = self.test_syllable('i',i,8)
					if miss > 2:
						log.add('F',0,-1)
						log.save()
						self.stop()
				res_teach = 1
			else:
				res_teach = -1

#			if not (teach or test):
#				self.play_instruction('audio/misc/repeat.ogg')
#				self.teach_syllable('images/syllables/LO.gif',self.load_sound(self.get_path('audio/pres/preslo.ogg')))
#				self.teach_syllable('images/syllables/MA.gif',self.load_sound(self.get_path('audio/pres/presma.ogg')))
		else:
			res_teach = -1
			self.start('Modul S',self.get_path('audio/instr/instr7b.ogg'))
			miss_teach = -1
			self.teach_syllable(self.get_path('images/syllables/A.gif'),self.load_sound(self.get_path('audio/pres/preslo.ogg')))
			self.teach_syllable(self.get_path('images/syllables/I.gif'),self.load_sound(self.get_path('audio/pres/presma.ogg')))

		if not teach:
			syllables = {'a':6, 'i':6}
			syllable_sound = {}
			syllable_sound['a'] = a
			syllable_sound['i'] = i

			sprites = {}
			sprites['a'] = pygame.image.load(self.get_path('images/stage_f/ufoa.gif'))
			sprites['i'] = pygame.image.load(self.get_path('images/stage_f/ufoi.gif'))

			bg_stage = pygame.image.load(self.get_path('images/bg/bg_space.gif'))

		if not (teach or test):
			self.draw(bg_stage)
			self.play_instruction('audio/instr/instr10.ogg',False)

		if not teach:
			log_f = Trail_Logger('test_f')
			stage = Space_Engine(log_f,self.surface,bg_stage,syllables,syllable_sound,sprites,self.get_path('data/modul_f'))
			miss = stage.start()
			if miss > 2 and not test:
				miss = stage.start()
				if miss > 2:
					log_f.save()
					if rep:
						log.add('F',res_teach,0)
						log.save()
						self.stop()
					else:
						log.add('U',res_teach,0)
						log.save()
						self.end()
			res_test = 1
			log_f.save()
		else:
			res_test = -1

		log.add('F',res_teach,res_test)
		log.save()

		if not (teach or test):
			image = pygame.image.load(os.path.join(self.path,'images/bg/bg_wave.jpg'))
			self.draw(image)
			self.play_instruction('audio/final/final1.ogg',False)


class Stage_Q(Stage):
	
	def __init__(self,log,teach=False,test=False,repeat=False):

		if teach or test:
			#super(Stage_Q,self).__init__(self,False)
			Stage.__init__(self,False)
		else:
			#super(Stage_Q,self).__init__(self,True)
			Stage.__init__(self,True)
		
		a = self.load_syllable_sound('a')
		i = self.load_syllable_sound('i')
		o = self.load_syllable_sound('o')
		fa = self.load_syllable_sound('fa')
		ri = self.load_syllable_sound('ri')
		me = self.load_syllable_sound('me')
		ko = self.load_syllable_sound('ko')

		if not repeat:
			if not (teach or test):
				self.start('Modul Q','audio/instr/instr9.ogg')

				self.teach_syllable(self.get_path('images/syllables/FA.gif'),self.load_sound(self.get_path('audio/pres/presti.ogg')))
				self.play_instruction(self.get_path('audio/instr/instr2.ogg'))
				self.teach_syllable(self.get_path('images/syllables/FA.gif'),fa['1'])
				self.play_instruction('audio/instr/instr3.ogg')

			if not test:
				miss = self.test_syllable('fa',fa,8)
				if miss > 2 and not teach:
					miss = self.test_syllable('fa',fa,8)
					if miss > 2:
						log.add('Q',0,-1)
						los.save()
						self.stop()
				res_teach = 1
			else:
				res_teach = -1

			if not (teach or test):
				self.play_instruction('audio/misc/repeat.ogg')
				self.teach_syllable(self.get_path('images/syllables/A.gif'),self.load_sound(self.get_path('audio/pres/preslo.ogg')))
				self.teach_syllable(self.get_path('images/syllables/I.gif'),self.load_sound(self.get_path('audio/pres/presma.ogg')))
				self.teach_syllable(self.get_path('images/syllables/O.gif'),self.load_sound(self.get_path('audio/pres/preske.ogg')))
				self.teach_syllable(self.get_path('images/syllables/ME.gif'),self.load_sound(self.get_path('audio/pres/presbu.ogg')))
				self.teach_syllable(self.get_path('images/syllables/KO.gif'),self.load_sound(self.get_path('audio/pres/presbu.ogg')))
				self.teach_syllable(self.get_path('images/syllables/RI.gif'),self.load_sound(self.get_path('audio/pres/presbu.ogg')))

		else:
			self.start('Modul K',self.get_path('audio/instr/instr7.ogg'))
			res_teach = -1
			miss_teach = -1
			self.teach_syllable(self.get_path('images/syllables/A.gif'),self.load_sound(self.get_path('audio/pres/preslo.ogg')))
			self.teach_syllable(self.get_path('images/syllables/I.gif'),self.load_sound(self.get_path('audio/pres/presma.ogg')))
			self.teach_syllable(self.get_path('images/syllables/O.gif'),self.load_sound(self.get_path('audio/pres/preske.ogg')))
			self.teach_syllable(self.get_path('images/syllables/ME.gif'),self.load_sound(self.get_path('audio/pres/presbu.ogg')))
			self.teach_syllable(self.get_path('images/syllables/KO.gif'),self.load_sound(self.get_path('audio/pres/presbu.ogg')))
			self.teach_syllable(self.get_path('images/syllables/RI.gif'),self.load_sound(self.get_path('audio/pres/presbu.ogg')))
			self.teach_syllable(self.get_path('images/syllables/FA.gif'),self.load_sound(self.get_path('audio/pres/presti.ogg')))


		if not teach:

			syllables = {'a':2,'i':2,'o':3,'me':2,'ko':2,'ri':2,'fa':5}
			syllable_sound = {}
			syllable_sound['a'] = a
			syllable_sound['i'] = i
			syllable_sound['o'] = o
			syllable_sound['me'] = me
			syllable_sound['ko'] = ko
			syllable_sound['ri'] = ri
			syllable_sound['fa'] = fa

			sprites = {}
			sprites['a'] = self.load_sprites('a')
			sprites['i'] = self.load_sprites('i')
			sprites['o'] = self.load_sprites('o')
			sprites['me'] = self.load_sprites('me')
			sprites['ko'] = self.load_sprites('ko')
			sprites['ri'] = self.load_sprites('ri')
			sprites['fa'] = self.load_sprites('fa')

			bg_stage = pygame.image.load(self.get_path('images/bg/bg_sky2.gif'))

		if not (teach or test):
			self.draw(bg_stage)
			self.play_instruction('audio/instr/instr12b.ogg',False)

		if not teach:
			log_q = Trail_Logger('test_q')
			stage = Balloon_Engine(log_q,self.surface,bg_stage,syllables,syllable_sound,sprites,self.get_path('data/modul_q'))
			miss = stage.start()
			if miss > 4:
				miss = stage.start()
				if miss > 4:
					log.add('Q',res_teach,0)
					log.save()
					log_q.save()
					if rep:
						self.stop()
					else:
						self.end()
			log_q.save()
			res_test = 1
		else:
			res_test = -1

		log.add('Q',res_teach,res_test)
		log.save()

		if not (teach or test):
			self.draw(pygame.image.load(os.path.join(self.path,'images/bg/bg_wave.jpg')))
			self.play_instruction('audio/final/final1.ogg',False)

	def load_sprites(self,t):

		ret = {}
		ret['g'] = pygame.image.load(self.get_path('images/stage_q/'+t+'_g.gif'))
		ret['r'] = pygame.image.load(self.get_path('images/stage_q/'+t+'_r.gif'))
		ret['y'] = pygame.image.load(self.get_path('images/stage_q/'+t+'_y.gif'))
		return ret



class Stage_P(Stage):

	def __init__(self, log, teach=False, test=False, rep=False):
		
		if teach or test:
			Stage.__init__(self,False)
		else:
			Stage.__init__(self,True)

		if not (teach and test):
			a = self.load_syllable_sound('a')
			i = self.load_syllable_sound('i')
			ko = self.load_syllable_sound('ko')
			me = self.load_syllable_sound('me')
			ri = self.load_syllable_sound('ri')

		if not rep:
			if not (teach or test):
				self.start('Modul P','audio/instr/instr9.ogg')
				self.teach_syllable('images/syllables/RI.gif',self.load_sound(os.path.join(self.path,'audio/pres/preslo.ogg')))
				self.play_instruction('audio/instr/instr2.ogg')
				self.teach_syllable('images/syllables/RI.gif',ri['1'])
				self.play_instruction('audio/instr/instr3.ogg')

			if not test:
				miss = self.test_syllable('ri',ri,8)
				if miss > 2:
					miss = self.test_syllable('ri',ri,8)
					if miss > 2:
						log.add('P',0,-1)
						log.save()
						self.stop()
				res_teach = 1
			else:
				res_teach = -1
		
			if not (teach or test):
				self.play_instruction('audio/misc/repeat.ogg')

		else:

			#TODO change instr7 to instruction for syllables and letters
			self.start('Modul I','audio/instr/instr7.ogg')
			self.teach_syllable('images/syllables/RI.gif',self.load_sound(os.path.join(self.path,'audio/pres/preslo.ogg')))

		if not (teach or test):
			self.teach_syllable('images/syllables/A.gif',self.load_sound(os.path.join(self.path,'audio/pres/preslo.ogg')))
			self.teach_syllable('images/syllables/I.gif',self.load_sound(os.path.join(self.path,'audio/pres/preslo.ogg')))
			self.teach_syllable('images/syllables/ME.gif',self.load_sound(os.path.join(self.path,'audio/pres/preslo.ogg')))
			self.teach_syllable('images/syllables/KO.gif',self.load_sound(os.path.join(self.path,'audio/pres/preslo.ogg')))

			self.draw(pygame.image.load(os.path.join(self.path,'images/bg/bg_smiley.jpg')))
			self.play_instruction('audio/instr/instr14.ogg',False)

		if not teach:

			syllable_sound = {}
			sprites = {}
			miss = {}

			syllable_sound['a'] = a
			syllable_sound['i'] = i
			syllable_sound['me'] = me
			syllable_sound['ko'] = ko
			syllable_sound['ri'] = ri

			miss['a'] = self.load_sound(os.path.join(self.path,'audio/syllables/amiss.ogg'))
			miss['i'] = self.load_sound(os.path.join(self.path,'audio/syllables/imiss.ogg'))
			miss['ko'] = self.load_sound(os.path.join(self.path,'audio/syllables/komiss.ogg'))
			miss['me'] = self.load_sound(os.path.join(self.path,'audio/syllables/memiss.ogg'))
			miss['ri'] = self.load_sound(os.path.join(self.path,'audio/syllables/rimiss.ogg'))


			sprites['a'] = {}
			sprites['a']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_p/airplane_l_a.gif'))
			sprites['a']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_p/airplane_r_a.gif'))
			sprites['i'] = {}
			sprites['i']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_p/airplane_l_i.gif'))
			sprites['i']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_p/airplane_r_i.gif'))
			sprites['ko'] = {}
			sprites['ko']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_p/airplane_l_ko.gif'))
			sprites['ko']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_p/airplane_r_ko.gif'))
			sprites['me'] = {}
			sprites['me']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_p/airplane_l_me.gif'))
			sprites['me']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_p/airplane_r_me.gif'))
			sprites['ri'] = {}
			sprites['ri']['l'] = pygame.image.load(os.path.join(self.path,'images/stage_p/airplane_l_ri.gif'))
			sprites['ri']['r'] = pygame.image.load(os.path.join(self.path,'images/stage_p/airplane_r_ri.gif'))

			bg_stage = pygame.image.load(os.path.join(self.path,'images/bg/bg_airplanes.gif'))
			log_p = Trail_Logger('test_p')

			stage = CatchMeIfYouCan(log_p,self.surface,bg_stage,syllable_sound,miss,sprites,order=os.path.join(self.path,'data/modul_p'))

			if not test:
				stage.play_instruction(self.load_sound(os.path.join(self.path,'audio/instr/instr15.ogg')),self.load_sound(os.path.join(self.path,'audio/instr/instr16.ogg')),pygame.image.load(os.path.join(self.path,'images/stage_p/instr_image1.gif')))

			miss = stage.start()
			if miss > 4:
				miss = stage.start()
				if miss > 4:
					log.add('P',res_teach,0)
					log.save()
					log_p.save()
					if rep:
						self.stop()
					else:
						self.end()
			log_p.save()
			res_test = 1
		else:
			res_test = -1

		log.add('P',res_teach,res_test)
		log.save()

		if not (teach or test):
			self.draw(pygame.image.load(os.path.join(self.path,'images/bg/bg_wave.jpg')))
			self.play_instruciton('audio/final/final1.ogg',False)

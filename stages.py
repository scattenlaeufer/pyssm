# -*- coding: utf-8 -*-

import pygame, sys, random
from pygame.locals import *
from engines import OneOutOfTwo
from helpers import Log_Handler


#generic form of a stage. all actual stages should inherit from this

class Stage:

    def __init__(self,bla=True):
        
        self.miss = 0
        self.mainClock = pygame.time.Clock()

        # init pygame
        pygame.init()

        # set window
        self.windowwidth = 1024
        self.windowheight = 768
        self.curser_unvisible = False
#        info = pygame.display.Info()
#        self.desktopwidth = info.current_w
#        self.desktopheight = info.current_h
#        print(str(self.desktopwidth)+' '+str(self.desktopheight))
        self.surface = pygame.display.set_mode((self.windowwidth,self.windowheight),0,32)
        pygame.display.set_caption('SSM Test v0.1') 

        self.bg_blank = (194,194,194)
        self.surface.fill(self.bg_blank)
        self.font1 = pygame.font.Font(None,70)
        if bla:
            self.text = self.font1.render('Willkommen zum Silbenlernspiel',True,(0,0,0))
            self.surface.blit(self.text,(self.position_center_width(self.text),100))

    def toggle_fullsreen(self):
        
        pygame.display.toggle_fullscreen()
        self.curser_unvisible = pygame.mouse.set_visible(self.curser_unvisible)
        
#        if self.curser_unvisible:
#            self.windowwidth = self.desktopwidth
#            self.windowheight = self.desktopheight
#        else:
#            self.windowwidth = 1024
#            self.windowheight = 768

#        self.surface = pygame.transform.scale(self.surface,(self.windowwidth,self.windowheight))
#        pygame.display.update()


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
        
        dic['1'] = self.load_sound('audio/syllable/'+syllable+'1.ogg')
        dic['2'] = self.load_sound('audio/syllable/'+syllable+'2.ogg')
        dic['3'] = self.load_sound('audio/syllable/'+syllable+'3.ogg')
        
        dic['miss'] = self.load_sound('audio/syllable/'+syllable+'miss.ogg')
        
        dic['neg1'] = self.load_sound('audio/syllable/'+syllable+'neg1.ogg')
        dic['neg2'] = self.load_sound('audio/syllable/'+syllable+'neg2.ogg')
        
        dic['pos1'] = self.load_sound('audio/syllable/'+syllable+'pos1.ogg')
        dic['pos2'] = self.load_sound('audio/syllable/'+syllable+'pos2.ogg')
        dic['pos3'] = self.load_sound('audio/syllable/'+syllable+'pos3.ogg')
        dic['pos4'] = self.load_sound('audio/syllable/'+syllable+'pos4.ogg')
        
        return dic

    
    def play_instruction(self,instr,clean=True):

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

        im = pygame.image.load(image)
        self.surface.blit(im,(self.position_center_width(im),self.position_center_height(im)))
        pygame.display.update()
        pygame.time.wait(3000)
        self.watch_keypress()

    def transform_height(self,item,width):

        x = item.get_size()[0]
        y = item.get_size()[1]
        ratio = float(y)/float(x)
        return int(width * ratio)


    def test_syllable(self,syllable,dic,n=6):

        miss = 0
        for i in range(n):
            self.surface.fill(self.bg_blank)
            correct = random.randint(1,2)

            image = pygame.image.load('images/syllables/'+syllable.upper()+'.gif')
            dimension = (self.windowwidth/3,self.transform_height(image,self.windowwidth/3))
            image = pygame.transform.scale(image,dimension)

            distr = pygame.image.load('images/distr/DISTR'+str(random.randint(1,10))+'.gif')
            distr = pygame.transform.scale(distr,dimension)
            
            if correct == 1:
                self.draw_left(image)
                self.draw_right(distr)
            else:
                self.draw_left(distr)
                self.draw_right(image)

            pygame.display.update()
            dic[str(random.randint(1,3))].play()

            key_pressed = False
            press = 0

            while True:
                for event in pygame.event.get():
                    self.standart_event(event)

                    if event.type == KEYDOWN:
                        if event.key == ord('u'):
                            press = 1
                            key_pressed = True
                        if event.key == ord('d'):
                            press = 2
                            key_pressed = True

                if press == correct and key_pressed:
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
                    pygame.event.clear()

                self.mainClock.tick(40)

        return miss



class Stage_A(Stage):

    def __init__(self,log,teach=False,test=False):
       
        if teach or test:
            Stage.__init__(self,False)
        else:
            Stage.__init__(self,True)

        #load sounds
        if not (teach and test):
            lo = self.load_syllable_sound('lo')
            ma = self.load_syllable_sound('ma')

        if not (teach or test):
            #edit title for modul A
            self.start('Modul A','audio/instr/instr1.ogg')

            #teach and test LO
            self.teach_syllable('images/syllables/LO.gif',self.load_sound('audio/pres/preslo.ogg'))
            self.play_instruction('audio/instr/instr2.ogg')
            self.teach_syllable('images/syllables/LO.gif',lo['1'])
            
            self.play_instruction('audio/instr/instr3.ogg')

        if not test:
            miss_teach = self.test_syllable('lo',lo,6)
        
        if not (teach or test):
            #teach and test MA
            self.play_instruction('audio/instr/instr4.ogg')

            self.teach_syllable('images/syllables/MA.gif',self.load_sound('audio/pres/presma.ogg'))
            self.play_instruction('audio/instr/instr2.ogg')
            self.teach_syllable('images/syllables/MA.gif',ma['1'])

            self.play_instruction('audio/instr/instr3.ogg')

        if not test:
            miss_teach += self.test_syllable('ma',ma,6)
        else:
            miss_teach = -1

        if not (teach or test):
            image = pygame.image.load('images/bg/bg_smiley.jpg')
            self.draw(image)
            self.play_instruction('audio/instr/instr5.ogg',False)

            image = pygame.image.load('images/bg/bg_landscape.jpg')
            self.draw(image)
            self.play_instruction('audio/instr/instr6.ogg',False)

        if not teach:
            syllables = {'lo':6,'ma':6}
            syllable_sound = {}
            syllable_images = {}
            syllable_sound['lo'] = lo
            syllable_images['lo'] = {}
            syllable_images['lo']['l'] = pygame.image.load('images/syllables/lo_left_trans.gif')
            syllable_images['lo']['r'] = pygame.image.load('images/syllables/lo_right_trans.gif')        
            syllable_sound['ma'] = ma
            syllable_images['ma'] = {}
            syllable_images['ma']['l'] = pygame.image.load('images/syllables/ma_left_trans.gif')
            syllable_images['ma']['r'] = pygame.image.load('images/syllables/ma_right_trans.gif')

            sprites = {}
            sprites['dog'] = {}
            sprites['dog']['l'] = pygame.image.load('images/stage_a/dog_l.gif')
            sprites['dog']['r'] = pygame.image.load('images/stage_a/dog_r.gif')
            sprites['duck'] = {}
            sprites['duck']['l'] = pygame.image.load('images/stage_a/duck_l.gif')
            sprites['duck']['r'] = pygame.image.load('images/stage_a/duck_r.gif')
            sprites['mouse'] = {}
            sprites['mouse']['l'] = pygame.image.load('images/stage_a/mouse_l.gif')
            sprites['mouse']['r'] = pygame.image.load('images/stage_a/mouse_r.gif')
            sprites['pig'] = {}
            sprites['pig']['l'] = pygame.image.load('images/stage_a/pig_l.gif')
            sprites['pig']['r'] = pygame.image.load('images/stage_a/pig_r.gif')

            bg_stage = pygame.image.load('images/bg/bg_landscape.jpg')
            
            stage = OneOutOfTwo(self.surface,bg_stage,sprites,syllables,syllable_images,syllable_sound)
            miss_test = stage.start(12)
        else:
            miss_test = -1

        log.add('A',miss_teach,miss_test)

        if not (teach or test):
            image = pygame.image.load('images/bg/bg_wave.jpg')
            self.draw(image)
            self.play_instruction('audio/final/final1.ogg',False)


class Stage_U(Stage):

    def __init__(self,log,teach=False,test=False):
       
        if teach or test:
            Stage.__init__(self,False)
        else:
            Stage.__init__(self,True)

        if not (teach and test):
            lo = self.load_syllable_sound('lo')
            ma = self.load_syllable_sound('ma')
            ke = self.load_syllable_sound('ke')
            bu = self.load_syllable_sound('bu')

        if not (teach or test):
            self.start('Modul U','audio/instr/instr9.ogg')

            self.teach_syllable('images/syllables/BU.gif',self.load_sound('audio/pres/presbu.ogg'))
            self.play_instruction('audio/instr/instr2.ogg')
            self.teach_syllable('images/syllables/BU.gif',bu['1'])
            self.play_instruction('audio/instr/instr3.ogg')

        if not test:
            miss_teach = self.test_syllable('bu',bu,6)
        else:
            miss_teach = -1

        if not (test or teach):
            image = pygame.image.load('images/bg/underwater.gif')
            self.draw(image)
            self.play_instruction('audio/instr/instr11.ogg',False)

        if not teach:
            syllables = {'lo':3,'ma':3,'ke':4,'bu':5}
            syllable_sound = {}
            syllable_images = {}
            syllable_sound['lo'] = lo
            syllable_images['lo'] = {}
            syllable_images['lo']['l'] = pygame.image.load('images/stage_u/lo_left_trans.gif')
            syllable_images['lo']['r'] = pygame.image.load('images/stage_u/lo_right_trans.gif')        
            syllable_sound['ma'] = ma
            syllable_images['ma'] = {}
            syllable_images['ma']['l'] = pygame.image.load('images/stage_u/ma_left_trans.gif')
            syllable_images['ma']['r'] = pygame.image.load('images/stage_u/ma_right_trans.gif')
            syllable_sound['ke'] = ke
            syllable_images['ke'] = {}
            syllable_images['ke']['l'] = pygame.image.load('images/stage_u/ke_left_trans.gif')
            syllable_images['ke']['r'] = pygame.image.load('images/stage_u/ke_right_trans.gif')
            syllable_sound['bu'] = bu
            syllable_images['bu'] = {}
            syllable_images['bu']['l'] = pygame.image.load('images/stage_u/bu_left_trans.gif')
            syllable_images['bu']['r'] = pygame.image.load('images/stage_u/bu_right_trans.gif')

            sprites = {}
            sprites['f1'] = {}
            sprites['f1']['r'] = pygame.image.load('images/stage_u/fish1_R.gif')
            sprites['f1']['l'] = pygame.image.load('images/stage_u/fish1_L.gif')
            sprites['f2'] = {}
            sprites['f2']['r'] = pygame.image.load('images/stage_u/fish2_R.gif')
            sprites['f2']['l'] = pygame.image.load('images/stage_u/fish2_L.gif')
            sprites['f3'] = {}
            sprites['f3']['r'] = pygame.image.load('images/stage_u/fish3_R.gif')
            sprites['f3']['l'] = pygame.image.load('images/stage_u/fish3_L.gif')
            sprites['f4'] = {}
            sprites['f4']['r'] = pygame.image.load('images/stage_u/fish4_R.gif')
            sprites['f4']['l'] = pygame.image.load('images/stage_u/fish4_L.gif')
            sprites['f5'] = {}
            sprites['f5']['r'] = pygame.image.load('images/stage_u/fish5_R.gif')
            sprites['f5']['l'] = pygame.image.load('images/stage_u/fish5_L.gif')
            sprites['f6'] = {}
            sprites['f6']['r'] = pygame.image.load('images/stage_u/fish6_R.gif')
            sprites['f6']['l'] = pygame.image.load('images/stage_u/fish6_L.gif')

            bg_stage = pygame.image.load('images/bg/underwater.gif')
            
            stage = OneOutOfTwo(self.surface,bg_stage,sprites,syllables,syllable_images,syllable_sound)
            miss_test = stage.start(15)
        else:
            miss_test = -1

        log.add('U',miss_teach,miss_test)
        
        if not (teach or test):
            image = pygame.image.load('images/bg/bg_wave.jpg')
            self.draw(image)
            self.play_instruction('audio/final/final1.ogg',False)

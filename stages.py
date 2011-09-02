# -*- coding: utf-8 -*-

import pygame, sys, random
from pygame.locals import *
from engines import OneOutOfTwo


#generic form of a stage. all actual stages should inherit from this

class Stage:

    def __init__(self):
        
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

        self.text = self.font1.render('Willkommen zum Silbenlehrnspiel',True,(0,0,0))
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

    def __init__(self):

        Stage.__init__(self)

        #load sounds
        self.lo = self.load_syllable_sound('lo')
        self.ma = self.load_syllable_sound('ma')

        #edit title for modul A
        self.text = self.font1.render('Modul A',True,(0,0,0))
        self.surface.blit(self.text,(self.position_center_width(self.text),250))
        pygame.display.update()

        self.play_instruction('audio/instr/instr1.ogg',False)

        self.text = self.font1.render(u'bitte Enter-Taste drücken',True,(0,0,0))
        self.surface.blit(self.text,(self.position_center_width(self.text),400))
        pygame.display.update()

        bla = True

        while bla:
            for event in pygame.event.get():
                self.standart_event(event)
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        bla = False

            self.mainClock.tick(20)

        #teach and test LO
        self.teach_syllable('images/syllables/LO.gif',self.load_sound('audio/pres/preslo.ogg'))
        self.play_instruction('audio/instr/instr2.ogg')
        self.teach_syllable('images/syllables/LO.gif',self.lo['1'])
        
        self.play_instruction('audio/instr/instr3.ogg')
        self.test_syllable('lo',self.lo,1)

        #teach and test MA
        self.play_instruction('audio/instr/instr4.ogg')

        self.teach_syllable('images/syllables/MA.gif',self.load_sound('audio/pres/presma.ogg'))
        self.play_instruction('audio/instr/instr2.ogg')
        self.teach_syllable('images/syllables/MA.gif',self.ma['1'])

        self.play_instruction('audio/instr/instr3.ogg')
        self.test_syllable('ma',self.ma,1)
   
#        print self.miss

        image = pygame.image.load('images/bg/bg_smiley.jpg')
        self.draw(image)
        self.play_instruction('audio/instr/instr5.ogg',False)

        image = pygame.image.load('images/bg/bg_landscape.jpg')
        self.draw(image)
        self.play_instruction('audio/instr/instr6.ogg',False)

        syllables = ['lo','ma']
        syllable_sound = {}
        syllable_images = {}
        syllable_sound['lo'] = self.lo
        syllable_images['lo'] = {}
        syllable_images['lo']['l'] = pygame.image.load('images/syllables/lo_left_trans.gif')
        syllable_images['lo']['r'] = pygame.image.load('images/syllables/lo_right_trans.gif')        
        syllable_sound['ma'] = self.ma
        syllable_images['ma'] = {}
        syllable_images['ma']['l'] = pygame.image.load('images/syllables/ma_left_trans.gif')
        syllable_images['ma']['r'] = pygame.image.load('images/syllables/ma_right_trans.gif')

        sprites = {}
        sprites['dog'] = {}
            #the l or r in the file name describe the viewing direciton, but i want the 
            #sprite, which looks right at the left site
        sprites['dog']['r'] = pygame.image.load('images/stage_a/dog_l.gif')
        sprites['dog']['l'] = pygame.image.load('images/stage_a/dog_r.gif')
        sprites['duck'] = {}
        sprites['duck']['r'] = pygame.image.load('images/stage_a/duck_l.gif')
        sprites['duck']['l'] = pygame.image.load('images/stage_a/duck_r.gif')
        sprites['mouse'] = {}
        sprites['mouse']['r'] = pygame.image.load('images/stage_a/mouse_l.gif')
        sprites['mouse']['l'] = pygame.image.load('images/stage_a/mouse_r.gif')
        sprites['pig'] = {}
        sprites['pig']['r'] = pygame.image.load('images/stage_a/pig_l.gif')
        sprites['pig']['l'] = pygame.image.load('images/stage_a/pig_r.gif')

        bg_stage = pygame.image.load('images/bg/bg_landscape.jpg')
        
        stage = OneOutOfTwo(self.surface,bg_stage,sprites,syllables,syllable_images,syllable_sound)
        print(stage.start())

        image = pygame.image.load('images/bg/bg_wave.jpg')
        self.draw(image)
        self.play_instruction('audio/final/final1.ogg',False)



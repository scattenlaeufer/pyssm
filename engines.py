# -*- coding: utf-8 -*-
import pygame, random, sys
from pygame.locals import *

class Engine:

    def __init__(self, surface, bg, random_order, order):
        self.miss = 0
        self.frames = 40
        self.surface = surface
        self.bg = bg
        self.random_order = random_order
        self.order = order
        self.mainClock = pygame.time.Clock()


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


    def draw_sprite_left(self,sprite):

        self.surface.blit(sprite,(0,self.surface.get_size()[1]-sprite.get_size()[1]))


    def draw_sprite_right(self,sprite):

        self.surface.blit(sprite,(self.surface.get_size()[0]-sprite.get_size()[0],self.surface.get_size()[1]-sprite.get_size()[1]))

    
    def draw_syllable_left(self,syllable):

        self.surface.blit(syllable,(50,300))


    def draw_syllable_right(self,syllable):

        self.surface.blit(syllable,(self.surface.get_size()[0]-syllable.get_size()[0]-50,300))


    def choose_two(self,source):

        out1 = random.randint(0,source-1)
        out2 = random.randint(0,source-2)

        if out1 <= out2:
            out2 = out2 + 1

        return (out1,out2)


class OneOutOfTwo(Engine):

    def __init__(self, surface, bg, sprites, syllables, syllable_images, syllable_sounds, random_order=True, order=None, neo=True):
        
        Engine.__init__(self,surface,bg,random_order,order)
        self.sprites = sprites
        self.syllable_images = syllable_images
        self.syllables = syllables
        self.syllable_sounds = syllable_sounds
        self.n_syllables = len(self.syllables)
        self.n_sprites = len(self.sprites)
        if neo:
            self.left = u'xvlcwuiaeoüöäpzXVLCWUIAEOÜÖÄPZ'
            self.right = u'khgfqßsnrtdybm,.jKHGFQẞSNRTDYBM–•J'
        else:
            self.left = u'qwertasdfgyxcvbQWERTASDFGYXCVB'
            self.right = u'zuiopühjklöänmm,.-ZUIOPÜHJKLÖÄNM'


    def start(self,n=10):

        for i in range(n):
            size = self.surface.get_size()
            self.bg = pygame.transform.scale(self.bg,size)
            self.surface.blit(self.bg,(0,0))

            correct = random.randint(0,1)
            sprite = self.choose_two(self.n_sprites)
            syllable = self.choose_two(self.n_syllables)

            self.draw_sprite_left(self.sprites[self.sprites.keys()[sprite[0]]]['l'])
            self.draw_sprite_right(self.sprites[self.sprites.keys()[sprite[1]]]['r'])
            self.draw_syllable_left(self.syllable_images[self.syllables[syllable[0]]]['l'])
            self.draw_syllable_right(self.syllable_images[self.syllables[syllable[1]]]['r'])
            pygame.display.update()

            self.syllable_sounds[self.syllables[syllable[correct]]][str(random.randint(1,3))].play()

            key_pressed = False
            press = 0

            while True:

                for event in pygame.event.get():
                    self.standart_event(event)
                    if event.type == KEYDOWN:
                        try:
                            if self.left.find(chr(event.key))>= 0:
                                press = 0
                                key_pressed = True
                            if self.right.find(chr(event.key)) >=0:
                                press = 1
                                key_pressed = True
                        except UnicodeDecodeError:
                            print(event.key)

                
                if press == correct and key_pressed:
                    self.syllable_sounds[self.syllables[syllable[correct]]]['pos'+str(random.randint(1,4))].play()
                    self.surface.blit(self.bg,(0,0))
                    self.draw_sprite_left(self.sprites[self.sprites.keys()[sprite[0]]]['l'])
                    self.draw_sprite_right(self.sprites[self.sprites.keys()[sprite[1]]]['r'])
                    if correct == 0:
                        self.draw_syllable_left(self.syllable_images[self.syllables[syllable[0]]]['l'])
                    else:
                        self.draw_syllable_right(self.syllable_images[self.syllables[syllable[1]]]['r'])
                    pygame.display.update()
                    pygame.time.wait(3700)
                    pygame.event.clear()
                    break

                if press != correct and key_pressed:
                    key_pressed = False
                    self.syllable_sounds[self.syllables[syllable[correct]]]['neg'+str(random.randint(1,2))].play() 
                    self.surface.blit(self.bg,(0,0))
                    self.draw_sprite_left(self.sprites[self.sprites.keys()[sprite[0]]]['l'])
                    self.draw_sprite_right(self.sprites[self.sprites.keys()[sprite[1]]]['r'])
                    if correct == 0:
                        self.draw_syllable_left(self.syllable_images[self.syllables[syllable[0]]]['l'])
                    else:
                        self.draw_syllable_right(self.syllable_images[self.syllables[syllable[1]]]['r'])
                    pygame.display.update()
                    pygame.time.wait(4500)
                    self.miss += 1
                    
                    if correct == 0:
                        self.draw_syllable_right(self.syllable_images[self.syllables[syllable[1]]]['r'])
                    else:
                        self.draw_syllable_left(self.syllable_images[self.syllables[syllable[0]]]['l'])
                    pygame.display.update()
                    self.syllable_sounds[self.syllables[syllable[correct]]][str(random.randint(1,3))].play()
                    pygame.event.clear()

                self.mainClock.tick(40)

        return self.miss




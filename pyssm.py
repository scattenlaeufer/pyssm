#!/usr/bin/python2
# -*- coding: utf-8 -*-
import pygame, sys, time
from helpers import Log_Handler
from pygame.locals import *
from stages import Stage_A

print('ssm training version 0.1\nwirtten by Björn Guth')

#load stage
#stage = Stage_A()


log = Log_Handler()
stage = Stage_A(log)
print(log)

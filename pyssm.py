#!/usr/bin/python2
# -*- coding: utf-8 -*-
import pygame, sys, time
from helpers.log import Log_Handler
from pygame.locals import *
from level.stages import Stage_A, Stage_U, Stage_F

print(u'ssm training version 0.1\nwirtten by Björn Guth')

def normal(teach,test):
	result = log.analyze()
	if result[0] == '0':
		stage = Stage_A(log,teach,test)
	else:
		if result[0] == 'A':
			if result[1]:
				stage = Stage_A(log,teach,test,True)
			else:
				stage = Stage_U(log,teach,test)
		else:
			if result[0] == 'U':
				if result[1]:
					stage = Stage_U(log,teach,test,True)
				else:
					print('Du bist durch!')


log = Log_Handler()

if len(sys.argv) == 1:
	normal(False,False)
else:
	if '--help' in sys.argv:
		print('\nHelp\n\nfollowing flags accepted:')
		print('\t-s [Stage]\tStart at given Stage')
		print('\t--test\t\tskips all instructions and the teaching part')
		print('\t--teach\t\tskips all instructions and the testing part')
		print('\t--log\t\tprints log file')
		print('\t--log-only\tprint log file and exit')
		sys.exit()

	if '--log-only' in sys.argv:
		print(log)
		sys.exit()

	test = False
	teach = False
	rep = False
	if '--test' in sys.argv:
		test = True

	if '--teach' in sys.argv:
		teach = True

	if '--rep' in sys.argv:
		rep = True

	if '-s' in sys.argv:
		start = sys.argv[sys.argv.index('-s')+1]
		if start == 'a':
			stage = Stage_A(log,teach,test,rep)
		elif start == 'u':
			stage = Stage_U(log,teach,test,rep)
		elif start == 'f':
			stage = Stage_F(log,teach,test,rep)
	else:
		normal(teach,test)
	
	if '--log' in sys.argv:
		print(log)

log.save()

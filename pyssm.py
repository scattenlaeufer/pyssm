#!/usr/bin/python2
# -*- coding: utf-8 -*-
import pygame, sys, time, random
from helpers.log import Log_Handler
from pygame.locals import *
from level.stages import Stage_A, Stage_U, Stage_F, Stage_Q, Stage_P

print(u'ssm training version 0.1\nwirtten by Björn Guth')

def cake():
	print('\n            ,:/+/-\n            /M/\n       .:/= ;MH/,    ,=/+%$XH@MM#@:\n      -$##@+$###@H@MMM#######H:.    -/H#\n.,H@H@ X######@ -H#####@+-     -+H###@x\n    .,@##H;      +XM##M/,     =%@###@X;-\nX%-  :M##########$.    .:%M###@%:\nM##H,   +H@@@$/-.  ,;$M###@%,          -\nM###M=,,---,.-%%H####M$:           ,+@##\n@##################@/.          :%##@$-\nM################H,         ;HM##M$=\n##################.    .=$M##M$=\n#################H..;XM##M$=         .:+\nM####################@%=          =+@MH%\n@#################M/.         =+H#X%=\n=+M###############M,     -/X#X+;.\n  .;XM###########H=    ,/X#H+:,\n    .=+HM#######M+/+HM@+=.\n         ,:/%XM####H/.\n              ,.:=-.\n')
	text_list = [u'If you finish this game, there will be cake!',u'Keep going! Cake is waiting for you!',u'Keep looking ahead for cake.',u"That's just a little fall back! You can still reach the cake!",u'You are making great procress. When you are finished, you will have earned your cake.',u"Eyes forward! You still remember the cake, don't you?",u"What are you waiting for? Go on or you will never get cake!"]
	print('\n'+text_list[random.randint(0,len(text_list)-1)])


def end():

	print('\n             .,-:;//;:=,\n          . :H@@@MM@M#H/.,+%;,\n       ,/X+ +M@@M@MM%=,-%HMMM@X/,\n     -+@MM; $M@@MH+-,;XMMMM@MMMM@+-$\n    ;@M@@M- XM@X;. -+XXXXXHHH@M@M#@/.\n  ,%MM@@MH ,@%=             .---=-=:=,.\n  =@#@@@MX.,                -%HX$$%%%:;\n =-./@M@M$                   .;@MMMM@MM:\n X@/ -$MM/                    . +MM@@@M$\n,@M@H: :@:                    . =X#@@@@-\n,@@@MMX, .                    /H- ;@M@M=\n.H@@@@M@+,                    %MM+..%#$.\n /MMMM@MMH/.                  XM@MH; =;\n  /%+%$XHH@$=              , .H@@@@MX,\n  .=--------.           -%H.,@@@@@MX,\n  .%MM@@@HHHXX$$$%+- .:$MMX =M@@MM%.\n    =XMMM@MM@MM#H;,-+HMM@M+ /MMMX=\n      =%@M@M#@$-.=$@MM@@@M; %M%=\n        ,:+$+-,/H#MMMMMMM@= =,\n              =++%%%%+/:-.')
	print('\nSorry, but the cake was a lie.')

def normal(teach,test,rep):
	result = log.analyze()
	if result[0] == '0':
		cake()
		stage = Stage_A(log,teach,test,rep)
	elif result[0] == 'A':
		if result[1]:
			cake()
			stage = Stage_A(log,teach,test,True)
		else:
			cake()
			stage = Stage_F(log,teach,test,rep)
	elif result[0] == 'F':
		if result[1]:
			cake()
			stage = Stage_F(log,teach,test,True)
		else:
			cake()
			stage = Stage_U(log,teach,test,rep)
	elif result[0] == 'U':
		if result[1]:
			cake()
			stage = Stage_U(log,teach,test,True)
		else:
			cake()
			stage = Stage_Q(log,teach,test,rep)
	elif result[0] == 'Q':
		if result[1]:
			cake()
			stage = Stage_Q(log,teach,test,True)
		else:
			end()

log = Log_Handler()

if len(sys.argv) == 1:
	normal(False,False,False)
else:
	if '--help' in sys.argv:
		print('\nHelp\n\nfollowing flags accepted:')
		print('\t-s [Stage]\tStart at given Stage')
		print('\t--test\t\tskips all instructions and the teaching part')
		print('\t--teach\t\tskips all instructions and the testing part')
		print('\t--rep\t\tstarts the repetition of a stage')
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
		elif start == 'q':
			stage = Stage_Q(log,teach,test,rep)
		elif start == 'p':
			stage = Stage_P(log,teach,test,rep)
	else:
		normal(teach,test)
	
	if '--log' in sys.argv:
		print(log)

log.save()

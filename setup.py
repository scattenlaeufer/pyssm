# -*- coding: utf-8 -*-
from distutils.core import setup

setup(name='pyssm',
		version='0.1',
		description='Small game to teach eight syllables',
		author=u'Björn Guth',
		author_email='bjoern.guth@rwth-aachen.de',
		url='http://www.ukaachen.de/content/folder/1161467',
		py_modules=['stages','engines'],
		packages=['helpers'],
		scripts=['pyssm.py'],
		data_files=[('',['images/bg/bg_wave.jpg',
							'images/bg/bg_smiley.jpg',
							'images/bg/bg_landscape.jpg',
							'images/bg/underwater.gif',

							'images/syllables/BU.gif',
							'images/syllables/KE.gif',
							'images/syllables/FE.gif',
							'images/syllables/LO.gif',
							'images/syllables/lo_left_trans.gif',
							'images/syllables/lo_right_trans.gif',
							'images/syllables/MA.gif',
							'images/syllables/ma_left_trans.gif',
							'images/syllables/ma_right_trans.gif',
							'images/syllables/PA.gif',
							'images/syllables/SU.gif',
							'images/syllables/TI.gif',

							'images/distr/DISTR1.gif',
							'images/distr/DISTR2.gif',
							'images/distr/DISTR3.gif',
							'images/distr/DISTR4.gif',
							'images/distr/DISTR5.gif',
							'images/distr/DISTR6.gif',
							'images/distr/DISTR7.gif',
							'images/distr/DISTR8.gif',
							'images/distr/DISTR9.gif',
							'images/distr/DISTR10.gif',

							'images/stage_a/dog_l.gif',
							'images/stage_a/dog_r.gif',
							'images/stage_a/duck_l.gif',
							'images/stage_a/duck_r.gif',
							'images/stage_a/mouse_l.gif',
							'images/stage_a/mouse_r.gif',
							'images/stage_a/pig_l.gif',
							'images/stage_a/pig_r.gif',

							'images/stage_u/bu_left_trans.gif',
							'images/stage_u/bu_right_trans.gif',
							'images/stage_u/ke_left_trans.gif',
							'images/stage_u/ke_right_trans.gif',
							'images/stage_u/lo_left_trans.gif',
							'images/stage_u/lo_right_trans.gif',
							'images/stage_u/ma_left_trans.gif',
							'images/stage_u/ma_right_trans.gif',
							'images/stage_u/fish1_L.gif',
							'images/stage_u/fish1_R.gif',
							'images/stage_u/fish2_L.gif',
							'images/stage_u/fish2_R.gif',
							'images/stage_u/fish3_L.gif',
							'images/stage_u/fish3_R.gif',
							'images/stage_u/fish4_L.gif',
							'images/stage_u/fish4_R.gif',
							'images/stage_u/fish5_L.gif',
							'images/stage_u/fish5_R.gif',
							'images/stage_u/fish6_L.gif',
							'images/stage_u/fish6_R.gif',])]
		)

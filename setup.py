# -*- coding: utf-8 -*-
from distutils.core import setup
from os import path
import shutil

setup(name='pyssm',
		version='0.1',
		description='Small game to teach eight syllables',
		author='Bjoern Guth',
		author_email='bjoern.guth@rwth-aachen.de',
		url='http://www.ukaachen.de/content/folder/1161467',
		packages=['helpers','level'],
		scripts=['pyssm.py'],
		package_dir={'level':'level'},
		package_data={'level':['images/bg/bg_wave.jpg',
							'images/bg/bg_smiley.jpg',
							'images/bg/bg_landscape.jpg',
							'images/bg/underwater.gif',
							'images/bg/background_space.gif',
							'images/bg/bg_sky.jpg',

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

							'images/stage_f/ufoke.gif',
							'images/stage_f/ufolo.gif',
							'images/stage_f/ufoma.gif',

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
							'images/stage_u/fish6_R.gif',

							'images/stage_q/bu_g.gif',
							'images/stage_q/bu_r.gif',
							'images/stage_q/bu_y.gif',
							'images/stage_q/ke_g.gif',
							'images/stage_q/ke_r.gif',
							'images/stage_q/ke_y.gif',
							'images/stage_q/lo_g.gif',
							'images/stage_q/lo_r.gif',
							'images/stage_q/lo_y.gif',
							'images/stage_q/ma_g.gif',
							'images/stage_q/ma_r.gif',
							'images/stage_q/ma_y.gif',
							'images/stage_q/ti_g.gif',
							'images/stage_q/ti_r.gif',
							'images/stage_q/ti_y.gif',

							'audio/final/final1.ogg',
							'audio/final/final2.ogg',

							'audio/instr/instr1.ogg',
							'audio/instr/instr2.ogg',
							'audio/instr/instr3.ogg',
							'audio/instr/instr4.ogg',
							'audio/instr/instr5.ogg',
							'audio/instr/instr6.ogg',
							'audio/instr/instr7.ogg',
							'audio/instr/instr8.ogg',
							'audio/instr/instr9.ogg',
							'audio/instr/instr10.ogg',
							'audio/instr/instr11.ogg',
							'audio/instr/instr12.ogg',
							'audio/instr/instr13.ogg',
							'audio/instr/instr14.ogg',
							'audio/instr/instr15.ogg',
							'audio/instr/instr16.ogg',
							'audio/instr/instr17.ogg',
							'audio/instr/instr18.ogg',
							'audio/instr/instr19.ogg',
							'audio/instr/instr20.ogg',

							'audio/misc/repeat.ogg',

							'audio/pres/presbu.ogg',
							'audio/pres/presfe.ogg',
							'audio/pres/preske.ogg',
							'audio/pres/preslo.ogg',
							'audio/pres/presma.ogg',
							'audio/pres/prespa.ogg',
							'audio/pres/pressu.ogg',
							'audio/pres/presti.ogg',

							'audio/syllable/bu1.ogg',
							'audio/syllable/bu2.ogg',
							'audio/syllable/bu3.ogg',
							'audio/syllable/bumiss.ogg',
							'audio/syllable/buneg1.ogg',
							'audio/syllable/buneg2.ogg',
							'audio/syllable/bupos1.ogg',
							'audio/syllable/bupos2.ogg',
							'audio/syllable/bupos3.ogg',
							'audio/syllable/bupos4.ogg',
							'audio/syllable/fe1.ogg',
							'audio/syllable/fe2.ogg',
							'audio/syllable/fe3.ogg',
							'audio/syllable/femiss.ogg',
							'audio/syllable/feneg1.ogg',
							'audio/syllable/feneg2.ogg',
							'audio/syllable/fepos1.ogg',
							'audio/syllable/fepos2.ogg',
							'audio/syllable/fepos3.ogg',
							'audio/syllable/fepos4.ogg',
							'audio/syllable/ke1.ogg',
							'audio/syllable/ke2.ogg',
							'audio/syllable/ke3.ogg',
							'audio/syllable/kemiss.ogg',
							'audio/syllable/keneg1.ogg',
							'audio/syllable/keneg2.ogg',
							'audio/syllable/kepos1.ogg',
							'audio/syllable/kepos2.ogg',
							'audio/syllable/kepos3.ogg',
							'audio/syllable/kepos4.ogg',
							'audio/syllable/lo1.ogg',
							'audio/syllable/lo2.ogg',
							'audio/syllable/lo3.ogg',
							'audio/syllable/lomiss.ogg',
							'audio/syllable/loneg1.ogg',
							'audio/syllable/loneg2.ogg',
							'audio/syllable/lopos1.ogg',
							'audio/syllable/lopos2.ogg',
							'audio/syllable/lopos3.ogg',
							'audio/syllable/lopos4.ogg',
							'audio/syllable/ma1.ogg',
							'audio/syllable/ma2.ogg',
							'audio/syllable/ma3.ogg',
							'audio/syllable/mamiss.ogg',
							'audio/syllable/maneg1.ogg',
							'audio/syllable/maneg2.ogg',
							'audio/syllable/mapos1.ogg',
							'audio/syllable/mapos2.ogg',
							'audio/syllable/mapos3.ogg',
							'audio/syllable/mapos4.ogg',
							'audio/syllable/pa1.ogg',
							'audio/syllable/pa2.ogg',
							'audio/syllable/pa3.ogg',
							'audio/syllable/pamiss.ogg',
							'audio/syllable/paneg1.ogg',
							'audio/syllable/paneg2.ogg',
							'audio/syllable/papos1.ogg',
							'audio/syllable/papos2.ogg',
							'audio/syllable/papos3.ogg',
							'audio/syllable/papos4.ogg',
							'audio/syllable/su1.ogg',
							'audio/syllable/su2.ogg',
							'audio/syllable/su3.ogg',
							'audio/syllable/sumiss.ogg',
							'audio/syllable/suneg1.ogg',
							'audio/syllable/suneg2.ogg',
							'audio/syllable/supos1.ogg',
							'audio/syllable/supos2.ogg',
							'audio/syllable/supos3.ogg',
							'audio/syllable/supos4.ogg',
							'audio/syllable/ti1.ogg',
							'audio/syllable/ti2.ogg',
							'audio/syllable/ti3.ogg',
							'audio/syllable/timiss.ogg',
							'audio/syllable/tineg1.ogg',
							'audio/syllable/tineg2.ogg',
							'audio/syllable/tipos1.ogg',
							'audio/syllable/tipos2.ogg',
							'audio/syllable/tipos3.ogg',
							'audio/syllable/tipos4.ogg',

							'data/modul_a',
							'data/modul_b',
							'data/modul_f',
							'data/modul_l',
							'data/modul_p',
							'data/modul_q',
							'data/modul_u',
							'data/modul_z'
							]}
		)

shutil.copy('pyssm.py',path.join(path.expanduser('~'),'pyssm.py'))
